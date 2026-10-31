---
title: Competitor research for SEO
author: MOZGII, Inc.
lang: en
description: How to find, categorise, rank and harvest search competitors for vocabulary, structure and content gaps, without copying their text.
---

# Competitor research for SEO

Search competitors show how the market names things and how it structures pages. Take structure and vocabulary;
never their text, numbers, prices, promises or names into your own copy.

## Find search competitors

Search competitors are the domains that rank for your phrases, which are often not your business competitors.

1. Search the top 10–20 phrases (by hand or through a SERP API) in the target markets; record every domain in the
   top 10 with the query that found it.
2. Add domains from industry lists, marketplaces and partner catalogues.
3. Separate media and aggregators (news sites, directories, marketplaces, Wikipedia) from sellers: they compete for
   the results page, not for the deal, and need a content answer, not an offer answer.

## Categorise competitors

Competitor categories decide what to learn from each.

| Category | Definition |
|---|---|
| direct | sells the same product or service |
| integrator | sells adjacent systems, with a page on your topic |
| adjacent | a platform or product that overlaps some queries |
| large generalist | a big firm with a section on the topic |
| content | media, blog, course or directory ranking for the queries |

## Closeness index

The closeness index (0–100) ranks who to study first. A starting formula; tune the weights to the business and write
them down with the list:

```text
closeness = category weight (direct 40, integrator 25, adjacent 20, large generalist 15, content 10)
          + 30 × shared directions / your directions
          + 30 × trust blocks present / 6   (prices, cases with numbers, legal details, reviews, guarantee, contacts)
```

## Harvest each competitor site

Harvesting reads a competitor's structure from public files and a sample of pages.

```bash
curl -s https://competitor.example/robots.txt | grep -i sitemap
curl -s https://competitor.example/sitemap.xml | grep -o '<loc>[^<]*' | sed 's/<loc>//' > competitor-urls.txt
# a sitemap index lists child sitemaps: fetch each and append its URLs
grep -E '\.xml(\.gz)?$' competitor-urls.txt | while read -r sm; do
  curl -s --compressed "$sm" | gunzip -cf | grep -o '<loc>[^<]*' | sed 's/<loc>//'
done >> competitor-urls.txt
cut -d/ -f4 competitor-urls.txt | sort | uniq -c | sort -rn | head -20     # pages per top-level section
```

- The full URL list shows sections, pages per direction and slug vocabulary: where they invest.
- Read 10–20 pages per close competitor: title, description, H1–H3, prices, calls to action, proof, legal details,
  JSON-LD types (view the source, or `curl -s <url>` and search for `<title`, `<h1`, `ld+json`).
- Write one note per site: what they sell, prices and terms, proof, path to a lead, page structure, overlap with your
  directions, strength per direction.

## Use the competitor research

Competitor research feeds four decisions.

- **Market signal** for scoring: share of competitors using the phrase's words in title, H1 or H2.
- **Gap list**: queries and sections competitors cover and you do not; directions where nobody has a page (a
  category nobody names yet is a strategic opportunity).
- **Strength per direction**: URL count plus mention density; tells where to expect a hard fight.
- **Structure ideas**: sections, segments covered, questions answered.

Do not copy their texts, numbers, cases or prices. Mentioning competitor brands on your pages brings legal and
advertising-law risk in many countries; compare by criteria instead. Refresh the harvest quarterly or before a large
content plan.
