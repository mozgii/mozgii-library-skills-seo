---
name: programmatic-seo
description: 'Plans, builds and launches pages generated from data at scale (locations, integrations, comparisons, alternatives, product specs, templates, glossaries) without falling into scaled content abuse or doorways: choosing page sets from demand, the unique data each page needs, template design, quality gates, indexing in batches, internal links, monitoring the indexed share, and pruning. Use when asked for programmatic SEO, pages for every city or integration, X vs Y or alternatives pages at scale, or why thousands of generated pages are not indexed.'
metadata:
  tags:
  - seo
  - programmatic-seo
  - scaled-content
  - templates
  - landing-pages
  - comparison-pages
---

# Programmatic SEO

Programmatic SEO generates many pages from one template and a dataset: one page per city, integration, product pair,
template or term. It works when each page answers a query people type with data that is specific to that page, and it
is scaled content abuse (or a doorway) when a template swaps one word and adds nothing. Google's spam policy judges
the result, whatever made it: people, templates or AI.

## Step 0: read the dataset and what is already live

Read the data before the template, because the number of rows with something unique to say sets how many pages can
exist. Measure the data, then what the site already has in that folder:

```bash
wc -l integrations.csv
cut -d, -f3 integrations.csv | sort -u | wc -l     # distinct values in the column that should make each page unique
curl -s https://www.example.com/sitemap.xml | grep -oE '<loc>[^<]+' | awk -F/ '{print $4}' | sort | uniq -c | sort -rn | head
```

Then read Page indexing filtered to the sitemap of any pages already generated, the Search Console queries they get,
and where the data comes from and how often it changes.

## When programmatic pages are worth it

Programmatic pages are worth building only when three things hold. Check them before any template is designed.

1. **A repeating query pattern with demand**: "[tool] integration with [tool]", "[city] [service] prices",
   "[product] vs [product]". Measure demand for a sample of 20–50 variants (the `keyword-research` skill); the head
   variants must have measurable volume.
2. **Data that differs per page**: prices, specs, availability, reviews, local facts, real usage numbers, steps that
   differ. If the only difference is the variable in the title, stop.
3. **A reason to be the best answer**: your own data, product or expertise. Aggregating what already ranks is not one.

## Page types and the data each needs

The common page types each need their own minimum of unique data per page.

| Page type | Query pattern | Unique data the page must carry |
|---|---|---|
| Location | "[service] in [city]" | address or service area, local prices, response times, local reviews, jobs done there, staff |
| Integration | "[product] [other tool] integration" | what syncs, setup steps for that pair, limits, screenshots, real use cases |
| Comparison | "[A] vs [B]" | a feature table from tested facts, prices with dates, who each suits, a verdict |
| Alternatives | "[competitor] alternatives" | why people leave the competitor, 5–10 real options with fit and price, honest placement of your own product |
| Product or spec | "[model] [spec]" | full specifications, compatibility, availability, own photos |
| Template or tool | "[document] template", "[unit] converter" | the working template or tool itself |
| Glossary | "what is [term]" | a precise definition, an example from your field, links to deeper pages |

## Design the template around the data

The template decides whether every page is useful. Design it from the data fields, not from a text with blanks.

- Put the unique data first: the table, the numbers, the answer. Generic explanation goes lower or on a hub page.
- Generate titles and descriptions from data ("Runner X vs Speed Y: 40 g lighter, €20 cheaper"), not from one sentence
  with a swapped name.
- Show empty states honestly. A field with no data is hidden, not filled with filler text.
- Add a human layer where it pays: an editor's note on the top 10% of pages by demand.
- AI may draft text from the data; a person checks a sample of every batch, and no claim appears that the data does
  not support.

## Quality gates before a page is indexable

A quality gate decides per page whether it is published, published with `noindex`, or not generated. Encode it in the
build, so it applies to every page.

```text
publish and index   unique data fields ≥ 4 of 6 AND measured demand (or a strategic reason) AND passes review sample
publish, noindex    useful to users who navigate there, but thin or without demand yet
do not generate     no data, duplicate of another page, or a combination nobody searches
```

Pages under `noindex` stay out of the sitemap and get no internal links from hubs until they pass the gate.

## Launch in batches and watch the indexed share

Launch in batches, so a quality problem shows on a hundred pages instead of ten thousand.

1. Publish the strongest 5–10% (highest demand, richest data) first, linked from hubs and in a sitemap of their own.
2. After four to six weeks, read that sitemap in Search Console: indexed share, impressions, clicks.
3. Indexed share above about 80% and impressions growing: release the next batch. Many "Crawled - currently not
   indexed": improve the template before releasing more.
4. Keep one sitemap per page type and batch so the Sitemaps and Page indexing reports show which set works.

## Internal links at scale

Generated pages need links from crawled pages, or they stay "Discovered - currently not indexed".

- A hub per page type and dimension (`/integrations/`, `/integrations/crm/`, `/locations/texas/`) linking to every
  indexable child.
- Sideways links by real relations: nearby cities, the other tools in the same category, the comparison's
  alternatives.
