---
title: Russian search language layer
author: MOZGII, Inc.
lang: en
description: How a Russian sentence carries a search query without reading like spam - morphology, zones, lemma counting, metadata, headings, topical completeness and over-optimisation signs.
---

# Russian search language layer

The search language layer is how a Russian sentence carries a search query without reading like spam. Pass 2 of the
Russian-language SEO skill applies this file. Page-level numbers (word minimums, how many H2s may change) belong to
the on-page contract; this file owns the language.

## Contents

1. How Yandex reads Russian words
2. Zones: where the main phrase goes
3. Counting repeats by lemma
4. Writing the metadata
5. Headings and structure
6. Answering the query
7. Topical completeness without density
8. Over-optimisation signs
9. Readability for a skimming reader
10. Claims and numbers

## How Yandex reads Russian words

Yandex matches all word forms of a query word by default; the Wordstat operators show what "fixed" means.

| Operator | Fixes | Example | Consequence for writing |
|---|---|---|---|
| none | nothing: all forms, any order, stop words ignored | `диван кровать` matches «диваны-кровати для гостиной» | inflect freely; one exact occurrence per zone is enough |
| `!word` | the word form (case, number, tense) | `!диван` excludes «дивана» | demand for one form tells which form goes into the title |
| `+на` | a stop word (preposition, pronoun) | `работа +на дому` is not «работа по дому» | when a preposition changes meaning, keep the searched one |
| `"…"` | the number of words, not the order | `"диван кровать"` excludes «диван кровать цена» | use quoted frequency to rank phrases against each other |
| `[…]` | word order | `[диван кровать]` | order matters only for titles and H1 |

Practical rules that follow:

- Write the grammatical sentence. «Как выбрать диван-кровать для ежедневного сна» covers the query «диван кровать
  для ежедневного сна выбрать»; the nominative chain is a query, not Russian.
- Hyphenated compounds keep a plain hyphen U+002D («диван-кровать»). Yandex splits it like a space. A non-breaking
  hyphen U+2011 is not guaranteed to split the same way; prevent line breaks in markup (`white-space: nowrap` on a
  span), never in the character.
- Abbreviations stay upper case in text («ИИ», «ЖК»). Search is case-insensitive; readers are not.
- Russian or Latin term: pick by demand, not taste. Compare quoted frequencies, for example `"!смарт !часы"` against
  `"!smart !watch"`.

## Zones: where the main phrase goes

The main phrase is the one query this page owns. It appears once, close to its searched form, in each zone;
everywhere else the text uses other forms and synonyms.

| Zone | Rule | Example for «диван-кровать» |
|---|---|---|
| `title` | phrase first, then the benefit or qualifier; brand at the end after a separator | «Диваны-кровати с ортопедическим матрасом — Магазин» |
| `H1` | phrase in natural grammar; may differ from the title | «Диваны-кровати» |
| `description` | phrase once + concrete offer + one number; a full sentence, not a list | «Диваны-кровати с ортопедическим матрасом: 120 моделей в наличии, доставка за 2 дня.» |
| lead (first ~120 words after H1) | phrase or a close form once, inside the first answer sentence | «Диван-кровать подходит для ежедневного сна, если у него…» |
| body | forms, synonyms, related terms; no exact repeats for their own sake | «модели с механизмом еврокнижка», «раскладной диван» |
| one H2 | a related query, often as a question | «Какой механизм дивана-кровати надежнее» |
| image alt | describes the image; contains the phrase only if the image shows it | «Диван-кровать в разложенном виде с матрасом» |

Commercial pages need the phrase in title, H1 and description; articles need it at least in the title or the H1.

## Counting repeats by lemma

Yandex lemmatises, so «диван», «дивана», «диванов» are one word to it. Count the main phrase by lemma: a window
where every content word of the phrase appears in any form, stop words ignored. The checker reports both counts:

```bash
node scripts/text-check.mjs article.md --phrase "диван кровать"
# exact: 2   by lemma: 9   per 1000 words: 4.1
```

- The limit comes from the on-page contract for the page type. Without it, treat more than one lemma occurrence per
  ~150 words of body as a reason to reread.
- A pillar page legitimately repeats its category word («ремонт» on the renovation hub). The signal is the full
  phrase repeated, especially in the same sentence shape, not the category noun alone.
- Never chase a count upward. Missing coverage is fixed by answering a sub-question in a new paragraph, not by
  inserting the phrase.

## Writing the metadata

Metadata is written per page in the searcher's words.

**Title.** Neither Yandex nor Google sets a character limit; both truncate by width and both rewrite titles that are
stuffed, templated, inaccurate or in another language than the page. Default limits when the project sets none: ≤ 60
characters visible, hard stop at 70.

