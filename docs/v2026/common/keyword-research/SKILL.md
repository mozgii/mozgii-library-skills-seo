---
name: keyword-research
description: 'Decides which search queries a site should target and which page owns each one, from measured demand rather than guessed phrases: seed lists, autocomplete expansion, volume from Keyword Planner, Bing, Search Console or Wordstat, search intent, a reproducible scoring formula with tiers, SERP-based clustering, one main phrase per page, cannibalisation checks, and a review of bought keyword lists. Use when asked for keyword research, a keyword map or content plan, what to write about, which query to put on a page, or why two pages compete for one query.'
metadata:
  tags:
  - seo
  - keyword-research
  - search-intent
  - keyword-mapping
  - cannibalization
  - content-plan
---

# Keyword research and keyword mapping

Keyword research decides which search queries a site should own and which page owns each one, from measured demand
rather than phrases someone imagined. The output is a keyword plan: every phrase with its volume (or an explicit "no
data"), intent, score, tier and owner page, with no phrase owned by two pages.

## Step 0: read what the site already ranks for

Read the site's own queries and pages first, because proven demand beats any seed list. The first command counts the
sitemap's URLs, the second lists queries the site already shows for (it needs a token with the `webmasters.readonly` scope
in `GSC_TOKEN`), and the third confirms the script runs.

```bash
curl -s https://www.example.com/sitemap.xml | grep -o '<loc>' | wc -l
curl -s -X POST "https://searchconsole.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query" \
  -H "Authorization: Bearer $GSC_TOKEN" -H "Content-Type: application/json" \
  -d '{"startDate":"2026-07-01","endDate":"2026-09-30","dimensions":["query"],"rowLimit":1000}' \
| python3 -c "import json,sys; [print(r['keys'][0], int(r['impressions']), int(r['clicks']), sep='\t') for r in json.load(sys.stdin).get('rows', [])]" > own-queries.tsv
python3 scripts/autocomplete.py --help
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

A sitemap index answers with its child sitemaps, so count those files too.

## Routing keyword tasks

Keyword tasks share one workflow; smaller requests use part of it.

| Task | Steps | Read |
|---|---|---|
| Build or extend a keyword plan for a site | 1–7 | all references |
| Check demand for a few phrases | 3 | [references/sources-and-tools.md](references/sources-and-tools.md) |
| Pick the main phrase for one page | 3, 4, 6 | [references/scoring.md](references/scoring.md) |
| Map phrases to pages, fix cannibalisation | 6, 7 | this file |
| Review a keyword list from a contractor | "Review a bought keyword list" | [references/scoring.md](references/scoring.md) |
| Competitor topics and gaps | step 2 | [references/competitor-research.md](references/competitor-research.md) |
| Russian-language demand and Wordstat | step 3 | the `yandex-wordstat` skill |
| Write the page for the chosen phrase | out of scope | `on-page-seo`, `content-briefs` |

## Inputs for keyword research

The inputs below each change the result, so ask once for any that is missing.

- **What the business sells**, to whom, and the deal sizes (they drive intent and value).
- **Markets**: countries, regions, cities, languages; the search engines that matter there.
- **Existing pages and their current phrases**: read the sitemap, the page list or the existing keyword file first;
  the site's own list is the starting point.
- **Data access**: Search Console, Google Ads (Keyword Planner), Bing Webmaster Tools, Wordstat, a paid tool, or only
  free sources.

## Keyword research workflow

The keyword research workflow runs in seven steps, from seeds to a verified plan.

### 1. Seeds

Seed phrases come from the offer, existing page titles, the words customers use in calls, chats and reviews, and
the queries the site already gets impressions for in Search Console (proven demand). Queries where a page already
sits on page two are the cheapest wins, so list those first. Write 10–30.

### 2. Competitors

Competitor research shows how the market names things and structures pages: categories, sitemaps, title and heading
vocabulary, gaps nobody covers ([references/competitor-research.md](references/competitor-research.md)). Take
structure and vocabulary, never text.

### 3. Expand and measure demand

The autocomplete script expands each seed with question or commercial modifiers and ranks candidates by a suggest
Signal (Σ 1/position); it is wording evidence, not volume. It asks Bing by default:

```bash
python3 scripts/autocomplete.py "trail running shoes" "hiking boots" --hl en --gl us --modifiers commercial --out candidates.tsv
python3 scripts/autocomplete.py "trail running shoes" --modifiers questions
python3 scripts/autocomplete.py "sofa bed" --hl en --gl gb
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

`--engine google` exists for a few seeds typed by hand, at your own risk: Google's spam policies name automated queries
as machine-generated traffic, so requests can be blocked. For Google's wording prefer Search Console queries and a
manual look at the suggestions in a private window.

