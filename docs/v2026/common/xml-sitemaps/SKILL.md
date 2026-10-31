---
name: xml-sitemaps
description: 'Builds, splits, validates and submits XML sitemaps (pages, images, video, news, hreflang) and notifies search engines of changes with IndexNow: limits, accurate lastmod, sitemap index files, robots.txt references, Search Console and Bing Webmaster submission, and a checker script. Use when creating or fixing a sitemap, when Search Console reports sitemap errors, when new pages are slow to be found, or when setting up IndexNow for Bing, Yandex and other engines.'
metadata:
  tags:
  - seo
  - sitemap
  - indexnow
  - crawling
  - bing
  - yandex
---

# XML sitemaps and IndexNow

An XML sitemap lists the canonical URLs a site wants crawled, with the date each last changed. It helps discovery on
large, new or poorly linked sites; it does not force indexing and does not raise rankings. IndexNow is a push
protocol that tells participating engines a URL changed, at the moment it changes.

## Step 0: read the sitemaps the site already publishes

Read what the site tells engines today before changing anything, because a generated sitemap overwrites hand edits and
an old file may still be listed.

```bash
curl -s https://www.example.com/robots.txt | grep -iE '^sitemap:'
curl -sI https://www.example.com/sitemap.xml | grep -iE '^(HTTP/|location:|content-type:)'
curl -s https://www.example.com/sitemap.xml | grep -oE '<(urlset|sitemapindex)[^>]*>'
curl -s https://www.example.com/sitemap.xml | grep -o '<loc>' | wc -l
```

The root must be `urlset` or `sitemapindex` in the namespace `http://www.sitemaps.org/schemas/sitemap/0.9`. No Sitemap
line and a 404 mean the site has none yet. Then find what writes the file (a CMS plugin, a framework route, a build
step), and read the last read date and errors in Search Console › Sitemaps and Bing Webmaster Tools › Sitemaps.

## Choose between a sitemap, IndexNow and Request indexing

A sitemap, IndexNow and Request indexing do different jobs, and most sites need the first two together.

| Need | Use | Why the others lose here |
|---|---|---|
| Every canonical URL known to every engine | XML sitemap | IndexNow carries only changes and Google does not use it; Request indexing is one URL at a time |
| Bing, Yandex, Seznam or Naver should hear of a change at once | IndexNow | a sitemap waits for the next read; Request indexing reaches Google only |
| One or a few URLs matter to Google after a fix | URL Inspection › Request indexing | a sitemap gives no single URL any priority; IndexNow does not reach Google |
| Many changed URLs and Google matters | sitemap with honest `lastmod` | Request indexing has a quota and suits only a few URLs; IndexNow does not reach Google |
| Job postings or livestream videos | Indexing API (`search-console`) | Google offers it for these short-lived pages only, where waiting for a sitemap read costs the page its value |

Request indexing promises neither a date nor inclusion: Google says a crawl can take a few days to a few weeks, and
repeating a request does not speed it up.

## What belongs in a sitemap

A sitemap holds only URLs that should be indexed. Each listed URL answers 200, carries no `noindex`, has a
self-referencing canonical and is on the sitemap's host. Leave out redirects, 404s, parameter variants, paginated
filter pages, internal search results and anything blocked by robots.txt. A sitemap full of non-canonical URLs
teaches search engines to trust it less.

## The sitemap format and its limits

The sitemap protocol (sitemaps.org) allows XML, RSS or Atom feeds, and plain text files with one URL per line.
Each file holds at most 50,000 URLs and 50 MB uncompressed; it must be UTF-8 and use absolute URLs. Larger sites
split into several files and list them in a sitemap index.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.example.com/shoes/trail-runner</loc>
    <lastmod>2026-10-14</lastmod>
  </url>
</urlset>
```

A sitemap index file lists child sitemaps (up to 50,000 per index):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://www.example.com/sitemaps/products-1.xml.gz</loc><lastmod>2026-10-27</lastmod></sitemap>
  <sitemap><loc>https://www.example.com/sitemaps/articles.xml</loc><lastmod>2026-10-25</lastmod></sitemap>
</sitemapindex>
```

## lastmod, priority and changefreq

The `lastmod` value is the only optional field Google uses, and only when it is consistently accurate. Set it to the
date of the last significant change to the main content, structured data or links, in W3C format (`2026-10-14` or
`2026-10-14T09:30:00+00:00`). Do not set it to the build time or today for every URL; a copyright-year change is not
a significant change. Google ignores `priority` and `changefreq`; Bing reads `lastmod` too and treats it as a strong
crawl signal.

## Splitting sitemaps by type

Splitting sitemaps by page type makes the Search Console Sitemaps report a diagnostic tool: indexed counts per file
show which template has the problem.

```text
/sitemap-index.xml
  /sitemaps/categories.xml
  /sitemaps/products-1.xml.gz ... products-N.xml.gz   (by ID range, so a URL stays in one file)
  /sitemaps/articles.xml
  /sitemaps/locations.xml
```

Generate sitemaps from the database of published pages, not from a crawl, so new pages appear at once and deleted
ones leave at once.

## Image, video, news and hreflang sitemaps

Sitemap extensions add images, videos, news articles and language alternates to the page entries. Google supports
the image, video and news extensions and `xhtml:link` hreflang alternates; examples and required tags are in
[references/sitemap-formats.md](references/sitemap-formats.md).

## Submitting a sitemap

A sitemap is submitted in three places, and the robots.txt line covers every engine at once.

1. Add a line to robots.txt: `Sitemap: https://www.example.com/sitemap-index.xml` (any number of lines allowed).
2. Search Console › Sitemaps › Add a new sitemap (or the Search Console API `sitemaps.submit`).
3. Bing Webmaster Tools › Sitemaps › Submit sitemap; Yandex Webmaster › Indexing › Sitemap files.

