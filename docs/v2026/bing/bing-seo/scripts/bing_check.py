#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright 2026 MOZGII, Inc. (https://mozgii.com/)
"""Check one page the way Bing reads it, without an account.

Usage:
  python3 bing_check.py https://example.com/page
  python3 bing_check.py https://example.com/page --key 0123456789abcdef [--key-location https://example.com/k.txt]

Reports PROBLEM for what keeps the page out of Bing or Copilot (blocked in robots.txt, noindex, a non-200 status, a
missing title, an IndexNow key file that fails) and NOTE for what limits it or needs a decision (noarchive and nocache
with the 1 March 2027 deadline, nosnippet, AI Training and AI Grounding preferences, crawl-delay, no Sitemap line, a
page with almost no text in its HTML). Standard library only (Python 3.9+).
Exit 0 when there is no PROBLEM (NOTE lines allowed), 1 when there is one, 2 on usage error.
"""
from __future__ import annotations

import http.client
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from email.message import Message
from html.parser import HTMLParser

BINGBOT = "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
MAX_BYTES = 3_000_000
FETCH_ERRORS = (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException)
THIN_TEXT = 200
KEY_SHAPE = re.compile(r"[A-Za-z0-9-]{8,128}")


class KeepRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *_hop):  # noqa: ANN002, ANN201
        return None


class Page(HTMLParser):
    """Collects the head tags and the visible text a crawler gets without running scripts."""

    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.robots: list[str] = []
        self.description = ""
        self.h1 = 0
        self.text = 0
        self.stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        fields = {name.lower(): (value or "") for name, value in attrs}
        if tag in ("script", "style", "title", "noscript"):
            self.stack.append(tag)
        if tag == "h1":
            self.h1 += 1
        if tag == "meta":
            name = fields.get("name", "").lower()
            if name in ("robots", "bingbot"):
                self.robots.append(fields.get("content", ""))
            if name == "description":
                self.description = fields.get("content", "")

    def handle_endtag(self, tag: str) -> None:
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        if "title" in self.stack:
            self.title += data
        elif not self.stack:
            self.text += len(data.strip())


def fetch(url: str) -> tuple[int, Message | None, bytes, str]:
    opener = urllib.request.build_opener(KeepRedirects)
    try:
        request = urllib.request.Request(url, headers={"User-Agent": BINGBOT})
        with opener.open(request, timeout=30) as answer:
            return answer.status, answer.headers, answer.read(MAX_BYTES), ""
    except urllib.error.HTTPError as refused:
        return refused.code, refused.headers, b"", ""
    except FETCH_ERRORS as failed:
        return 0, None, b"", str(getattr(failed, "reason", failed))


def groups_of(robots: str) -> dict[str, list[tuple[str, str]]]:
    """robots.txt as {lowercased agent: [(allow or disallow, path)]}; a run of User-agent lines shares its rules."""
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
    return groups


def applies(rule: str, target: str) -> bool:
    regex = ".*".join(re.escape(piece) for piece in rule.rstrip("$").split("*"))
    return re.match(regex + ("$" if rule.endswith("$") else ""), target) is not None


def blocked(groups: dict[str, list[tuple[str, str]]], path: str) -> bool:
    """RFC 9309: the longest matching rule wins, and allow wins a tie."""
    rules = groups.get("bingbot", groups.get("*", []))
    best, verdict = -1, False
    for kind, pattern in rules:
        if pattern and applies(pattern, path) and (len(pattern) > best or (len(pattern) == best and kind == "allow")):
            best, verdict = len(pattern), kind == "disallow"
    return verdict


def robots_lines(raw: str) -> list[str]:
    return [line.strip() for line in raw.split(",") if line.strip()]


def directive_notes(directives: list[str]) -> tuple[list[str], list[str]]:
    problems, notes = [], []
    lowered = [d.lower().replace(" ", "") for d in directives]
    if "noindex" in lowered or "none" in lowered:
        problems.append("noindex: the page cannot appear in Bing, Copilot or grounding results")
    old = sorted({d for d in lowered if d in ("noarchive", "nocache")})
    if old:
        notes.append(f"{', '.join(old)}: not read for training or grounding after 1 March 2027; publish the new preferences")
    if "nosnippet" in lowered or "max-snippet:0" in lowered:
        notes.append("no snippet allowed: Bing shows no caption, and Copilot citations can suffer")
    for value in lowered:
        if value.startswith(("ai-training:", "ai-grounding:")):
            notes.append(f"AI preference on this page: {value}")
    return problems, notes


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
    url = args[0]
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        print(__doc__, file=sys.stderr)
        return 2
    origin = f"{parts.scheme}://{parts.netloc}"
    problems: list[str] = []
    notes: list[str] = []

    status, _, body, error = fetch(f"{origin}/robots.txt")
    if status == 200:
        robots = body.decode("utf-8", "replace")
        groups = groups_of(robots)
        target = parts.path or "/"
        if blocked(groups, target + (f"?{parts.query}" if parts.query else "")):
            problems.append(f"robots.txt blocks bingbot from {target}")
        delay = re.search(r"(?im)^\s*crawl-delay:\s*(\S+)", robots)
        if delay:
            notes.append(f"crawl-delay {delay.group(1)} in robots.txt overrides the Crawl control setting")
        if "__usage_ai-training" in groups:
            notes.append(f"robots.txt sets AI Training rules: {groups['__usage_ai-training']}")
        if not re.search(r"(?im)^\s*sitemap:", robots):
            notes.append("robots.txt has no Sitemap line")
    elif status >= 500 or status == 0:
        problems.append(f"robots.txt did not answer ({status or error})")

    status, headers, body, error = fetch(url)
    print(f"status {status or error}")
    if status != 200:
        where = headers.get("Location", "") if headers else ""
        problems.append(f"page answers {status or error}" + (f" -> {where}" if where else ""))
    directives: list[str] = []
    if headers:
        for raw in headers.get_all("X-Robots-Tag") or []:
            scope, _, rest = raw.partition(":")
            if scope.strip().lower() == "bingbot":
                directives.extend(robots_lines(rest))
            elif scope.strip().lower() in ("otherbot", "googlebot"):
                continue
            else:
                directives.extend(robots_lines(raw))
    page = Page()
    page.feed(body.decode("utf-8", "replace"))
    for raw in page.robots:
        directives.extend(robots_lines(raw))
    found_problems, found_notes = directive_notes(directives)
    problems.extend(found_problems)
    notes.extend(found_notes)
    if status == 200:
        title = page.title.strip()
        if not title:
            problems.append("no <title>")
        elif len(title) < 10:
            notes.append(f"short title ({len(title)} characters)")
        if not page.description.strip():
            notes.append("no meta description")
        if page.h1 != 1:
            notes.append(f"{page.h1} H1 headings")
        if page.text < THIN_TEXT:
            notes.append(f"only {page.text} characters of text in the HTML: check that the content is not client-side only")

    key = opts.get("--key", "")
    if key:
        if not KEY_SHAPE.fullmatch(key):
            problems.append("IndexNow key: 8 to 128 characters of a-z, A-Z, 0-9 and hyphen")
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