Then measure volume for the shortlisted candidates in Google Keyword Planner (exact ranges unless the account runs
ads), Bing Webmaster Tools › Keyword Research (free, exact Bing numbers), Search Console impressions for phrases the
site already shows for, or a paid tool. For Russian-language markets use Wordstat exact frequency (`yandex-wordstat`).

- Record the source and month next to each number; numbers from different tools are not comparable.
- A phrase with no measurable demand is never a main phrase. Keep it only as a body-text variant or a recorded
  strategic bet.

### 4. Intent

Search intent decides the page type, and a page of the wrong type does not rank no matter how good it is. Classify
each phrase (table in [references/scoring.md](references/scoring.md)): transactional, commercial investigation,
informational, navigational, local, or exclude. Check the top 10 results for the phrase: if they are all product
listings, an article will not rank there, and the reverse.

### 5. Score and tier

The score makes two people rank the same list the same way:

```text
rating = 0.55 × business value + 0.20 × market signal + 0.10 × suggest signal + 0.15 × page readiness
tiers:   A ≥ 70   B 55–70   C < 55
```

Definitions and code: [references/scoring.md](references/scoring.md). Write the weights next to the list. A strategic
bet gets a fixed, labelled bonus and a review date; it is never presented as demand.

### 6. Cluster and map

Clustering groups phrases that one page can answer; mapping gives each cluster an owner page.

- **Cluster** by SERP overlap when results are available: phrases whose top 10 share three or more URLs belong to one
  page. Without SERP data, cluster by same intent and same content words.
- **One main phrase per page**: the strongest-demand phrase of its cluster with the right intent, plus 3–6 secondary
  phrases.
- **Owner rule**: a main phrase appears in the title or H1 of its owner page only. Other pages may use it in body text
  and link to the owner with the phrase as anchor (`internal-linking`).

Output columns:

```text
phrase | volume | source/month | intent | rating | tier | cluster | owner page | role (main/secondary/body) | note
```

### 7. Verify the plan

The plan is verified before anyone writes a page.

- Every phrase has a volume or `no data` written; no zero-demand phrase is a main phrase.
- No phrase is main on two pages (role in column 9 of a TSV export):

```bash
awk -F'\t' '$9=="main"{print $1}' plan.tsv | sort | uniq -d    # expect no output
```

- Every page in the plan has exactly one main phrase; pages with fewer than three phrases are listed.
- Main phrases missing from their owner page's title are listed as fixes.
- Six weeks after publishing, Search Console › Performance › Queries for the main phrase: if two pages share the
  impressions, the owner rule is broken somewhere.

## Worked example: a keyword plan for a trail running shop

Request: a UK running shop with 40 pages is adding a trail shoe range and wants a plan. It has Search Console and Keyword
Planner, with no active ads.

Seeds and competitors: 14 seeds from category names, customer emails and Search Console, where "trail running shoes"
already sits at position 14 on the category page, so it goes first. Three competitors split trail shoes by terrain, and
none has a page for wide feet.

Measure: `autocomplete.py` expands the seeds with commercial modifiers and returns 86 candidates. Keyword Planner gives
ranges for the 25 shortlisted, and two phrases with no volume and no suggestion are dropped: a phrase with no demand is
never a main phrase.

Score, tier and map, with the weights written next to the list. The cluster and note columns are left out here:

| phrase | volume | source/month | intent | rating | tier | owner page | role |
|---|---|---|---|---|---|---|---|
| trail running shoes | 10K–100K | Planner 2026-10 | transactional | 89 | A | /running-shoes/trail/ | main |
| wide fit trail shoes | 100–1K | Planner 2026-10 | transactional | 71 | A | /running-shoes/trail/wide/ | main |
| waterproof trail shoes | 1K–10K | Planner 2026-10 | transactional | 65 | B | /running-shoes/trail/ | secondary |
| how long do trail shoes last | 100–1K | Planner 2026-10 | informational | 42 | C | /guides/trail-shoe-life/ | main |

"Trail running shoes" scores 0.55 × 90 (value) + 0.20 × 80 (market) + 0.10 × 100 (suggest) + 0.15 × 90 (readiness) = 89. The top results for "waterproof trail
shoes" share four URLs with the main phrase, so it stays on the same page as a secondary phrase instead of getting one
of its own. "Wide fit" has a smaller volume, but nobody serves it and buyers mean to buy, so it earns a new page.

Check: the `awk` duplicate test in step 7 prints nothing, every page has one main phrase, and the source and month sit
beside each number. Six weeks after publishing, Search Console shows the three main phrases on their owner pages only.

## Find keyword cannibalisation

Cannibalisation is two or more pages of one site competing for the same query, so neither ranks well. Export query
and page pairs from Search Console (the Search Analytics API with dimensions `query` and `page`, or the BigQuery bulk
export) into a TSV with the columns query, page, clicks, impressions, and list queries where several pages each get a
meaningful share of impressions:

