#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright 2026 MOZGII, Inc. (https://mozgii.com/)
"""Read a site's XML sitemaps and check them against the protocol and against the pages they list.

Usage:
  python3 sitemap_check.py https://example.com/              # finds sitemaps through robots.txt, else /sitemap.xml
  python3 sitemap_check.py https://example.com/sitemap.xml   # one sitemap or sitemap index
  options: --sample N   check N listed URLs (default 20; 0 skips): status, redirect, noindex, canonical
           --tsv FILE   write every listed URL with its lastmod

Checks: each file parses, holds at most 50,000 URLs and 50 MB uncompressed, uses absolute URLs on the same host
(a relative or empty loc is reported and never fetched), lastmod values that are valid W3C dates and not in the future, and whether every lastmod is identical (a sign the
value is generated rather than real). A root other than urlset or sitemapindex in the protocol's http:// namespace, or a
file that lists nothing, is a problem: engines would read 0 URLs from it. Sample checks flag URLs that redirect, fail, carry noindex or point their
canonical elsewhere: none of those belong in a sitemap. Standard library only (Python 3.9+).
Exit 0 when no problem is found, 1 when there are problems, 2 on usage error.
"""
from __future__ import annotations

import datetime as dt
import http.client
import random
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zlib
from email.message import Message
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; sitemap-check/1.0)"
PROTOCOL = "www.sitemaps.org/schemas/sitemap"
NS = f"{{http://{PROTOCOL}/0.9}}"
LIMIT_URLS, LIMIT_BYTES = 50_000, 50 * 1024 * 1024
LASTMOD_FORMATS = ("%Y", "%Y-%m", "%Y-%m-%d", "%Y-%m-%dT%H:%M%z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *_hop):  # noqa: ANN002, ANN201
        return None


class Head(HTMLParser):
    """Meta robots values and the first canonical, whatever the order or quoting of their attributes."""

    def __init__(self) -> None:
        super().__init__()
        self.robots: list[str] = []
        self.canonical = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta" and a.get("name", "").lower() == "robots":
            self.robots.append(a.get("content", ""))
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split() and not self.canonical:
            self.canonical = a.get("href", "")


def absolute(url: str) -> bool:
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return False
    return parts.scheme in ("http", "https") and bool(parts.netloc)


def parse_lastmod(value: str) -> dt.datetime | None:
    """A W3C datetime as an aware value, or None when it is not one."""
    day, _, clock = value.partition("T")
    if len(day) not in (4, 7, 10) or (clock and not (clock.endswith("Z") or clock[-3:-2] == ":")):
        return None
    digits = re.sub(r"(\.[0-9]{6})[0-9]+", r"\1", value)
    for pattern in LASTMOD_FORMATS:
        try:
            parsed = dt.datetime.strptime(digits, pattern)
        except ValueError:
            continue
        return parsed.replace(tzinfo=parsed.tzinfo or dt.timezone.utc)
    return None


def same_url(base: str, href: str) -> bool:
    try:
        return urllib.parse.urljoin(base, href) == base
    except ValueError:
        return False


def lowered(headers: Message) -> dict[str, str]:
    """Header names in lowercase; a repeated header keeps every copy, as X-Robots-Tag often has more than one."""
    return {name.lower(): ", ".join(headers.get_all(name) or []) for name in headers.keys()}


def get(url: str, follow: bool = True) -> tuple[int, dict[str, str], bytes]:
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect)
    try:
        request = urllib.request.Request(url, headers={"User-Agent": UA})
        with opener.open(request, timeout=30) as answer:
            return answer.status, lowered(answer.headers), answer.read(LIMIT_BYTES + 1)
    except urllib.error.HTTPError as refused:
        return refused.code, lowered(refused.headers), b""
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException) as failed:
        return 0, {"error": str(getattr(failed, "reason", failed))}, b""