- Links from the product or service pages each set supports.
- No link blocks of hundreds of generated pages on every page; link what a reader would follow.

## Prune and maintain generated pages

Programmatic pages age with their data, so they need a schedule.

- Refresh data on a schedule and show the date of the data on the page.
- Every quarter, list pages with no impressions in 6 months: improve the data, merge, `noindex` or remove (404 or a
  301 to the hub when links point there).
- When the source of a page's data disappears (a discontinued product, a closed location), the page follows it.

## Worked example: integration pages for a SaaS product

Situation: a scheduling tool connects to 1,400 apps through a connector platform and wants a page per integration.

Decision: demand checked for 60 pairs; 180 apps have measurable "[tool] [app] integration" searches. Unique data
exists for 220 apps (triggers, actions, setup steps, usage counts from the product). Plan: generate 220 pages; index
the 180 with demand and full data; `noindex` the 40 without demand; do not generate the other 1,180. Launch the top
30 with editor notes and screenshots first, from an `/integrations/` hub with category hubs. After five weeks 27 of 30
indexed and impressions growing: release the remaining 150 in two batches.

## Verify a batch before and after launch

A batch is checked twice. Before launch, measure how much of each page is its own: fetch a sample and compare the
visible text pairwise, so a word-swap template shows up at once:

```bash
python3 - urls.txt <<'EOF'
import html, itertools, re, sys, urllib.request
def words(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
        text = r.read().decode("utf-8", "replace")
    text = re.sub(r"(?is)<(script|style).*?</\1>|<[^>]+>", " ", text)
    tokens = re.findall(r"\w+", html.unescape(text).lower())
    return {" ".join(tokens[i:i + 5]) for i in range(len(tokens) - 4)}
urls = [line.strip() for line in open(sys.argv[1]) if line.strip()][:20]
pages = {u: words(u) for u in urls}
for a, b in itertools.combinations(urls, 2):
    share = len(pages[a] & pages[b]) / max(1, min(len(pages[a]), len(pages[b])))
    if share > 0.7:
        print(f"{share:.0%} shared: {a} {b}")
EOF
```

Pairs above 70% shared five-word runs need a look: a shared header and footer count too, so judge the main content of
any pair it names. No output means the sample differs. After launch, read the batch's own sitemap in Search Console:
indexed share above about 80% and impressions growing clear the next batch; a pile of "Crawled - currently not
indexed" sends the template back. Every `noindex` page must be absent from the sitemaps, so compare the two lists.

## Checklist for programmatic SEO

The checklist runs before launch and at each batch.

1. Query pattern measured on a sample; head variants have demand.
2. At least four fields of unique data per indexable page; empty fields hidden.
3. Titles, descriptions and H1 generated from data, not a swapped word.
4. Quality gate encoded: index, `noindex` or not generated, per page.
5. Launched in batches with a sitemap per batch; indexed share read before the next batch.
6. Hubs and sideways links reach every indexable page.
7. Data refresh and quarterly pruning scheduled.

## Gotchas in programmatic SEO

The gotchas below turn programmatic SEO into a spam problem.

1. **City-swap pages.** Symptom: 400 town pages sit in "Crawled - currently not indexed". Cause:
   The same text for 400 towns is a doorway. Fix: build one strong regional page instead.
2. **Generating every combination.** Symptom: the sitemap holds millions of URLs and traffic reaches a few. Cause: the
   data allows it, but most combinations have no searcher. Fix: generate only what has demand and data.
3. **Publishing 50,000 pages at once.** Symptom: crawl stalls and quality problems show everywhere at once. Cause:
   nothing tested the template on a small set. Fix: launch in batches.
4. **AI text without data.** Symptom: fluent pages draw no impressions or a spam action. Cause: pages that say nothing
   specific are scaled content abuse. Fix: give each page its own data first.
5. **Comparison pages that always pick you.** Symptom: readers leave and reviewers call it out. Cause: every verdict
   favours your product. Fix: give an honest verdict with facts.
6. **No pruning.** Symptom: a healthy set slowly loses impressions. Cause: stale data pages pull down how Google
   judges the whole set. Fix: prune every quarter.
7. **Thin pages in the sitemap.** Symptom: the indexed share falls across the set. Cause: a sitemap full of `noindex`
   or thin URLs teaches Google to trust the set less. Fix: keep only pages that passed the gate.

## Anti-patterns in programmatic SEO

Anti-patterns at scale multiply a small template mistake by the number of pages.

| Do not | Do this instead |
|---|---|
| Starting from a template and looking for data later | start from the data fields and design around them |
| Filling empty fields with generic text | hide the field |
| Writing one title sentence with a swapped name | generate titles and descriptions from the data |
| Letting AI state claims the data does not hold | have a person check a sample of every batch |
| Putting hundreds of generated links on every page | link what a reader would follow |

## See also for programmatic SEO

- `keyword-research`: measuring a query pattern's demand
- `local-seo`: location pages that are not doorways
- `algorithm-updates-and-penalties`: scaled content abuse and recovery
- `xml-sitemaps`: one sitemap per batch
- `internal-linking`: hubs and sideways links