```bash
awk -F'\t' 'NR>1 && $4>50 {n[$1]++; p[$1]=p[$1]" "$2} END {for (q in n) if (n[q]>1) print n[q]"\t"q"\t"p[q]}' rows.tsv | sort -rn | head -30
```

Fix by choosing one owner, merging or differentiating the other page (different intent), moving the phrase out of the
other page's title and H1, and linking to the owner. Two pages ranking 1 and 2 for a query is not a problem.

## Review a bought keyword list

Keyword lists from contractors are often generated from templates (service + industry + city) and have no demand.
Zero-demand phrases rank fast because nobody competes, so a report of "positions growing" can coexist with zero
traffic.

1. Measure every phrase (step 3); mark keep (demand), tail (weak), drop (none).
2. For dropped phrases, look for the wording people do type (autocomplete, Search Console queries).
3. Report counts per decision, the phrases worth adding with numbers, and what to ask the contractor for: volume per
   phrase with source, region and month, and reporting in impressions, clicks and leads instead of positions.

<example>
Input: 500 phrases. Result: 4 kept (16–76 searches a month), 2 tail, 16 duplicates, 478 dropped (no volume and no
longer variant with volume). One missing phrase with demand found during the check.
</example>

## Checklist for a keyword plan

The keyword plan checklist is what makes the plan usable by writers and developers.

1. Seeds include the site's own Search Console queries.
2. Every phrase has volume with source and month, or "no data".
3. Intent checked against the live top 10 for every main phrase.
4. Scores computed with written weights; tiers assigned.
5. One main phrase per page; no phrase main on two pages (the awk check passes).
6. Each cluster has an owner page, existing or planned, with its page type.

## Gotchas in keyword research

The gotchas below are the usual reasons a keyword plan brings no traffic.

1. **Planning on inflated volume.** Symptom: a phrase with thousands of searches brings tens of visits. Cause: tools
   group close variants and round; Wordstat broad counts every longer query. Fix: use exact or close-match numbers and
   compare like with like.
2. **Template permutations.** Symptom: hundreds of "service for industry in city" phrases sit in the plan with no
   impressions. Cause: the list came from a template, and those phrases have no demand. Fix: measure them and drop
   what has none.
3. **Ignoring intent.** Symptom: a commercial page targeting an informational query (or the reverse) stays on page
   two. Cause: the page type does not match the results. Fix: check the top 10 and match the page type.
4. **Two pages, one phrase.** Symptom: rankings alternate between pages. Cause: the plan gave both pages one main
   phrase. Fix: keep one owner; the other links to it.
5. **Keyword difficulty as truth.** Symptom: a phrase is dropped for its score, or chosen and then proves impossible.
   Cause: difficulty scores are vendor estimates from backlink counts. Fix: read the actual top 10: who ranks, what
   type of page, how strong.
6. **Scraping search results.** Symptom: requests are blocked, or a tool's IP gets captchas. Cause: automated queries
   to Google violate its policies and get blocked. That covers `--engine google` in the autocomplete script, which is
   why Bing is its default. Fix: use Search Console, official APIs, or a SERP data provider, and keep `--engine
   google` to a few seeds at your own risk.
7. **Zero volume is not zero value.** Symptom: a B2B phrase with no recorded searches brings a real lead, or a page
   built on such a phrase brings nothing. Cause: long, specific B2B phrases often sit below what tools can measure.
   Fix: mark them as bets with a review date instead of building pages on them blindly.

## Anti-patterns in keyword research

Anti-patterns in keyword research produce long lists that nobody can act on.

| Do not | Do this instead |
|---|---|
| Starting from a tool's list instead of the site | start from the offer and Search Console queries |
| Mixing numbers from different tools in one column | record the source and month beside each number |
| Adjusting weights until a favourite phrase wins | write the weights beside the list and keep them |
| Creating a page for every variant | cluster phrases one page can answer |
| Copying competitors' text along with their structure | take structure and vocabulary, never text |

## References for keyword research

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/sources-and-tools.md](references/sources-and-tools.md): every demand, wording and position source,
  what it gives, its limits.
- [references/scoring.md](references/scoring.md): demand levels, the rating formula, intent classes, tiers,
  strategic bets.
- [references/competitor-research.md](references/competitor-research.md): finding, categorising and harvesting
  competitors.
- `scripts/autocomplete.py`: seed expansion from Bing autocomplete (Google only with `--engine google`, at your own
  risk) with a Signal score.

## See also for keyword research

- `on-page-seo`: placing the chosen phrases on a page
- `content-briefs`: turning a phrase into a brief
- `internal-linking`: the owner rule in links
- `yandex-wordstat`: Wordstat and Russian-language demand
- `bing-webmaster-tools`: Bing's Keyword Research tool and query exports
- `search-console`: query exports and cannibalisation data
