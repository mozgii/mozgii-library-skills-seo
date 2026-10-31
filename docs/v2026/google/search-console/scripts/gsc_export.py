#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright 2026 MOZGII, Inc. (https://mozgii.com/)
"""Export Google Search Console performance rows through the Search Analytics API, paging past 25,000 rows.

Usage:
  GSC_TOKEN is set from: gcloud auth application-default print-access-token
  python3 gsc_export.py sc-domain:example.com 2026-07-01 2026-09-30 [--dims query,page] [--type web]
                        [--country usa] [--device MOBILE] [--page-contains /blog/] [--query-regex "(?i)price"]
                        [--quota-project my-project] [--max-rows 100000] [--out rows.tsv]

The property is written as Search Console shows it: sc-domain:example.com for a domain property, or the URL
prefix with its trailing slash (https://www.example.com/). Dimensions: date, query, page, country, device,
searchAppearance (hour needs dataState hourly_all and is left out here). Types: web, image, video, news, discover,
googleNews. The token is read from the GSC_TOKEN environment variable and never printed or written to a file;
it needs the scope https://www.googleapis.com/auth/webmasters.readonly. Standard library only.
Exit 0 on success, 1 on an API or network error, 2 on usage error.
"""
from __future__ import annotations

import http.client
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://searchconsole.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query"
PAGE = 25_000
SECONDS = 120
EXIT_OK, EXIT_API, EXIT_USAGE = 0, 1, 2


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
    token = os.environ.get("GSC_TOKEN", "")
    if len(args) != 3 or not token or not opts.get("--max-rows", "100000").isdigit():
        print(__doc__, file=sys.stderr)
        return EXIT_USAGE
    site, start, end = args
    dims = [d for d in opts.get("--dims", "query,page").split(",") if d]
    filters = []
    if "--country" in opts:
        filters.append({"dimension": "country", "operator": "equals", "expression": opts["--country"]})
    if "--device" in opts:
        filters.append({"dimension": "device", "operator": "equals", "expression": opts["--device"]})
    if "--page-contains" in opts:
        filters.append({"dimension": "page", "operator": "contains", "expression": opts["--page-contains"]})
    if "--query-regex" in opts:
        filters.append({"dimension": "query", "operator": "includingRegex", "expression": opts["--query-regex"]})
    head = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    if "--quota-project" in opts:
        head["x-goog-user-project"] = opts["--quota-project"]
    url = API.format(site=urllib.parse.quote(site, safe=""))
    max_rows = int(opts.get("--max-rows", "100000"))
    rows: list[dict[str, object]] = []
    while len(rows) < max_rows:
        body = {"startDate": start, "endDate": end, "dimensions": dims, "type": opts.get("--type", "web"),
                "rowLimit": PAGE, "startRow": len(rows), "dataState": "final"}
        if filters:
            body["dimensionFilterGroups"] = [{"groupType": "and", "filters": filters}]
        payload = json.dumps(body).encode()
        req = urllib.request.Request(url, payload, head)
        try:
            with urllib.request.urlopen(req, timeout=SECONDS) as answer:
                got = json.loads(answer.read()).get("rows", [])
        except urllib.error.HTTPError as refused:
            detail = refused.read().decode("utf-8", "replace")[:500]
            print(f"API error {refused.code}: {detail}", file=sys.stderr)
            return EXIT_API
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as failed:
            print(f"network error: {getattr(failed, 'reason', failed)}", file=sys.stderr)
            return EXIT_API
        except ValueError as failed:
            print(f"the API sent something that is not JSON: {failed}", file=sys.stderr)
            return EXIT_API
        rows.extend(got)
        if len(got) < PAGE:
            break
    lines = ["\t".join(dims + ["clicks", "impressions", "ctr", "position"])]
    for r in rows[:max_rows]:
        keys = [str(k) for k in r.get("keys", [])]  # type: ignore[union-attr]
        lines.append("\t".join(keys + [str(r["clicks"]), str(r["impressions"]), f"{float(str(r['ctr'])):.4f}", f"{float(str(r['position'])):.1f}"]))
    text = "\n".join(lines) + "\n"
    if "--out" in opts:
        with open(opts["--out"], mode="w", encoding="utf-8") as out:
            out.write(text)
        print(f"{len(lines) - 1} rows written to {opts['--out']}")
    else:
        print(text, end="")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
