#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright 2026 MOZGII, Inc. (https://mozgii.com/)
"""Check one page the way Naver's Yeti crawler reads it, without an account.

Usage:
  python3 naver_check.py https://example.co.kr/page
  python3 naver_check.py https://example.co.kr/page --key 0123456789abcdef [--key-location https://example.co.kr/k.txt]

Reports PROBLEM for what keeps a page out of Naver (blocked in robots.txt, noindex, a non-200 status, no title, a
relative canonical, HTML over 4 MB, a charset that disagrees with the server, a bad IndexNow key) and NOTE for what the
guides warn about (a title over 40 or a description over 80 characters, repeated words, frames, links only in
JavaScript, no viewport, a weak og:image setup, a missing or oversized sitemap, nosourceinfo, nosublinks). An
X-Robots-Tag counts when it has no crawler prefix or a yeti: prefix; another crawler's directives are left out.
Standard library only (Python 3.9+).
Exit 0 when there is no PROBLEM (NOTE lines allowed), 1 when there is one, 2 on usage error.
"""
from __future__ import annotations

import http.client
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from email.message import Message
from html.parser import HTMLParser

YETI = "Mozilla/5.0 (compatible; Yeti/1.1; +https://naver.me/spd)"
READ_LIMIT = 11_000_000
HTML_LIMIT = 4_000_000
FEED_LIMIT = 10_000_000
SITEMAP_URLS = 50_000
TITLE_CHARS, DESCRIPTION_CHARS = 40, 80
FETCH_ERRORS = (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException)
HEX_KEY = re.compile(r"[a-fA-F0-9-]{8,128}")
WORD = re.compile(r"[\w가-힣]{2,}")
AGENT = re.compile(r"[a-z][-\w]*")
VALUE_DIRECTIVES = {"unavailable_after", "max-video-preview", "max-image-preview", "max-snippet"}


class KeepRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *_hop):  # noqa: ANN002, ANN201
        return None


class Page(HTMLParser):
    """Collects the tags Search Advisor's guides name, from the HTML the crawler gets."""

    def __init__(self) -> None:
        super().__init__()
        self.titles: list[str] = []
        self.meta: dict[str, str] = {}
        self.robots: list[str] = []
        self.canonical = ""
        self.icons: Counter[str] = Counter()
        self.charset = ""
        self.frames = 0
        self.h1 = 0
        self.script_links = 0
        self.nosublink = 0
        self.in_title = False
        self.in_body = False
        self.verification_in_body = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        fields = {name.lower(): (value or "") for name, value in attrs}
        if tag == "body":
            self.in_body = True
        elif tag == "title":
            self.in_title = True
            self.titles.append("")
        elif tag == "h1":
            self.h1 += 1
        elif tag in ("frame", "frameset"):
            self.frames += 1
        elif tag == "a":
            href = fields.get("href", "").strip().lower()
            if href.startswith("javascript:") or (href in ("", "#") and "onclick" in fields):
                self.script_links += 1
            if "nosublink" in fields.get("rel", "").lower():
                self.nosublink += 1
        elif tag == "link":
            rel = fields.get("rel", "").lower().strip()
            if rel == "canonical":
                self.canonical = fields.get("href", "")
            elif rel in ("shortcut icon", "icon", "apple-touch-icon", "apple-touch-icon-precomposed"):
                self.icons[rel] += 1
        elif tag == "meta":
            self.read_meta(fields)

    def read_meta(self, fields: dict[str, str]) -> None:
        name = (fields.get("name") or fields.get("property") or "").lower()
        content = fields.get("content", "")
        if "charset" in fields:
            self.charset = fields["charset"].lower()
        if name in ("robots", "naver", "yeti"):
            self.robots.append(content.lower())
        elif name:
            self.meta[name] = content
        if name == "naver-site-verification" and self.in_body:
            self.verification_in_body = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.titles[-1] += data


def fetch(url: str) -> tuple[int, Message | None, bytes, str]:
    opener = urllib.request.build_opener(KeepRedirects)
    try:
        request = urllib.request.Request(url, headers={"User-Agent": YETI})
        with opener.open(request, timeout=30) as answer:
            return answer.status, answer.headers, answer.read(READ_LIMIT), ""
    except urllib.error.HTTPError as refused:
        return refused.code, refused.headers, b"", ""
    except FETCH_ERRORS as failed:
        return 0, None, b"", str(getattr(failed, "reason", failed))


