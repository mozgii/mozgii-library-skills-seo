#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright 2026 MOZGII, Inc. (https://mozgii.com/)
"""Check hreflang annotations across a set of language or country versions of one page.

Usage:
  python3 hreflang_check.py https://example.com/en/page [https://example.com/de/seite ...]

Starts from the given URLs, reads the hreflang annotations in each page's HTML <link> tags and in its HTTP Link
header, then fetches every alternate it finds (up to 60 pages). Reports, per page: missing self reference, missing
return link (A names B but B does not name A), an alternate that does not answer 200 directly, a canonical that
points elsewhere (hreflang must sit on canonical URLs), invalid codes (a region alone, reserved codes such as UK or
EU, unsupported forms such as es-419) and duplicate codes. A page that cannot be requested, such as an href with a
space, is a problem. A missing x-default is optional, and kr and se are real language codes (Kanuri, Northern Sami) that
are usually Korea or Sweden typed by mistake: both print as a NOTE and do not fail the run. Standard library only.
Exit 0 when the cluster has no problems (NOTE lines allowed), 1 when there are problems, 2 on usage error.
"""
from __future__ import annotations

import http.client
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; hreflang-check/1.0)"
RESERVED = {"UK", "EU", "UN"}
# Two-letter country codes people often mistake for languages; none of these is an ISO 639-1 language.
NOT_LANGUAGES = {"jp": "ja", "cn": "zh", "gr": "el", "dk": "da", "ua": "uk", "cz": "cs", "us": "en-US"}
# Country codes that are also real ISO 639-1 languages: valid, but rarely what the site meant.
LIKELY_COUNTRIES = {"kr": ("Kanuri", "ko"), "se": ("Northern Sami", "sv")}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *_hop):  # noqa: ANN002, ANN201
        return None


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.alts: list[tuple[str, str]] = []
        self.canonical = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "link":
            return
        a = {k.lower(): (v or "") for k, v in attrs}
        rel = a.get("rel", "").lower().split()
        if "alternate" in rel and a.get("hreflang"):
            self.alts.append((a["hreflang"], a.get("href", "")))
        if "canonical" in rel and not self.canonical:
            self.canonical = a.get("href", "")


def valid_shape(code: str) -> bool:
    """Language, optional 4-letter script, optional 2-letter region: en, zh-Hant, en-GB, zh-Hant-TW."""
    language, *rest = code.split("-")
    lengths = [len(part) for part in rest]
    return (
        len(language) == 2
        and code.replace("-", "").isascii()
        and code.replace("-", "").isalpha()
        and lengths in ([], [4], [2], [4, 2])
    )


def joined(base: str, href: str) -> str:
    """The absolute URL, or the href as written, which then fails at the fetch and is reported."""
    try:
        return urllib.parse.urljoin(base, href)
    except ValueError:
        return href


def fetch(url: str) -> tuple[int, list[tuple[str, str]], str, str]:
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
            status, header, body = r.status, ", ".join(r.headers.get_all("Link") or []), r.read(3_000_000)
    except urllib.error.HTTPError as refused:
        return refused.code, [], "", ""
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException) as failed:
        return 0, [], "", str(getattr(failed, "reason", failed))
    p = Links()
    p.feed(body.decode("utf-8", "replace"))
    alts = [(c, joined(url, h)) for c, h in p.alts]
    for m in re.finditer(r'<([^>]+)>\s*;([^,]*hreflang="?([^";,]+)"?[^,]*)', header):
        if "alternate" in m.group(2):
            alts.append((m.group(3), joined(url, m.group(1))))
    return status, alts, joined(url, p.canonical) if p.canonical else "", ""


def code_problem(code: str) -> str:
    if code.lower() == "x-default":
        return ""
    if code.lower() in NOT_LANGUAGES:
        return f"'{code}' is not a language code (did you mean '{NOT_LANGUAGES[code.lower()]}'?)"
    if re.search(r"-\d{3}$", code):
        return f"'{code}' uses a numeric region; Google does not support codes such as es-419"
    if not valid_shape(code):
        return f"'{code}' is not ISO 639-1 language [+ script] [+ ISO 3166-1 region]"
    region = code.split("-")[-1]
    if len(code.split("-")) > 1 and len(region) == 2 and region.upper() in RESERVED:
        return f"'{code}' uses reserved region {region.upper()} (UK is GB)"
    return ""


def code_note(code: str) -> str:
    language, _, region = code.lower().partition("-")
    if language in LIKELY_COUNTRIES and region in ("", language):
        name, meant = LIKELY_COUNTRIES[language]
        return f"'{code}' is {name}; if the page is for that country's main language, use '{meant}'"
    return ""


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    start = [a for a in argv if a.startswith(("http://", "https://"))]
    if not start:
        print(__doc__, file=sys.stderr)
        return 2
    pages: dict[str, tuple[int, list[tuple[str, str]], str, str]] = {}
    queue = list(start)
    while queue and len(pages) < 60:
        url = queue.pop(0)
        if url in pages:
            continue
        pages[url] = fetch(url)
        queue.extend(h for _, h in pages[url][1] if h not in pages)
    problems: list[str] = []
    notes: list[str] = []
    for url, (status, alts, canonical, error) in pages.items():
        if status != 200:
            answer = f"answers {status}" if status else f"could not be requested ({error})"
            problems.append(f"{url}: {answer}; alternates must answer 200 without a redirect")
            continue
        if not alts:
            problems.append(f"{url}: no hreflang annotations")
            continue
        if canonical and canonical != url:
            problems.append(f"{url}: canonical points to {canonical}; put hreflang on canonical URLs only")
        codes = [c for c, _ in alts]
        for c in sorted(set(codes)):
            if codes.count(c) > 1 and len({h for cc, h in alts if cc == c}) > 1:
                problems.append(f"{url}: code {c} names more than one URL")
            if msg := code_problem(c):
                problems.append(f"{url}: {msg}")
            if msg := code_note(c):
                notes.append(f"{url}: {msg}")
        if url not in {h for _, h in alts}:
            problems.append(f"{url}: no self-referencing hreflang")
        if "x-default" not in {c.lower() for c in codes}:
            notes.append(f"{url}: no x-default (optional, recommended for a language selector or fallback)")
        for code, href in alts:
            other = pages.get(href)
            if other and other[0] == 200 and url not in {h for _, h in other[1]}:
                problems.append(f"{url}: names {href} as {code}, but that page has no return link")
    print(f"checked {len(pages)} pages")
    for n in notes:
        print("NOTE", n)
    for p in problems:
        print("PROBLEM", p)
    print(f"{'FAIL' if problems else 'PASS'}: {len(problems)} problems")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
