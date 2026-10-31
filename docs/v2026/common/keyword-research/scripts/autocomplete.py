#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright 2026 MOZGII, Inc. (https://mozgii.com/)
"""Expand seed phrases into candidate queries from Bing (default) or Google autocomplete, ranked by a suggest Signal.

Usage:
  python3 autocomplete.py "running shoes" ["trail shoes" ...] [--hl en] [--gl us] [--engine bing|google]
                          [--modifiers questions|commercial|alphabet|none] [--out candidates.tsv]

For each seed the script asks the engine's public suggestion endpoint for the seed alone and for the seed combined
with modifiers (question words, commercial words, or a-z), then scores every suggestion with
Signal = sum of 1/position over every list it appears in. Signal ranks candidates against each other; it is NOT a
search volume. Check volume afterwards in Google Keyword Planner, Bing Webmaster Tools Keyword Research or a paid
tool. The endpoints are unofficial and undocumented: they may change or rate-limit without notice; the script waits
0.7 s between calls and caches answers for 7 days in .seo-cache/autocomplete.json. Standard library only.
Bing is the default because Google's spam policies name automated queries to Google as machine-generated traffic.
With --engine google you accept that risk yourself: requests can be blocked, and a script that sends them breaks that
policy. Use it for a few seeds at most, never on a schedule, and never with --modifiers alphabet on a long list.
Exit 0 on success, 1 when every request failed, 2 on usage error.
"""
from __future__ import annotations

import json
import string
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

MODIFIERS = {
    "questions": ["", "how ", "what ", "why ", "which ", "can ", "best ", " vs", " for", " near me"],
    "commercial": ["", " price", " cost", " buy", " best", " review", " vs", " alternative", " cheap", " online"],
    "alphabet": [""] + [f" {c}" for c in string.ascii_lowercase],
    "none": [""],
}
CACHE = Path(".seo-cache/autocomplete.json")


def endpoint(engine: str, q: str, hl: str, gl: str) -> str:
    if engine == "bing":
        return "https://api.bing.com/osjson.aspx?" + urllib.parse.urlencode({"query": q, "market": f"{hl}-{gl.upper()}"})
    return "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode({"client": "firefox", "q": q, "hl": hl, "gl": gl})


def suggest(engine: str, q: str, hl: str, gl: str, cache: dict[str, dict[str, object]]) -> list[str]:
    key = f"{engine}|{hl}|{gl}|{q}"
    hit = cache.get(key)
    if hit and time.time() - float(str(hit["t"])) < 7 * 86400:
        return [str(s) for s in hit["s"]]  # type: ignore[union-attr]
    req = urllib.request.Request(endpoint(engine, q, hl, gl), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8", "replace"))
    out = [str(s) for s in data[1]] if isinstance(data, list) and len(data) > 1 else []
    cache[key] = {"t": time.time(), "s": out}
    time.sleep(0.7)
    return out


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    seeds: list[str] = []
    opts: dict[str, str] = {}
    it = iter(argv)
    for a in it:
        if a.startswith("--"):
            opts[a] = next(it, "")
        else:
            seeds.append(a)
    engine, hl, gl = opts.get("--engine", "bing"), opts.get("--hl", "en"), opts.get("--gl", "us")
    mods = MODIFIERS.get(opts.get("--modifiers", "questions"))
    if not seeds or mods is None or engine not in ("google", "bing"):
        print(__doc__, file=sys.stderr)
        return 2
    if engine == "google":
        print("warning: --engine google sends automated queries, which Google's spam policies forbid; requests may be blocked", file=sys.stderr)
    try:
        cache = json.loads(CACHE.read_bytes())
    except (OSError, ValueError):
        cache = {}
    rows: list[tuple[str, str, float, int]] = []
    ok = failed = 0
    for seed in seeds:
        signal: dict[str, float] = {}
        lists: dict[str, int] = {}
        for m in mods:
            q = (m + seed) if m.endswith(" ") else (seed + m)
            try:
                found = suggest(engine, q.strip(), hl, gl, cache)
                ok += 1
            except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as e:
                failed += 1
                print(f"request failed for {q!r}: {e}", file=sys.stderr)
                continue
            for pos, s in enumerate(found, 1):
                k = s.lower().strip()
                signal[k] = signal.get(k, 0.0) + 1 / pos
                lists[k] = lists.get(k, 0) + 1
        rows.extend((seed, k, v, lists[k]) for k, v in signal.items())
    CACHE.parent.mkdir(exist_ok=True, parents=True)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    rows.sort(key=lambda r: (r[0], -r[2]))
    text = "seed\tcandidate\tsignal\tlists\n" + "".join(f"{s}\t{c}\t{v:.2f}\t{n}\n" for s, c, v, n in rows)
    if "--out" in opts:
        Path(opts["--out"]).write_text(text, encoding="utf-8")
    print(text, end="")
    return int(ok == 0 and failed > 0)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