def rules_for_yeti(robots: str) -> list[tuple[str, str]]:
    groups: dict[str, list[tuple[str, str]]] = {}
    agents: list[str] = []
    in_rules = False
    for raw in robots.splitlines():
        field, _, value = raw.split("#", 1)[0].partition(":")
        field, value = field.strip().lower(), value.strip()
        if field == "user-agent":
            if in_rules:
                agents, in_rules = [], False
            agents.append(value.lower())
            groups.setdefault(value.lower(), [])
        elif field in ("allow", "disallow") and agents:
            in_rules = True
            for agent in agents:
                groups[agent].append((field, value))
    return groups.get("yeti", groups.get("*", []))


def blocked(rules: list[tuple[str, str]], path: str) -> bool:
    """RFC 9309: the longest matching rule wins, and allow wins a tie."""
    best, verdict = -1, False
    for kind, pattern in rules:
        if not pattern:
            continue
        body = ".*".join(re.escape(part) for part in pattern.rstrip("$").split("*"))
        if re.match(body + ("$" if pattern.endswith("$") else ""), path):
            if len(pattern) > best or (len(pattern) == best and kind == "allow"):
                best, verdict = len(pattern), kind == "disallow"
    return verdict


def repeated_words(text: str) -> list[str]:
    counts = Counter(word.lower() for word in WORD.findall(text))
    return sorted(word for word, seen in counts.items() if seen >= 2)


def check_robots(origin: str, target: str, problems: list[str], notes: list[str]) -> list[str]:
    status, headers, body, error = fetch(f"{origin}/robots.txt")
    if status == 0:
        problems.append(f"robots.txt did not answer: {error}")
        return []
    if status >= 500:
        problems.append(f"robots.txt answers {status}: Yeti reads a 5xx as disallow all")
        return []
    if status in (301, 302, 307, 308):
        notes.append(f"robots.txt redirects ({status}); Yeti follows up to 5 HTTP redirects, then allows all")
        return []
    if status != 200:
        notes.append(f"robots.txt answers {status}: Yeti reads a 4xx as allow all")
        return []
    if "html" in (headers.get_content_type() if headers else ""):
        notes.append("robots.txt comes back as HTML, which Yeti may read as no file: serve text/plain")
    text = body.decode("utf-8", "replace")
    if blocked(rules_for_yeti(text), target):
        problems.append(f"robots.txt blocks Yeti from {target}")
    sitemaps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", text)
    if not sitemaps:
        notes.append("robots.txt has no Sitemap line")
    return sitemaps


def check_sitemap(url: str, host: str, problems: list[str], notes: list[str]) -> None:
    status, _, body, error = fetch(url)
    if status != 200:
        notes.append(f"sitemap {url} answers {status or error}")
        return
    locations = re.findall(r"<loc>\s*([^<\s]+)", body.decode("utf-8", "replace"))
    if len(body) >= FEED_LIMIT:
        problems.append(f"sitemap {url} is over the 10 MB submission limit")
    if len(locations) > SITEMAP_URLS:
        problems.append(f"sitemap {url} lists {len(locations)} URLs, over 50,000")
    relative = [loc for loc in locations if not loc.startswith(("http://", "https://"))]
    if relative:
        problems.append(f"sitemap {url}: {len(relative)} relative URLs, which Naver does not collect")
    foreign = {urllib.parse.urlsplit(loc).netloc for loc in locations if loc not in relative} - {host}
    if foreign:
        notes.append(f"sitemap {url} lists other hosts: {sorted(foreign)[:3]}")


def header_directives(values: list[str]) -> set[str]:
    """X-Robots-Tag directives meant for Yeti: unscoped, or after a yeti: prefix; another crawler's are left out."""
    found: set[str] = set()
    for value in values:
        scope = ""
        for part in value.lower().split(","):
            name, colon, rest = part.strip().partition(":")
            if colon and AGENT.fullmatch(name) and name not in VALUE_DIRECTIVES:
                scope, part = name, rest
            if scope in ("", "yeti"):
                found.add(part.strip())
    return found