- Specific: what the page gives, in the searcher's words. Not «Главная», not «Услуги».
- Sentence case: only the first word and proper names are capitalised.
- Brand once, at the end, after «—», «|» or «:».
- No year unless the content is about that year and will be updated.
- Unique across the site; a title template that only swaps one word is boilerplate.

**Description.** Yandex uses the meta description for the snippet when it fits the query. Default length: 120–160
characters, hard stop at 170. One or two sentences: what the reader gets plus proof (a number, a term, a guarantee);
the phrase once; no comma-separated keyword lists; only what the page actually shows.

**H1.** One per page, the most prominent heading, matching the title's intent. It can be longer and warmer than the
title.

**Open Graph title and description.** May be shorter and more social; keep the same promise.

## Headings and structure

Headings in Russian text follow the same structure rules as any page, plus Russian case conventions.

- Sentence case in every heading: «Как выбрать диван-кровать», not «Как Выбрать Диван-Кровать».
- H2s mirror real sub-queries people type («Сколько стоит…», «Чем отличается…», «Как выбрать…»). Each H2's first
  sentence answers it directly; quick answers and Alice AI quote such sentences.
- Heading levels never skip (H2 → H3), and no heading is used for styling.
- Lists for steps and options, tables for comparisons with three or more attributes, a short summary at the top of
  long articles («Коротко: …»).
- Paragraphs of one to four sentences; one idea each.

## Answering the query

The first screen decides whether the reader stays, and Yandex measures it through behaviour.

1. H1 restates the query in natural Russian.
2. The lead answers it in the first two sentences (definition, price range, verdict) before any background.
3. Proof follows immediately: a number, a case, a named source.
4. Then the depth: how, why, limits, alternatives.

Openers to delete: «В современном мире…», «Не секрет, что…», «В этой статье мы расскажем…», «Давайте
разберемся…». They delay the answer and are typical machine-text markers.

## Topical completeness without density

Search engines judge whether a page covers the topic the way experts do, not how often a word occurs. Build coverage
from the query's neighbourhood:

- Yandex suggestions and Wordstat top queries for the phrase: each recurring sub-question is a candidate H2 or
  paragraph.
- Terms the top pages share: entities (materials, standards, brands), numbers (цена, срок, гарантия) and the steps a
  buyer must understand.
- Objections the buyer has: risk, quality, delivery, cost of ownership.

Ignore «тошнота», «водность», density percentages, uniqueness percentages and "top-10 length targets": Yandex
publishes none of these numbers, and optimising them produces exactly the text its filters demote.

## Over-optimisation signs

Yandex's guidance on SEO texts names query spam, over-optimisation, hidden text and content without added value as
violations. In text they look like this:

| Sign | Example | Fix |
|---|---|---|
| Nominative query chains | «диван кровать купить недорого москва» | a grammatical sentence with one form |
| Same phrase in consecutive sentences | «Диван-кровать… Диван-кровать… Диван-кровать…» | a pronoun, a synonym, or merged sentences |
| City or industry swap pages | «Ремонт квартир в Казани» × 50 cities, same text | publish a city page only with unique proof (jobs, prices, reviews there) |
| Keyword list in a paragraph or footer | «диваны, диваны-кровати, угловые диваны, софы…» | delete; link to real pages instead |
| Phrase in every alt and every H2 | 8 of 8 H2s start with the phrase | change at most a few headings; vary them |
| Sentences that exist only for the robot | «Если вам нужен диван кровать купить недорого…» | delete |

Over-optimisation can hit one page or the whole host. Recovery is a rewrite for intent with fewer entries in title,
body and alt, not a synonym swap.

## Readability for a skimming reader

Readable Russian keeps a skimming reader on the page.

- Sentences mostly 8–20 words, mixed with short ones. Uniform 18–30-word sentences read as machine text.
- Verbs over nouns («ремонтируем», not «осуществляем проведение ремонта»).
- One term per concept across the article: once «диван-кровать», always «диван-кровать» (or a declared synonym),
  never a new word every paragraph for "variety".
- Numbers in digits for metrics, words up to ten in prose («три этапа»).

## Claims and numbers

Every claim in Russian commercial text must survive a reader's and a regulator's check.

- Every number has a source the editor can open: the company's own data, a named study with a date, an official
  statistic. Quote at most 15 words from a source; paraphrase the rest.
- Superlatives («лучший», «№1», «уникальный») are advertising claims under the advertising law (38-ФЗ): remove them
  or replace them with a provable number.
- Plans are not results; vendor claims are not facts; a pilot is not a rollout. Name what each number is.
