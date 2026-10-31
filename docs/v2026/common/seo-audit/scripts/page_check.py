#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright 2026 MOZGII, Inc. (https://mozgii.com/)
"""Fetch one URL the way a crawler does and print its SEO facts as JSON.

Usage:
  python3 page_check.py https://example.com/page [--ua googlebot|bingbot|browser] [--max-hops 10]

Reports: every redirect hop with its status, the final status, X-Robots-Tag, meta robots, canonical, title and
description with lengths, H1 and H2 headings, html lang, hreflang alternates, JSON-LD @types, Open Graph tags,
images without alt, internal and external link counts, the word count of the visible text, and the HTML size
(Googlebot reads only the first 2 MB, uncompressed).
Uses only the Python standard library (3.9+). Exit 0 when the final status is 200, 1 otherwise, 2 on usage error.
The HTML is what the server returns; text that appears only after JavaScript runs is not seen here.
"""
from __future__ import annotations

import gzip
import http.client
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import zlib
from email.message import Message
from html.parser import HTMLParser

WEBKIT = "AppleWebKit/537.36 (KHTML, like Gecko)"
GOOGLEBOT_PAGE = "http://www.google.com/bot.html"
AGENTS = {
    "googlebot": f"Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) {WEBKIT} "
    f"Chrome/126.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +{GOOGLEBOT_PAGE})",
    "bingbot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "browser": f"Mozilla/5.0 (X11; Linux x86_64) {WEBKIT} Chrome/126.0 Safari/537.36",
}
MAX_BYTES = 5_000_000


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *_hop):  # noqa: ANN002, ANN201
        return None


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta: dict[str, str] = {}
        self.og: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.headings: list[tuple[str, str]] = []
        self.lang = ""
        self.jsonld: list[str] = []
        self.images_no_alt = 0
        self.images = 0
        self.anchors: list[str] = []
        self.text: list[str] = []
        self._stack: list[str] = []
        self._buf: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or a.get("http-equiv") or "").lower()
            if key.startswith("og:"):
                self.og[key] = a.get("content", "")
            elif key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            self.links.append(a)
        elif tag == "img":
            self.images += 1
            if "alt" not in a:
                self.images_no_alt += 1
        elif tag == "a" and a.get("href"):
            self.anchors.append(a["href"])
        if tag in ("script", "style", "noscript", "template"):
            self._skip += 1
        if tag in ("title", "h1", "h2", "h3") or (tag == "script" and a.get("type", "").lower() == "application/ld+json"):
            self._stack.append("jsonld" if tag == "script" else tag)
            self._buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "noscript", "template") and self._skip:
            self._skip -= 1
        if not self._stack:
            return
        top = self._stack[-1]
        if (top == "jsonld" and tag == "script") or top == tag:
            self._stack.pop()
            text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            if top == "title" and not self.title:
                self.title = text
            elif top == "jsonld":
                self.jsonld.append("".join(self._buf))
            elif top in ("h1", "h2", "h3"):
                self.headings.append((top, text))

    def handle_data(self, data: str) -> None:
        if self._stack:
            self._buf.append(data)
        if not self._skip:
            self.text.append(data)


def ld_types(blocks: list[str]) -> list[str]:
    found: list[str] = []
    for raw in blocks:
        try:
            pending = [json.loads(raw)]
        except json.JSONDecodeError:
            found.append("INVALID_JSON")
            continue
        while pending:
            node = pending.pop()
            if isinstance(node, list):
                pending.extend(node)
            elif isinstance(node, dict):
                kinds = node.get("@type", [])
                found.extend([kinds] if isinstance(kinds, str) else [str(k) for k in kinds] if isinstance(kinds, list) else [])
                pending.extend(node.values())
    return sorted(set(found))


def header_map(message: Message) -> dict[str, str]:
    """Lowercase names; every X-Robots-Tag header is kept, because a site may send several."""
    found = {name.lower(): value for name, value in message.items()}
    robots = message.get_all("X-Robots-Tag")
    if robots:
        found["x-robots-tag"] = ", ".join(robots)
    return found


def fetch(url: str, ua: str) -> tuple[int, dict[str, str], bytes]:
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "gzip, deflate", "Accept": "text/html,*/*"})
    try:
        with opener.open(req, timeout=30) as res:
            status, headers, body = res.status, header_map(res.headers), res.read(MAX_BYTES)
    except urllib.error.HTTPError as e:
        status, headers, body = e.code, header_map(e.headers), e.read(MAX_BYTES)
    enc = headers.get("content-encoding", "")
    if enc == "gzip":
        body = gzip.decompress(body)
    elif enc == "deflate":
        body = zlib.decompress(body)
    return status, headers, body


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
    if len(args) < 1 or not args[0].startswith(("http://", "https://")):
        print(__doc__, file=sys.stderr)
        return 2
    ua_name = opts.get("--ua", "googlebot")
    hop_limit = opts.get("--max-hops", "10")
    if ua_name not in AGENTS or not hop_limit.isdecimal():
        print(__doc__, file=sys.stderr)
        return 2
    ua = AGENTS[ua_name]
    max_hops = int(hop_limit)
    url = args[0]
    hops: list[dict[str, object]] = []
    try:
        for _ in range(max_hops + 1):
            status, headers, body = fetch(url, ua)
            hops.append({"url": url, "status": status})
            if status in (301, 302, 303, 307, 308) and headers.get("location"):
                url = urllib.parse.urljoin(url, headers["location"])
                continue
            break
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException) as e:
        print(json.dumps({"url": url, "error": str(e), "hops": hops}, ensure_ascii=False, indent=1))
        return 1
    charset = re.search(r"charset=([\w-]+)", headers.get("content-type", ""))
    try:
        html = body.decode(charset.group(1) if charset else "utf-8", errors="replace")
    except LookupError:
        html = body.decode("utf-8", errors="replace")
    page = Page()
    page.feed(html)
    canonicals = [ln.get("href", "") for ln in page.links if "canonical" in ln.get("rel", "").lower().split()]
    hreflang = {ln.get("hreflang", ""): ln.get("href", "") for ln in page.links if ln.get("hreflang")}
    host = urllib.parse.urlsplit(url).netloc
    internal = sum(1 for h in page.anchors if urllib.parse.urlsplit(urllib.parse.urljoin(url, h)).netloc == host)
    desc = page.meta.get("description", "")
    words = len(re.findall(r"\w+", " ".join(page.text)))
    report = {
        "final_url": url,
        "status": status,
        "hops": hops,
        "redirect_hops": len(hops) - 1,
        "x_robots_tag": headers.get("x-robots-tag", ""),
        "meta_robots": page.meta.get("robots", ""),
        "meta_googlebot": page.meta.get("googlebot", ""),
        "canonical": canonicals,
        "canonical_is_self": bool(canonicals) and urllib.parse.urljoin(url, canonicals[0]) == url,
        "title": page.title,
        "title_chars": len(page.title),
        "description": desc,
        "description_chars": len(desc),
        "h1": [t for h, t in page.headings if h == "h1"],
        "h2": [t for h, t in page.headings if h == "h2"],
        "html_lang": page.lang,
        "hreflang": hreflang,
        "jsonld_types": ld_types(page.jsonld),
        "open_graph": page.og,
        "images": page.images,
        "images_without_alt": page.images_no_alt,
        "links_internal": internal,
        "links_external": len(page.anchors) - internal,
        "words": words,
        "html_bytes": len(body),
        "over_googlebot_2mb": len(body) > 2 * 1024 * 1024,
    }
    print(json.dumps(report, indent=1, ensure_ascii=False))
    return 0 if status == 200 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
