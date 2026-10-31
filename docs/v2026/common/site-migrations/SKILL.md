---
name: site-migrations
description: 'Plans, runs and verifies a site migration without losing search traffic: domain changes, HTTP to HTTPS, URL restructures, CMS or platform changes, merges of sites or sections, and redesigns. Covers the URL inventory, the one-to-one redirect map, pre-launch checks on staging, launch-day steps, Change of Address, monitoring, rollback criteria and a redirect checker script. Use when a site is moving domain, platform or URL structure, when a redesign changes URLs, or when traffic dropped after a migration.'
metadata:
  tags:
  - seo
  - migration
  - redirects
  - domain-change
  - https
  - replatforming
---

# Site migrations without traffic loss

A site migration is any change to URLs, hosts, platform or templates that search engines must relearn. Done well,
traffic dips for a few weeks and recovers; done badly, it falls for months. The difference is almost always the
redirect map and what was checked before launch.

## Step 0: read how the site answers before the move

Read the current hosts, redirects and platform first, because an older migration's redirects and a forgotten host are what a
new map most often breaks. The loop follows all four host variants, and the next lines read the sitemap entries and the
server.

```bash
for u in http://example.com/ http://www.example.com/ https://example.com/ https://www.example.com/; do
  curl -sIL -o /dev/null -w "$u -> %{url_effective} %{http_code} (%{num_redirects} hops)\n" "$u"
done
curl -s https://example.com/robots.txt | grep -iE '^(disallow|sitemap):'
curl -sIL https://example.com/ | grep -iE '^(server:|x-powered-by:)'
python3 --version                                     # redirect_check.py needs 3.9 or later
```

Then note the platform before and after, who controls DNS and the redirect rules, which Search Console and Bing Webmaster
Tools properties are verified, and any earlier move whose redirects must survive this one.

## Types of migration and their risk

Migration types differ in how much search engines must relearn, so the plan scales with the type.

| Type | Example | Risk | Change of Address in Search Console |
|---|---|---|---|
| Protocol | http to https | low | no |
| Host | example.com to www.example.com | low | no |
| Domain | old-example.com to example.com | medium | yes |
| URL structure | `/p/123` to `/shoes/trail-runner` | medium to high | no |
| Platform or CMS | one e-commerce platform to another | high: URLs, templates, rendering change at once | only if the domain changes |
| Merge | two sites into one | high | yes, for the retired domain |
| Redesign on same URLs | new templates | medium: content, links and speed change | no |

Change as few things at once as the business allows. A domain change plus new URLs plus new templates makes any
drop impossible to diagnose.

## Migration plan

To prepare a move to a new domain or new URLs, work through the migration plan: six phases, starting weeks
before the move. The migration plan has six phases; each ends with a check that must pass before the next starts.

### 1. Benchmark the old site

The benchmark records the starting point to compare against later. Export from Search Console 16 months of clicks
and impressions by page and by query; organic sessions and conversions by landing page from analytics; a full crawl;
the indexed page count; the top linked pages (Search Console Links report or a backlink tool); Core Web Vitals per
template.

### 2. Build the URL inventory

The URL inventory lists every old URL that has value. Combine: the crawl, all XML sitemaps, analytics landing pages
(13+ months), Search Console pages with impressions, backlink targets, server log URLs Googlebot requests, and
images, PDFs and other files. Deduplicate and keep the source of each URL.

### 3. Write the redirect map

The redirect map assigns each old URL one new URL, or marks it gone. Rules:

- Map one to one to the most equivalent page: product to product, article to article.
- Merge only true duplicates into one page.
- Content that has no equivalent and no value: 404 or 410. Redirecting it to the home page is a soft 404.
- Redirect in one hop with 301 or 308; update old redirects so they point at final URLs too (no chains from earlier
  migrations).
- Write the map as a CSV of absolute URLs, `old_url,new_url`, with `gone` for removed pages; it doubles as the test
  file. `redirect_check.py` requests each URL, so it exits 2 on a map of relative paths: add the scheme and host first
  (`https://old.example.com/shoes,https://www.example.com/footwear/`).

