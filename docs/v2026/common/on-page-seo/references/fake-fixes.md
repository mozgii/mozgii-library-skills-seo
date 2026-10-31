---
title: Real SEO fixes and fake fixes
author: MOZGII, Inc.
lang: en
description: A decision table of real fixes versus fake fixes that only satisfy a checker, the list of metrics to ignore, and the nine validation lines every edit must pass.
---

# Real SEO fixes and fake fixes

A fake fix makes a checker go green without helping a reader. It gets reverted, because search engines measure what
readers do and demote text written for robots (Google's keyword stuffing and scaled content policies, Yandex's
over-optimisation filter).

## Decision table: real fix or fake fix

The decision table pairs each common finding with the fix that helps and the fix to reject.

| Finding | Real fix | Fake fix (reject) |
|---|---|---|
| Main phrase missing in title or H1 | put the wording people search (highest demand for the same offer) at the start of the title and in the H1, in natural grammar | appending the raw query to the title; keeping a zero-demand wording because a plan says so (flag it instead) |
| Main phrase missing in description | rewrite to 120–160 characters: phrase + one number (price, days) + one reason to click | a list of keywords; a description longer than 170 |
| Main phrase missing in lead | rewrite the first sentence so it answers the query with the phrase in it | a new sentence that only repeats the phrase |
| Below the word minimum | add an answer the buyer needs: a price example, a step, a limitation, an FAQ from the page's phrase list | filler paragraphs, text copied from another page, repeated sections; if the page already answers everything, leave it and say so |
| A-tier phrase missing | use it once where it answers a question: an H2, the lead, a card title or an FAQ question | inserting it into several paragraphs |
| Exact repeats above the limit | replace extra repeats with pronouns, synonyms, merged sentences | swapping in near-identical forms to fool the counter |
| Few internal links in | a sentence with a descriptive link on two or three related pages | link blocks, footer lists, the same anchor everywhere |
| Wording nobody searches | switch to the searched wording if it describes the same offer | keeping it; or switching to a high-volume wording that describes a different offer |
| Typo or wrong case in a term | fix every file with the same error (`grep -rn` across content) | fixing one page and leaving the copies |
| Thin location or industry page | add a case or specific task from real material | copying another page and swapping the place or industry word (doorway) |
| Low score from a text-analysis tool | ignore the score; read the text | raising density, padding for "uniqueness" |

## Ignore list

The ignore list names metrics that look like targets but are not.

| Signal | Why it is not a target |
|---|---|
| keyword density, "nausea" and "water" scores | no engine publishes such numbers; optimising them produces over-optimised text |
| word count of the top 10 | no magic length; coverage of questions matters |
| uniqueness percentage | a tool's own index, not the engine's |
| domain authority, trust and visibility scores as goals | third-party formulas or consequences, not causes |
| meta keywords | ignored by Google and Bing |
| Lighthouse SEO score 100 | only says certain tags exist |
| heading count, exact-match domain | not ranking levers |

## Validation lines for every edit

Every edit must pass all nine validation lines; a fix that fails any line is reverted and the report says which.

1. The build passes and the page is still server-rendered or static.
2. The finding is gone, checked on the built HTML, not the source.
3. No new finding on the changed page or on pages sharing the phrase.
4. Stuffing: main phrase exact ≤ 3 in the text, once in the title; inflected forms counted too for languages with
   rich morphology (for Russian, `text-check.mjs` in the `russian-language-seo` skill).
5. Cannibalisation: no other page's title or H1 carries this page's main phrase.
6. Truth: every number and claim matches the business's source of facts or a cited source; no unprovable
   superlatives ("best", "number one") where advertising law requires proof.
7. Language: passes the site's style rules and reads as written by a person (no filler openers, no stacked hedges).
8. Read-aloud: no sentence exists only for robots.
9. Layout: a longer title or H1 does not break the first screen at 375 px width.