Google retired its sitemap ping endpoint in 2023; requests to it do nothing. Resubmit only when the index URL changes.

## Verify

The sitemap check script reads sitemaps through robots.txt (or a given URL), recurses into index files and gzip,
checks the root element and namespace, limits, hosts and lastmod values, flags a file that lists nothing, and samples
listed URLs for status, `noindex` and canonical:

```bash
python3 scripts/sitemap_check.py https://www.example.com/
python3 scripts/sitemap_check.py https://www.example.com/sitemaps/products-1.xml.gz --sample 100 --tsv urls.tsv
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

Exit 0 means no problem found; each `PROBLEM` line names the file or URL.

## IndexNow for instant change notification

To ping Bing and Yandex the moment you publish or change a page, use IndexNow. IndexNow lets a site notify participating engines (Microsoft Bing, Yandex, Seznam.cz, Naver and others listed at
indexnow.org) when a URL is added, changed or deleted; one submission is shared with all of them. Google does not
use IndexNow. Set it up in three steps:

1. Generate a key of 8–128 characters (`a-z`, `A-Z`, `0-9`, `-`): `python3 -c "import uuid; print(uuid.uuid4().hex)"`.
2. Host it as `https://www.example.com/<key>.txt` containing the key.
3. Submit changed URLs from the publishing code:

```bash
curl -s -o /dev/null -w '%{http_code}\n' "https://api.indexnow.org/indexnow?url=https://www.example.com/shoes/trail-runner&key=$INDEXNOW_KEY"

curl -s -X POST https://api.indexnow.org/indexnow -H 'Content-Type: application/json; charset=utf-8' -d '{
  "host": "www.example.com",
  "key": "'"$INDEXNOW_KEY"'",
  "urlList": ["https://www.example.com/shoes/trail-runner", "https://www.example.com/shoes/"]
}'
```

Responses: 200 received, 202 received and key validation pending, 400 bad format, 403 key not found, 422 URLs not on
the host, 429 too many requests. A POST takes up to 10,000 URLs. Submit only real changes; IndexNow complements
sitemaps, it does not replace them.

## Worked example: a sitemap with 60% "Submitted URL not indexed"

Situation: a 90,000-URL sitemap shows 54,000 submitted and not indexed.

`sitemap_check.py --sample 200` finds 31% of sampled URLs redirect (old product URLs), 12% canonicalise to another
URL (colour variants), and every `lastmod` equals the build time. Fix: generate the sitemap from published canonical
product and category records only; take `lastmod` from the record's content update time; split into categories,
products by ID range and articles. Check: the Sitemaps report per file after recrawl; the products files show which
template still has a gap.

## Checklist for sitemaps

The sitemap checklist confirms the file helps instead of misleading.

1. Every listed URL answers 200, is indexable and self-canonical (`sitemap_check.py` sample passes).
2. Files under 50,000 URLs and 50 MB; an index when there are several.
3. `lastmod` is the real change date, not the build date.
4. Referenced in robots.txt and submitted in Search Console and Bing Webmaster Tools.
5. Search Console Sitemaps report: status Success, recent read date, indexed count close to submitted count.
6. IndexNow sends changed URLs on publish, update and delete (if Bing or Yandex traffic matters).

## Gotchas with sitemaps

The gotchas below are the common reasons a sitemap is ignored or harmful.

1. **Every lastmod is today.** Symptom: Google stops using the dates and the checker warns. Cause: the generator
   stamps the build time, so search engines stop trusting the field. Fix: store the content's real modified date.
2. **Sitemap lists redirected URLs.** Symptom: the Page indexing report shows "Page with redirect" for sitemap URLs
   after a migration. Cause: the old list was kept. Fix: list new URLs only; keep the old sitemap briefly only to
   speed up the discovery of redirects.
3. **A sitemap in a subfolder.** Symptom: URLs outside that folder are reported as not allowed. Cause: a sitemap
   covers only its folder and below, unless submitted in Search Console. Fix: host sitemaps at the root.
4. **Cached sitemap at the CDN.** Symptom: new pages stay missing from the file for days. Cause: the CDN serves a
   stale list. Fix: set a short cache lifetime for sitemap files.
5. **"Couldn't fetch" in Search Console.** Symptom: the file is valid in a browser and fails in the report. Cause:
   often a WAF or bot rule blocking Googlebot, or a slow generator timing out. Fix: allow Googlebot and serve sitemaps
   as static files.

## Anti-patterns in sitemaps

Anti-patterns with sitemaps treat the file as a dump of every URL and not a list of what should rank.

| Do not | Do this instead |
|---|---|
| Generating a sitemap from a crawl | generate it from the database of published pages |
| Listing parameter variants and filter pages | list canonical, indexable URLs only |
| Setting `priority` and `changefreq` carefully | skip them, because Google ignores both |
| Pinging Google's old endpoint | add the file to robots.txt and Search Console, because the ping was retired in 2023 |
| Submitting every URL through IndexNow on a schedule | submit only real changes, alongside the sitemap |

## References for sitemaps

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/sitemap-formats.md](references/sitemap-formats.md): image, video, news and hreflang sitemap examples.
- `scripts/sitemap_check.py`: the sitemap and listed-URL checker.

## See also for sitemaps

- `crawling-and-indexing`: discovery
- `search-console`: Page indexing reasons and the Indexing API
- `canonical-urls`: which URL belongs in a sitemap
- `international-seo`: hreflang in sitemaps
- `news-and-discover-seo`: news sitemaps
- `site-migrations`: sitemaps through a move
- `bing-seo`, `naver-search-advisor`: engine-specific submission limits and IndexNow rules