Pattern rules cover most URLs; the money pages are mapped and reviewed by hand.

```nginx
# pattern: /p/<id>-<slug> -> /shoes/<slug>
rewrite ^/p/[0-9]+-([a-z0-9-]+)$ /shoes/$1 permanent;
# explicit map for pages whose slug changed, from the CSV (the map block goes in the http context;
# redirects.map holds lines like: /old-page /new-page/;)
map $request_uri $new_uri { include /etc/nginx/redirects.map; }
# inside the server block:
if ($new_uri) { return 301 $new_uri; }
```

### 4. Prepare and test on staging

Staging tests the new site as search engines will see it, behind authentication so it is not indexed.

- Crawl staging: status codes, canonicals (to production URLs), titles, H1, structured data, hreflang, internal
  links to final URLs, no `noindex` meant for production.
- Compare templates with the old site: main content, headings, internal links and structured data kept or improved.
- Test the redirect map against staging (`--delay` keeps the load low):

```bash
python3 scripts/redirect_check.py redirect-map.csv --delay 0.1 --out results.tsv
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

- Prepare the production robots.txt and sitemaps of new URLs; remove staging-only blocks.
- Check rendering with URL Inspection on a temporarily open staging URL, or with the Rich Results Test.

### 5. Launch

Launch day follows a fixed order, at a low-traffic time, with developers available for at least two days after.

1. Deploy the new site and turn on the redirects together.
2. Run `redirect_check.py` on the full map against production; fix every non-PASS row.
3. Confirm robots.txt allows crawling and production pages carry no `noindex`.
4. Submit the new sitemaps; keep the old sitemap for a few weeks so redirects are discovered.
5. Domain changes: Search Console › Settings › Change of Address on the old property, for every verified variant of
   the old domain (subdomains and www or bare versions, even ones no longer used);
   Bing Webmaster Tools › Site Move.
6. Update the important external links you control: profiles, business listings, ad campaigns, email templates.

### 6. Monitor and fix

Monitoring after launch compares daily against the benchmark for at least eight weeks.

- Search Console on both properties: Page indexing (old URLs moving to "Page with redirect", new URLs indexed),
  Crawl stats (crawl rate rises at first; errors should not), Performance by page.
- Server logs and 404 reports: new 404s from old URLs missing from the map; add them.
- Analytics: organic landings and conversions by template against the benchmark.

## Expected traffic after a migration

Traffic after a migration follows a known pattern. Google's guidance says a medium-sized site can take a few weeks
for most pages to move in the index, longer for large sites, with fluctuations meanwhile. A drop of 10–20% for a few
weeks on a domain or platform change is common; a drop over 30% after four weeks, or one concentrated on a template,
points to a fault in that template or its redirects.

## How long to keep redirects

Redirects stay for at least one year, and in practice for as long as anyone may follow an old link. Keep the old
domain registered and renewing; a lapsed domain loses every redirect and can be bought by someone else.

## Rollback criteria

Rollback criteria are agreed before launch, so the decision is not made in a panic. Typical triggers: the site
cannot serve redirects or new pages reliably; a sitewide `noindex` or robots block shipped and cannot be fixed in an
hour; conversions down more than an agreed share for several days with a cause that cannot be fixed forward.

## Worked example: moving a shop from /p/123 URLs to readable URLs

Situation: 18,000 product URLs `/p/123` move to `/shoes/trail-runner-x`, same domain, new templates.

Inventory: the crawl (17,400), sitemaps (18,000), Search Console pages with impressions (9,800), backlink targets
(1,150), log URLs (21,000 incl. old campaign URLs): 22,600 unique. Map: a rule from the product ID to the new slug
covers 17,900; 300 discontinued products with links go to their category, 4,400 with no value are `gone` (410).
Staging: `redirect_check.py` 100% PASS; templates keep the reviews block and breadcrumbs. Launch on a Tuesday
morning; first hour: robots.txt and `noindex` checked, full map re-run on production. Week four: clicks at 92% of
the benchmark, Page indexing shows old URLs as "Page with redirect"; 140 new 404s from old email links added to the
map.

## Verify

Verify a migration on production, in this order. The redirect check comes first and passes only with no non-PASS row:

```bash
python3 scripts/redirect_check.py redirect-map.csv --delay 0.1 --out results.tsv     # expect exit 0
awk -F'\t' 'NR > 1 && $1 != "PASS"' results.tsv                                      # expect no row
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

