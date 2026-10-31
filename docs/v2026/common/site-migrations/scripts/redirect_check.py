#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright 2026 MOZGII, Inc. (https://mozgii.com/)
"""Check a redirect map after (or before) a site migration.

Usage:
  python3 redirect_check.py map.csv [--delay 0.2] [--out results.tsv]

map.csv has two columns, old URL and expected new URL, with or without a header row. Both are absolute URLs, because
the script requests them; a map of relative paths must get its scheme and host first:
  https://old.example.com/shoes,https://www.example.com/footwear/
Write "gone" in the second column, in place of the new URL, when the old URL should answer 404 or 410:
  https://old.example.com/sale-2019,gone

For each old URL the script follows redirects one hop at a time and reports PASS when the first hop is a 301 or 308
straight to the expected URL and that URL answers 200. Otherwise it names the problem: WRONG_TARGET, TEMPORARY
(302/303/307), CHAIN (more than one hop), LOOP, TARGET_NOT_200, NO_REDIRECT, SHOULD_BE_GONE. Standard library only.
Exit 0 when every row passes, 1 when any row fails, 2 on usage error, an unreadable map or a map with no usable row.
"""
from __future__ import annotations

import csv
import http.client
import math
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; redirect-check/1.0)"
NO_ROWS = "no usable row: every row needs an absolute old URL (http:// or https://), not a relative path like /old-page"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *_hop):  # noqa: ANN002, ANN201
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def hop(url: str) -> tuple[int, str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
        with OPENER.open(req, timeout=30) as r:
            return r.status, ""
    except urllib.error.HTTPError as e:
        loc = e.headers.get("Location", "")
        try:
            return e.code, urllib.parse.urljoin(url, loc) if loc else ""
        except ValueError:
            return e.code, loc
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException) as e:
        return 0, str(e)


def norm(u: str) -> str:
    try:
        p = urllib.parse.urlsplit(u.strip())
    except ValueError:
        return u.strip()
    return urllib.parse.urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path or "/", p.query, ""))


def check(old: str, new: str) -> tuple[str, list[str]]:
    chain: list[str] = []
    url, seen = old, set()
    first_status = None
    for _ in range(10):
        status, loc = hop(url)
        chain.append(f"{status} {url}")
        first_status = first_status if first_status is not None else status
        if status in (301, 302, 303, 307, 308) and loc:
            if loc in seen:
                return "LOOP", chain
            seen.add(url)
            url = loc
            continue
        break
    hops = len(chain) - 1
    if new.lower() == "gone":
        return ("PASS" if first_status in (404, 410) else "SHOULD_BE_GONE"), chain
    if hops == 0:
        return "NO_REDIRECT", chain
    final_status = int(chain[-1].split(" ", 1)[0])
    if norm(url) != norm(new):
        return "WRONG_TARGET", chain
    if first_status not in (301, 308):
        return "TEMPORARY", chain
    if hops > 1:
        return "CHAIN", chain
    if final_status != 200:
        return "TARGET_NOT_200", chain
    return "PASS", chain


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    args: list[str] = []
    opts: dict[str, str] = {}
    it = iter(argv)
    for a in it:
        if a.startswith("--"):
            opts[a] = next(it, "")
        else:
            args.append(a)
    if not args:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        delay = float(opts.get("--delay", "0.2"))
    except ValueError:
        delay = -1.0
    if delay < 0 or not math.isfinite(delay):
        print("--delay takes a number of seconds, 0 or more", file=sys.stderr)
        return 2
    try:
        with open(args[0], newline="", encoding="utf-8") as f:
            rows = [r for r in csv.reader(f) if len(r) >= 2 and r[0].startswith(("http://", "https://"))]
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        print(f"cannot read {args[0]}: {e}", file=sys.stderr)
        return 2
    if not rows:
        print(f"{args[0]}: {NO_ROWS}", file=sys.stderr)
        return 2
    results: list[tuple[str, str, str, str]] = []
    counts: dict[str, int] = {}
    for old, new, *_ in rows:
        verdict, chain = check(old, new)
        counts[verdict] = counts.get(verdict, 0) + 1
        results.append((verdict, old, new, " | ".join(chain)))
        if verdict != "PASS":
            print(f"{verdict}\t{old}\texpected {new}\t{' | '.join(chain)}")
        time.sleep(delay)
    if "--out" in opts:
        with open(opts["--out"], mode="w", encoding="utf-8") as out:
            out.write("verdict\told\texpected\tchain\n" + "".join("\t".join(r) + "\n" for r in results))
    print("summary: " + ", ".join(f"{name} {n}" for name, n in sorted(counts.items())) + f" (of {len(rows)})")
    return 0 if counts.get("PASS", 0) == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
