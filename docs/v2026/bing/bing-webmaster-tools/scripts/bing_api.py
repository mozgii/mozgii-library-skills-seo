#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright 2026 MOZGII, Inc. (https://mozgii.com/)
"""Read a site's Bing Webmaster data and submit URLs through the REST (JSON) API.

Usage:
  export BING_WEBMASTER_KEY=...        # or BING_WEBMASTER_TOKEN=... for an OAuth access token
  python3 bing_api.py sites
  python3 bing_api.py quota https://www.example.com/
  python3 bing_api.py queries https://www.example.com/ [--top 50] [--out queries.tsv]
  python3 bing_api.py pages https://www.example.com/ [--top 50] [--out pages.tsv]
  python3 bing_api.py crawl https://www.example.com/ [--out crawl.tsv]
  python3 bing_api.py submit https://www.example.com/ https://www.example.com/a https://www.example.com/b
  python3 bing_api.py submit https://www.example.com/ --file urls.txt

Microsoft refreshes queries and pages weekly and crawl daily. submit reads the daily quota first, sends 500
URLs a batch, and refuses URLs on another host. The key or token comes only from the environment and is never printed;
a key travels in the URL's query string, so this script never prints a request URL. Standard library only (Python 3.9+).
Exit 0 on success, 1 on an API or network error, 2 on usage error.
"""
from __future__ import annotations

import datetime as dt
import http.client
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

KEY_HOST, TOKEN_HOST = "https://ssl.bing.com", "https://www.bing.com"
JSON_PATH = "/webmaster/api.svc/json/"
JSON_TYPE = "application/json; charset=utf-8"
NETWORK_ERRORS = (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException)
BATCH = 500
TICKS = re.compile(r"/Date\((-?\d+)[+-]\d{4}\)/|/Date\((-?\d+)\)/")
EXIT_OK, EXIT_API, EXIT_USAGE = 0, 1, 2
QUERY_COLUMNS = ["Date", "Query", "Clicks", "Impressions", "AvgClickPosition", "AvgImpressionPosition"]
CRAWL_COLUMNS = ["Date", "CrawledPages", "CrawlErrors", "InIndex", "InLinks", "BlockedByRobotsTxt", "Code2xx", "Code301",
                 "Code302", "Code4xx", "Code5xx", "AllOtherCodes", "ContainsMalware"]


class ApiError(Exception):
    pass


def call(method: str, params: dict[str, str] | None = None, payload: dict[str, object] | None = None) -> object:
    key, token = os.environ.get("BING_WEBMASTER_KEY", ""), os.environ.get("BING_WEBMASTER_TOKEN", "")
    query = dict(params or {})
    head = {"Content-Type": JSON_TYPE}
    if token:
        head["Authorization"] = f"Bearer {token}"
        base = TOKEN_HOST
    else:
        query["apikey"] = key
        base = KEY_HOST
    url = f"{base}{JSON_PATH}{method}?{urllib.parse.urlencode(query)}"
    data = json.dumps(payload).encode() if payload is not None else None
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data, head), timeout=60) as answer:
            return json.loads(answer.read()).get("d")
    except urllib.error.HTTPError as refused:
        raise ApiError(f"{method}: HTTP {refused.code}: {fault_text(refused.read())}") from None
    except NETWORK_ERRORS as failed:
        raise ApiError(f"{method}: network error: {type(failed).__name__}") from None
    except ValueError:
        raise ApiError(f"{method}: the API sent something that is not JSON") from None


def fault_text(raw: bytes) -> str:
    """Only the API's own ErrorCode and Message: other text could echo the request."""
    try:
        fault = json.loads(raw)
    except ValueError:
        return "no details"
    if isinstance(fault, dict) and "ErrorCode" in fault:
        return f"ErrorCode {fault['ErrorCode']}: {str(fault.get('Message', ''))[:200]}"
    return "no details"


def plain_date(value: object) -> str:
    found = TICKS.fullmatch(str(value).replace("\\", ""))
    if not found:
        return str(value)
    millis = int(found.group(1) or found.group(2))
    return dt.datetime.fromtimestamp(millis / 1000, dt.timezone.utc).date().isoformat()


