---
title: Wordstat and Yandex demand sources
author: MOZGII, Inc.
lang: en
description: Wordstat operators for exact frequency, every Yandex demand, wording and position source with its limits, and the metrics to ignore.
---

# Wordstat and Yandex demand sources

Wordstat and the other Yandex sources answer three questions: how many people search a phrase, how they phrase it,
and where a site ranks. Prices and quotas change; read the current terms before relying on a paid source.

## Contents

1. Wordstat operators
2. Demand sources for Yandex
3. Wordstat through the Yandex Search API
4. Wording sources for Yandex
5. Your own site's Yandex queries and positions
6. Competitor positions in Yandex
7. What to ignore

## Wordstat operators

Wordstat operators fix parts of a query, which is how exact frequency is measured. Yandex matches all word forms by
default (official help: yandex.ru/support2/wordstat/ru/content/operators).

| Operator | Fixes | Example |
|---|---|---|
| `!word` | the word form (case, number, tense) | `купить !диван` |
| `+word` | a stop word (preposition, pronoun) | `работа +на дому` |
| `"..."` | the number of words (order may vary) | `"купить диван"` |
| `[...]` | the word order | `билеты [из москвы в казань]` |
| `-word` | excludes a word | `доставка -цветы` |
| `(a\|b)` | alternatives | `заказать (суши\|пиццу)` |

Exact frequency of a phrase as typed: quotes plus `!` on every word, prepositions included:
`"!ремонт !квартир !под !ключ"`.

## Demand sources for Yandex

Yandex demand sources estimate monthly query frequency; exact frequency decides.

| Source | Access | Gives | Limits |
|---|---|---|---|
| Wordstat web (wordstat.yandex.ru) | Yandex ID, by hand | broad and operator-filtered monthly frequency, regions, devices, dynamics | manual; the reference number for decisions |
| Wordstat API (`https://api.wordstat.yandex.net`) | Yandex OAuth token, then a connection request to Yandex Direct support with your login and `ClientId` | the same data as the new Wordstat: frequency, top and similar queries, dynamics, regions, devices | a personal quota per second and per day (429), and a total quota on the whole API (503) |
| Yandex Search API: Wordstat methods | a service account with an API key, billed per 1,000 requests | top queries, dynamics, regional distribution | quotas; see "Wordstat through the Yandex Search API" |
| Bukvarix free API (`https://api.bukvarix.com`) | `api_key=free`, a key shared by everyone, no login | a copy of Wordstat: broad and exact frequency, all regions combined | 429 after about 30 fast requests; snapshot date not stated; regions not split |
| Key Collector and paid suites | licence plus Yandex accounts | bulk Wordstat collection by region | paid, manual setup |

`scripts/demand.mjs` uses the Bukvarix copy plus Yandex suggestions with a 30-day cache and 429 backoff. It sends every
request over https and refuses a redirect to anything else, so nobody on the network can read a phrase; Bukvarix and
Yandex still receive each phrase they answer, so keep unannounced product names out of it. Bukvarix TSV
columns: phrase, words, characters, broad frequency, exact frequency. A phrase may be stored in another form or
order; the script matches by content words before reporting zero, and shows the stored form in the `as` column.

Confirm numbers that decide a main phrase in Wordstat itself, with the regions the business sells to.

## Wordstat through the Yandex Search API

The Yandex Search API offers Wordstat as synchronous REST and gRPC methods, with no application to Direct support. The
service account needs the role `search-api.webSearch.user`, and an API key needs the scope `yc.search-api.execute`. Send
`Authorization: Api-key <key>` or `Authorization: Bearer <IAM token>`, and put your folder in `folderId`.

| Method | REST: POST `https://searchapi.api.cloud.yandex.net` + | Returns |
|---|---|---|
| `GetTop` | `/v2/wordstat/topRequests` | the most popular queries containing the phrase over the last 30 days, plus associations; `numPhrases` defaults to 50, at most 2,000 |
| `GetDynamics` | `/v2/wordstat/dynamics` | query frequency per month, week or day between `fromDate` and `toDate`, each with `count` and `share` |
| `GetRegionsDistribution` | `/v2/wordstat/regions` | the last 30 days per region: `count`, `share` and `affinityIndex`; `region` is `REGION_ALL`, `REGION_CITIES` or `REGION_REGIONS` |
| `GetRegionsTree` | see the API reference | the region codes Wordstat supports |

`phrase` takes search operators, up to 400 characters in `GetRegionsDistribution`. In `GetDynamics` every operator works
for daily data, while weekly and monthly data accept only `+`; a week runs Sunday to Saturday. `regions` takes region
IDs such as `213` for Moscow, and `devices` takes `DEVICE_ALL`, `DEVICE_DESKTOP`, `DEVICE_PHONE` or `DEVICE_TABLET`.

```bash
curl -s -X POST https://searchapi.api.cloud.yandex.net/v2/wordstat/topRequests \
  -H "Authorization: Api-key $YANDEX_API_KEY" -H 'Content-Type: application/json' \
  -d '{"phrase":"ремонт квартир","numPhrases":100,"regions":["213"],"folderId":"'"$YANDEX_FOLDER_ID"'"}'
```

The answer holds `totalCount`, `results` and `associations`, with counts as strings. On 31 October 2026 the pricing page
listed, without VAT, $0.1639344 per 1,000 requests for `GetTop` and `GetDynamics`, $0.409836 for
`GetRegionsDistribution`, and `GetRegionsTree` free. The limits page listed quotas of 10 requests a second and 100 an
hour, which support can raise. Read both pages before a large run. Source: [Wordstat in the Search
API](https://aistudio.yandex.ru/docs/en/search-api/concepts/wordstat).

## Wording sources for Yandex

Wording sources show how people phrase a need; they rank phrases against each other, not by volume.

| Source | Access | Gives |
|---|---|---|
| Yandex suggest `https://suggest.yandex.ru/suggest-ff.cgi?part=...&uil=ru&v=3&sn=10` | none | up to 10 completions by popularity |
| Wordstat "similar queries" | login | neighbouring queries |
| Webmaster › Search queries | site owner | the exact words people used to find you |

Suggest Signal = Σ 1/position over every list the phrase appears in (`demand.mjs --expand`).

## Your own site's Yandex queries and positions

Your own Yandex queries and positions come from Yandex Webmaster, in the interface or through the Webmaster API with
the owner's OAuth token (search query reports with shows, clicks and average show and click positions; popular
queries cover the top 3,000). For research, export the queries you already get shows for: they are proven demand your
pages partly match.

## Competitor positions in Yandex

Competitor positions in Yandex must be collected without scraping the results page.

- Scraping the Yandex results page triggers a captcha and blocks. Do not.
- Yandex Search API (Yandex Cloud) returns results pages for a fee per request, cheaper in deferred mode.
- Manual check: a private window, `lr=213` (Moscow) or `lr=225` (Russia) in the search URL, a screenshot with the date.

## What to ignore

Some Russian-market SEO metrics look precise and mean little.

| Claim | Why |
|---|---|
| site scores and "trust" from third-party services | vendors' own formulas; Yandex does not use them |
| «тошнота», «водность», keyword density | Yandex publishes no such numbers; they produce text written for the robot |
| keyword difficulty from tools built on Google data | weak for Yandex |
| positions for zero-demand phrases | they rank because nobody competes, and bring nothing |
| meta keywords | ignored |