Then confirm that crawlers can read the new site. Run the `noindex` commands on one URL per template:

```bash
curl -s https://www.example.com/robots.txt | grep -iE '^disallow:[[:space:]]*/[[:space:]]*$'    # expect nothing
curl -sI https://www.example.com/ | grep -iE '^x-robots-tag:.*noindex'                          # expect nothing
curl -sL https://www.example.com/ | grep -ioE '<meta[^>]+noindex[^>]*>'                         # expect nothing
```

Finish in Search Console: over the following weeks, Page indexing on the old property moves the old URLs to "Page with
redirect", and the new URLs show as indexed.

## Checklist for a migration

The migration checklist is the minimum; skipping any item is a decision the owner signs.

1. Benchmark exported (Search Console, analytics, crawl, links, Core Web Vitals).
2. URL inventory from at least crawl, sitemaps, analytics, Search Console and backlinks.
3. Redirect map one to one; no home-page dumping; no chains; `gone` for removed pages.
4. Staging crawled and compared; content, titles, links and structured data kept.
5. `redirect_check.py` passes on production for every row.
6. robots.txt and `noindex` checked on production within the first hour.
7. New sitemaps submitted; Change of Address done for a domain change.
8. Daily monitoring for eight weeks; 404s from old URLs added to the map.

## Gotchas in migrations

The gotchas below are the causes behind most failed migrations.

1. **Redirecting everything to the home page.** Symptom: old URLs show as Soft 404 and their rankings are lost. Cause:
   mass redirects to one page are treated as soft 404s. Fix: map each old URL to its closest equivalent, or return 404
   or 410.
2. **Chains from earlier migrations.** Symptom: `http://old/a` to `https://old/a` to `https://new/a` to
   `https://new/a/` shows up as CHAIN in the checker. Cause: old redirects were left pointing at old targets. Fix:
   point every old form straight at the final URL.
3. **Staging robots.txt shipped.** Symptom: crawling stops on launch day. Cause: `Disallow: /` went live with the
   release. Fix: check it in the first hour.
4. **Content cut in the redesign.** Symptom: the redirects work but the new pages are weaker. Cause: shorter pages,
   removed FAQ or text, and fewer internal links. Fix: compare templates before launch.
5. **Internal links still point to old URLs.** Symptom: logs show redirects on every click and crawl. Cause: the
   content and navigation were not updated. Fix: update links in content and navigation.
6. **Images and PDFs forgotten.** Symptom: image search traffic and links to files are lost. Cause: they were left out
   of the inventory. Fix: include them in the inventory.
7. **Moving during peak season.** Symptom: a normal dip lands on the most valuable weeks, and a fault cannot be
   separated from a content change. Cause: the date was set without looking at the calendar, or the move was tied to a
   large content change. Fix: move at a quiet time, apart from other large changes.

## Anti-patterns in migrations

Anti-patterns in migrations save a day of planning and cost months of traffic.

| Do not | Do this instead |
|---|---|
| Changing domain, URLs and templates in one release | change as few things at once as the business allows |
| Testing the redirect map only on a sample | run every row on staging and on production |
| Dropping redirects after a few months | keep them at least one year, and keep the old domain registered |
| Using 302 for permanent moves | use 301 or 308 |
| Deciding on rollback during the incident | agree the criteria before launch |

## References for migrations

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- `scripts/redirect_check.py`: tests a redirect map CSV: one hop, permanent status, right target, target answers 200.

## See also for migrations

- `crawling-and-indexing`: robots.txt, `noindex` and status codes
- `xml-sitemaps`: new sitemaps and the old one
- `canonical-urls`: canonicals that follow the move
- `internal-linking`: links to final URLs
- `seo-measurement`: benchmarks and monitoring
- `search-console`: exports for the benchmark and the Page indexing report after launch
- `naver-search-advisor`: moves on Naver