def check_page(headers: Message | None, body: bytes, problems: list[str], notes: list[str]) -> None:
    page = Page()
    page.feed(body.decode("utf-8", "replace"))
    directives = {d.strip() for raw in page.robots for d in raw.split(",")}
    if headers:
        directives |= header_directives(headers.get_all("X-Robots-Tag") or [])
    if {"noindex", "none"} & directives:
        problems.append("noindex: the page leaves Naver's results")
    if "nofollow" in directives:
        notes.append("nofollow: Yeti collects no links from this page")
    if "nosourceinfo" in directives:
        notes.append("nosourceinfo: Naver gives no AI-written source description for this site")
    if "nosublinks" in directives:
        notes.append("nosublinks: no sublinks for this site in results")
    if len(body) >= HTML_LIMIT:
        problems.append(f"HTML is {len(body)} bytes; Naver reports pages of about 4 MB as too large")
    server = headers.get_content_charset() if headers else None
    if page.charset and server and page.charset != server.lower():
        problems.append(f"meta charset {page.charset} disagrees with the server's {server}")
    if page.verification_in_body:
        problems.append("naver-site-verification sits in <body>; ownership checks read <head> only")
    if len(page.titles) > 1:
        notes.append(f"{len(page.titles)} <title> elements")
    title = page.titles[0].strip() if page.titles else ""
    description = page.meta.get("description", "").strip()
    if not title:
        problems.append("no <title>")
    elif len(title) > TITLE_CHARS:
        notes.append(f"title is {len(title)} characters; the site check recommends 40 at most")
    if not description:
        notes.append("no meta description")
    elif len(description) > DESCRIPTION_CHARS:
        notes.append(f"description is {len(description)} characters; the site check recommends 80 at most")
    for label, text in (("title", title), ("description", description)):
        words = repeated_words(text)
        if words:
            notes.append(f"{label} repeats {', '.join(words[:3])}: repetition can cost exposure")
    if page.canonical and not page.canonical.startswith(("http://", "https://")):
        problems.append(f"relative canonical {page.canonical!r}; Naver asks for an absolute URL")
    if not page.canonical:
        notes.append("no rel=canonical")
    if "og:image" not in page.meta:
        notes.append("no og:image, which Naver can use as the thumbnail")
    if "viewport" not in page.meta:
        notes.append("no viewport meta tag")
    if page.frames:
        notes.append(f"{page.frames} frame tags: keep important content out of frames")
    if page.script_links:
        notes.append(f"{page.script_links} links exist only in JavaScript, so Yeti cannot follow them")
    if page.h1 > 1:
        notes.append(f"{page.h1} H1 elements")
    for rel, seen in page.icons.items():
        if seen > 1:
            notes.append(f"{seen} favicons with rel={rel}: keep one, or it may not show")
    if page.nosublink:
        notes.append(f"{page.nosublink} links carry rel=nosublink")


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    args: list[str] = []
    opts: dict[str, str] = {}
    words = iter(argv)
    for word in words:
        if word.startswith("--"):
            opts[word] = next(words, "")
        else:
            args.append(word)
    if len(args) != 1 or not args[0].startswith(("http://", "https://")):
        print(__doc__, file=sys.stderr)
        return 2
    try:
        parts = urllib.parse.urlsplit(args[0])
    except ValueError:
        print(__doc__, file=sys.stderr)
        return 2
    origin = f"{parts.scheme}://{parts.netloc}"
    problems: list[str] = []
    notes: list[str] = []
    target = (parts.path or "/") + (f"?{parts.query}" if parts.query else "")
    sitemaps = check_robots(origin, target, problems, notes)
    status, headers, body, error = fetch(args[0])
    print(f"status {status or error}")
    if status == 200:
        check_page(headers, body, problems, notes)
    else:
        where = headers.get("Location", "") if headers else ""
        problems.append(f"page answers {status or error}" + (f" -> {where}" if where else ""))
    if parts.scheme == "http":
        notes.append("the page is on http: Yeti prefers https, and the site should redirect to it")
    if sitemaps:
        check_sitemap(sitemaps[0], parts.netloc, problems, notes)
    key = opts.get("--key", "")
    if key:
        if not HEX_KEY.fullmatch(key):
            problems.append("IndexNow key: Naver allows 8 to 128 characters of a-f, A-F, 0-9 and hyphen")
        location = opts.get("--key-location") or f"{origin}/{key}.txt"
        status, _, body, error = fetch(location)
        if status != 200:
            problems.append(f"IndexNow key file answers {status or error}: {location}")
        elif body.decode("utf-8", "replace").strip() != key:
            problems.append(f"IndexNow key file does not hold the key: {location}")
        else:
            print(f"IndexNow key file ok: {location}")
    for note in notes:
        print("NOTE", note)
    for problem in problems:
        print("PROBLEM", problem)
    print(f"{'FAIL' if problems else 'PASS'}: {len(problems)} problems, {len(notes)} notes")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