def find_sitemaps(start: str) -> list[str]:
    if urllib.parse.urlsplit(start).path.endswith((".xml", ".gz", ".txt")):
        return [start]
    root = urllib.parse.urljoin(start, "/")
    status, _, body = get(urllib.parse.urljoin(root, "/robots.txt"))
    found = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", body.decode("utf-8", "replace")) if status == 200 else []
    return found or [urllib.parse.urljoin(root, "/sitemap.xml")]


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
    if not args or not absolute(args[0]) or not opts.get("--sample", "20").isdigit():
        print(__doc__, file=sys.stderr)
        return 2
    sample = int(opts.get("--sample", "20"))
    host = urllib.parse.urlsplit(args[0]).netloc
    problems: list[str] = []
    urls: list[tuple[str, str]] = []
    queue, seen = find_sitemaps(args[0]), set()
    now = dt.datetime.now(dt.timezone.utc)
    while queue:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        if not absolute(sm):
            problems.append(f"relative or empty sitemap URL {sm!r}")
            continue
        status, headers, body = get(sm)
        if status != 200:
            problems.append(f"{sm}: no response ({headers['error']})" if status == 0 else f"{sm}: HTTP {status}")
            continue
        if body[:2] == b"\x1f\x8b":
            try:
                body = zlib.decompressobj(wbits=31).decompress(body, LIMIT_BYTES + 1)
            except zlib.error as e:
                problems.append(f"{sm}: gzip does not decompress ({e})")
                continue
        if len(body) > LIMIT_BYTES:
            problems.append(f"{sm}: over 50 MB uncompressed")
        if sm.endswith(".txt"):
            lines = [ln.strip() for ln in body.decode("utf-8", "replace").splitlines() if ln.strip()]
            urls.extend((ln, "") for ln in lines)
            problems.extend(f"{sm}: relative or empty loc {ln!r}" for ln in lines if not absolute(ln))
            print(f"{sm}: text sitemap, {len(lines)} URLs")
            if not lines:
                problems.append(f"{sm}: 0 URLs")
            continue
        try:
            root = ET.fromstring(body)
        except ET.ParseError as e:
            problems.append(f"{sm}: XML does not parse ({e})")
            continue
        if root.tag not in (f"{NS}urlset", f"{NS}sitemapindex"):
            problems.append(f"{sm}: root is {root.tag!r}; expected urlset or sitemapindex in namespace http://{PROTOCOL}/0.9")
            continue
        if root.tag == f"{NS}sitemapindex":
            children = [el.findtext(f"{NS}loc", "").strip() for el in root.findall(f"{NS}sitemap")]
            print(f"{sm}: sitemap index, {len(children)} sitemaps")
            if not any(children):
                problems.append(f"{sm}: sitemap index lists 0 sitemaps")
            queue.extend(c for c in children if c)
            continue
        entries = root.findall(f"{NS}url")
        print(f"{sm}: {len(entries)} URLs")
        if not entries:
            problems.append(f"{sm}: 0 URLs")
        if len(entries) > LIMIT_URLS:
            problems.append(f"{sm}: {len(entries)} URLs, over the 50,000 limit")
        lastmods: set[str] = set()
        for el in entries:
            loc = (el.findtext(f"{NS}loc") or "").strip()
            lm = (el.findtext(f"{NS}lastmod") or "").strip()
            urls.append((loc, lm))
            if not absolute(loc):
                problems.append(f"{sm}: relative or empty loc {loc!r}")
            elif urllib.parse.urlsplit(loc).netloc != host:
                problems.append(f"{sm}: other host {loc}")
            if lm:
                lastmods.add(lm)
                when = parse_lastmod(lm)
                if when is None:
                    problems.append(f"{sm}: lastmod not a W3C date {lm!r} ({loc})")
                elif when > now + dt.timedelta(days=1):
                    problems.append(f"{sm}: lastmod in the future {lm} ({loc})")
        if len(entries) > 20 and len(lastmods) == 1:
            problems.append(f"{sm}: every lastmod is {next(iter(lastmods))}: probably generated, not the real change date")
    dupes = len(urls) - len({u for u, _ in urls})
    if dupes:
        problems.append(f"{dupes} duplicate URLs across sitemaps")
    print(f"total: {len(urls)} URLs in {len(seen)} files")
    if "--tsv" in opts:
        with open(opts["--tsv"], mode="w", encoding="utf-8") as out:
            out.write("url\tlastmod\n" + "".join(f"{u}\t{m}\n" for u, m in urls))
    fetchable = [u for u, _ in urls if absolute(u)]
    for loc in random.sample(fetchable, min(sample, len(fetchable))):
        status, headers, body = get(loc, follow=False)
        if status == 0:
            problems.append(f"listed URL gives no response: {loc} ({headers['error']})")
            continue
        head = Head()
        head.feed(body[:400_000].decode("utf-8", "replace"))
        if status != 200:
            problems.append(f"listed URL returns {status}: {loc}" + (f" -> {headers.get('location')}" if headers.get("location") else ""))
        if "noindex" in " ".join([*head.robots, headers.get("x-robots-tag", "")]).lower():
            problems.append(f"listed URL is noindex: {loc}")
        if head.canonical and head.canonical != loc and not same_url(loc, head.canonical):
            problems.append(f"listed URL canonicalises elsewhere: {loc} -> {head.canonical}")
    for p in problems:
        print("PROBLEM", p)
    print(f"{'FAIL' if problems else 'PASS'}: {len(problems)} problems")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