def as_table(rows: object, columns: list[str]) -> list[list[str]]:
    table = []
    for row in rows if isinstance(rows, list) else []:
        table.append([plain_date(row.get(c)) if c == "Date" else str(row.get(c, "")) for c in columns])
    return table


def emit(columns: list[str], table: list[list[str]], out: str) -> None:
    text = "\t".join(columns) + "\n" + "".join("\t".join(row) + "\n" for row in table)
    if out:
        Path(out).write_text(text, encoding="utf-8")
        print(f"{len(table)} rows written to {out}")
    else:
        print(text, end="")


def clicks_of(row: list[str]) -> int:
    return int(row[2]) if row[2].isdigit() else 0


def submit(site: str, urls: list[str]) -> int:
    host = urllib.parse.urlsplit(site).netloc
    strangers = [u for u in urls if urllib.parse.urlsplit(u).netloc != host]
    if strangers or not urls:
        print(f"refused: {len(strangers)} URLs are not on {host}" if strangers else "no URLs given", file=sys.stderr)
        return EXIT_USAGE
    quota = call("GetUrlSubmissionQuota", {"siteUrl": site})
    daily = quota.get("DailyQuota", 0) if isinstance(quota, dict) else 0
    print(f"daily quota left: {daily}")
    if len(urls) > daily:
        print(f"refused: {len(urls)} URLs, {daily} left today; quotas reset at midnight UTC", file=sys.stderr)
        return EXIT_API
    for start in range(0, len(urls), BATCH):
        chunk = urls[start:start + BATCH]
        call("SubmitUrlBatch", payload={"siteUrl": site, "urlList": chunk})
        print(f"submitted {start + len(chunk)} of {len(urls)}")
    return EXIT_OK


def run(args: list[str], opts: dict[str, str]) -> int:
    command, site = args[0], args[1] if len(args) > 1 else ""
    out = opts.get("--out", "")
    if command == "sites":
        sites = call("GetUserSites")
        for entry in sites if isinstance(sites, list) else []:
            print(f"{entry.get('Url', '')}\tverified={entry.get('IsVerified', '')}")
    elif command == "quota":
        quota = call("GetUrlSubmissionQuota", {"siteUrl": site})
        if isinstance(quota, dict):
            print(f"daily {quota.get('DailyQuota')}\tmonthly {quota.get('MonthlyQuota')}")
    elif command in ("queries", "pages"):
        method = "GetQueryStats" if command == "queries" else "GetPageStats"
        table = as_table(call(method, {"siteUrl": site}), QUERY_COLUMNS)
        table.sort(key=clicks_of, reverse=True)
        emit(QUERY_COLUMNS, table[:int(opts.get("--top", "50"))], out)
    elif command == "crawl":
        emit(CRAWL_COLUMNS, as_table(call("GetCrawlStats", {"siteUrl": site}), CRAWL_COLUMNS), out)
    else:
        urls = args[2:]
        if "--file" in opts:
            urls += Path(opts["--file"]).read_text(encoding="utf-8").split()
        return submit(site, urls)
    return EXIT_OK


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return EXIT_OK
    args: list[str] = []
    opts: dict[str, str] = {}
    words = iter(argv)
    for word in words:
        if word.startswith("--"):
            opts[word] = next(words, "")
        else:
            args.append(word)
    known = ("sites", "quota", "queries", "pages", "crawl", "submit")
    usable = args and args[0] in known and (args[0] == "sites" or len(args) > 1) and opts.get("--top", "1").isdigit()
    if not usable or not (os.environ.get("BING_WEBMASTER_KEY") or os.environ.get("BING_WEBMASTER_TOKEN")):
        print(__doc__, file=sys.stderr)
        return EXIT_USAGE
    code = EXIT_USAGE
    try:
        code = run(args, opts)
    except ApiError as failed:
        print(failed, file=sys.stderr)
        code = EXIT_API
    except OSError as failed:
        print(f"cannot use the file: {failed}", file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
