---
name: russian-language-seo
description: 'Writes, edits and localises Russian-language text that must rank in Yandex and Google and read as written by a native professional: articles, service and product copy, title, description, H1, headings, FAQ, alt text and slugs. Places the main phrase in the right zones, counts repeats by lemma the way Yandex does, avoids over-optimisation filters, removes bureaucratic and machine-sounding Russian, applies Russian typography, 168-FZ and 38-FZ wording rules, and translates English material for Russian search with a lint script. Use for напиши SEO-текст, перепиши текст, метатеги, переспам, канцелярит, звучит как нейросеть, переведи или локализуй статью, translate into Russian for the blog.'
metadata:
  tags:
  - seo
  - russian
  - yandex
  - copywriting
  - translation
  - typography
  - 168-fz
---

# Russian-language SEO text

Russian SEO text has to satisfy two readers: a search engine that matches every word form of a query, and a native
reader who leaves at the first sentence that sounds like a robot or a bureaucrat. This skill is one pass for any
search-facing Russian text, including English material localised for Russian readers. Page-level rules (word
minimums, how many headings may change) belong to `on-page-seo`; choosing the phrase belongs to `keyword-research`
and `yandex-wordstat`.

## Step 0: read the site's language conventions and the tools

Read a published page and the checker first, because the site's own usage wins over the defaults in this skill. The commands
confirm Node, confirm the checker runs, and show the page's declared language and whether it writes ё.

```bash
node --version                                                     # expect 18 or later
node scripts/text-check.mjs --help
curl -sL https://www.example.ru/uslugi/ | grep -ioE '<html[^>]+lang="[^"]*"'
curl -sL https://www.example.ru/uslugi/ | grep -o 'ё' | wc -l      # 0 on a long page: the site writes е
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

## Routing Russian text tasks

Russian text tasks follow the passes in order; smaller requests use part of them.

| Task | Do | Read |
|---|---|---|
| New article or page text for a target query | passes 0–5 in order | [references/seo-language.md](references/seo-language.md), then the two style references |
| Title, description, H1, lead only | pass 0, the metadata part of pass 2, passes 4–5 | [references/seo-language.md](references/seo-language.md) |
| Translate or localise English material | translation workflow, then passes 2–5 | [references/translation.md](references/translation.md) |
| Fix an over-optimised or machine-sounding text | pass 5 first (to see the failures), then passes 2–4 | [references/editing-passes.md](references/editing-passes.md) |
| URL slug for a new Russian page | "Slugs" below | [references/translation.md](references/translation.md) |
| Legal pages (privacy, terms) | skip: legal wording governs | — |

## Pass 0: inputs

The inputs below decide every later pass, so collect them before writing a word.

- **Main phrase**: the one query this page owns (from the brief or keyword plan). One page, one main phrase.
- **Intent**: informational (answer, definition, how-to), commercial (price, service, contractor), comparison. The
  intent decides what the lead must answer.
- **Page type**: article, service, category, case study, news; limits per type come from `on-page-seo`.
- **Proof available**: numbers, cases, sources with dates. Text without proof turns into filler.
- **Site conventions**: read two or three published pages of the same type for terms, tone, heading style, ё usage
  and slug scheme. The site's own usage wins over the defaults here.

If the main phrase or intent is missing, ask once; do not invent a target.

## Pass 1: meaning

The meaning pass writes the answer before the prose.

1. H1: the query in natural Russian.
2. Lead: the answer in the first two sentences (definition, price range, verdict, timeline).
3. Proof right after: a number, a case, a named source with a date.
4. H2 outline from real sub-questions (suggestions, «люди также ищут», the buyer's objections); each H2 answers one,
   in its first sentence.

Cut every paragraph that answers nothing. «В современном мире…», «Не секрет, что…» and «В этой статье мы
расскажем…» delay the answer; delete them.

## Pass 2: search layer

The search layer places the query in Russian that a person would write. Full rules with examples:
[references/seo-language.md](references/seo-language.md).

**Russian morphology.** Yandex matches all word forms and ignores stop words unless the query fixes them (`!` fixes a
form, `+` a preposition, quotes the word count, `[]` the order). So write grammatical Russian: «как сделать ремонт
квартиры под ключ» serves the query «ремонт квартира под ключ как сделать»; the query chain itself is never a
sentence.

**Zones.** The main phrase appears once, in its searched form or close to it, in each zone; other places use other
forms and synonyms.

| Zone | Rule |
|---|---|
| title | phrase first, then the benefit; brand last after «—», «\|» or «:» |
| H1 | phrase in natural grammar; one H1 per page |
| description | phrase once + a concrete offer + one number; a sentence, not a list |
| lead (first ~120 words) | phrase or a close form inside the first answer sentence |
| one H2 | a related query, often as a question |
| body, alt | forms and synonyms; alt describes the image |

**Repeats are counted by lemma.** «диван», «дивана», «диванов» are one word to Yandex. Count the phrase across all
forms; when the body carries it more than about once per 150 words, reread for stuffing.

**Metadata defaults** (when the project sets none): title ≤ 60 characters visible, never over 70; description
120–160, never over 170. Sentence case, unique per page, only promises the page keeps.

```text
title:       Ремонт квартир под ключ в Москве: смета за один день — Компания
H1:          Ремонт квартир под ключ
description: Делаем ремонт квартир под ключ: смета за один день, фиксированная цена
             в договоре, гарантия три года. Сроки от 45 дней.
lead:        Ремонт квартир под ключ включает черновые и чистовые работы, закупку
             материалов и вывоз мусора. Двухкомнатную квартиру сдаем за 60–75 дней.
```

**Compounds and case.** Hyphenated compounds («интернет-магазин», «ИИ-помощник») keep a plain hyphen (U+002D):
Yandex splits it like a space. A non-breaking hyphen (U+2011) may not split the same way, so prevent line breaks in
markup instead. Abbreviations such as «ИИ» stay upper case.

**Russian or Latin term** («ИИ» or «AI», «смартфон» or «smartphone»): choose by measured demand
([references/translation.md](references/translation.md)); with equal demand choose Russian.

**Over-optimisation.** Yandex treats query spam, over-optimisation, hidden text and content without added value as
violations, page-level or host-level (the Baden-Baden filter in `yandex-seo`). Density, «тошнота», «водность» and
uniqueness percentages are not targets; Yandex publishes none of them, and chasing them produces the text its filters
demote.

## Pass 3: register and typography

The register and typography pass makes the text read like a professional Russian site. Full rules:
[references/typography-and-register.md](references/typography-and-register.md). The ones that most often break
search-facing text:

- «вы» in lower case; verbs over nouns; one idea per sentence; numbers first.
- No unproven superlatives («лучший», «№1», «уникальный»): advertising claims that need proof under the advertising
  law (38-ФЗ).
- Quotes «ёлочки» (nested „лапки“), ranges with an en dash `5–7 дней`, a no-break space between number and unit and
  after short prepositions, `₽` after the number, `…` as one character.
- Plurals on dynamic numbers through `Intl.PluralRules`; numbers and money through `Intl`.
- Russian words in consumer-facing text (срок, not дедлайн; панель, not дашборд) under the state-language law
  (168-ФЗ, amended rules in force from 1 March 2026); keep CRM, API and trademarks.
- Headings in sentence case: only the first word and proper names capitalised.

## Pass 4: natural Russian

The natural-Russian pass removes the bureaucratic and machine patterns readers notice first. Full rules:
[references/editing-passes.md](references/editing-passes.md). Three passes in order:

1. **Orthography**: by default е instead of ё in common words (Yandex matches е and ё alike, so е never costs
   ranking); keep ё in names (Фёдор, Артём) and where the meaning would be ambiguous. Follow the site if it uses ё
   consistently.
2. **Vocabulary**: данный → этот; remove «является»; осуществлять → the direct verb; функционировать → работать;
   the chancellery list (в рамках, ввиду того, следует отметить, таким образом…).
3. **Structure**: em dash only for «подлежащее — сказуемое»; active voice; нужно or можно instead of следует,
   необходимо, рекомендуется; varied sentence length; at most one participial phrase per sentence.

## Pass 5: verify with the checker

The checker lints a Markdown or text file (optional front matter `title` and `description`) and counts the main
phrase by lemma across the zones. It needs Node 18 or later and no packages:

```bash
node scripts/text-check.mjs content/remont-kvartir.md --phrase "ремонт квартир под ключ" --max 3
# phrase «ремонт квартир под ключ»: exact 1, by lemma 4, per 1000 words 3.8, words 1050
#   title: yes  h1: yes  description: yes  lead: yes
# PASS: 0 fail, 2 warn
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

- Exit 0 means pass. Every `FAIL` line is fixed before the text ships; each `WARN` is fixed or justified in one line.
- It checks chancellery words, machine-text openers, 168-ФЗ loanwords, 38-ФЗ claims, ё, U+2011, three dots,
  straight quotes, capital «Вы», em-dash density, Title Case headings and title, H1 count, heading jumps, title and
  description length, and the main phrase by lemma (`--max N` sets the page's repeat limit).

For text inside JSX or TSX files, grep the source as well:

```bash
grep -rnE 'ё' src --include='*.tsx'                                   # expect none in user text
grep -rnoE '\b(софт|фикс-прайс|дедлайн|фидбэк|митинг|лендинг|онбординг|саппорт|апдейт|дашборд|воркфлоу)\b' src --include='*.tsx'
grep -rnE '"[^"]*\b[0-9]+ (дней|дня|день)\b' src --include='*.tsx'      # hard-coded plurals on dynamic values
```

Then read the title, the lead and every H2 aloud. If a sentence exists only for the robot, delete it.

## Worked example: a page text for «ремонт квартир под ключ»

Request: a service page for a Moscow renovation firm. The main phrase is «ремонт квартир под ключ», the intent is
commercial, and the proof on hand is 64 finished projects in 2025 and a price from 28,000 roubles per square metre.

Pass 1 replaces the old opening with the answer, and pass 3 and pass 4 strip the chancellery tone:

```text
Было:  В современном мире осуществление ремонта квартир под ключ является актуальной задачей.
       Наша компания предоставляет услуги ремонта квартир под ключ на высоком уровне.
Стало: Ремонт квартир под ключ стоит от 28 тысяч рублей за квадратный метр и занимает 10–14 недель
       для квартиры 50 м². В цену входят черновые и чистовые работы, материалы и вывоз мусора.
```

The new lead answers price and time in its first sentence, and the old one gave no fact at all. Pass 2 puts the exact
phrase in the H1 and the lead, and uses other forms in the H2s: «Сколько стоит ремонт квартиры 50 м²», «Сколько длится
ремонт под ключ». Proof follows at once: «В 2025 году мы сдали 64 объекта».

The first checker run stops on three words:

```bash
node scripts/text-check.mjs remont-etapy.md --phrase "ремонт квартир под ключ" --max 3
# phrase «ремонт квартир под ключ»: exact 1, by lemma 1, per 1000 words 8.1, words 124
#   title: yes  h1: yes  description: yes  lead: yes
# FAIL ё in common words: счёт, ещё, твёрдая → е
# FAIL: 1 fail, 0 warn
```

The site writes е, so the three words change and the second run exits 0 with `PASS: 0 fail, 0 warn`. Then the title,
lead and H2s are read aloud, and no sentence exists only for the robot.

## Translation from English

Translation for Russian search is localisation: the Russian page answers the Russian query. Full workflow and term
table: [references/translation.md](references/translation.md). The rules that decide ranking:

1. Decide the Russian query and intent first; the English title is not the Russian title.
2. Build a term sheet before translating: one Russian term per concept, chosen by demand.
3. Translate meaning by paragraph; keep every fact, number and caveat; localise examples or mark them as foreign.
4. Rewrite calques: «является», passive voice, «в то время как», «решение» for everything, Title Case headlines.
5. Russian formats: `1 500 000,5`, `11 октября 2026`, `5–7 дней`, `5 млн долларов`; metric units; established
   Russian spelling of names.
6. Then passes 2–5 as for original text.

<example>
English: "Why Most Kitchen Renovations Go Over Budget"
Literal: «Почему большинство ремонтов кухни выходят за рамки бюджета»
For search: «Ремонт кухни дороже сметы: пять причин и как их избежать» (the query words first, a Russian sentence,
sentence case, no calque «выходят за рамки бюджета»).
</example>

## Slugs for Russian pages

Slugs are transliterated Russian, not English. Derive the scheme from the site's existing URLs (the sitemap or the
content folder) and reuse it, so one site has one transliteration. Lower case, hyphens, digits kept, query words kept;
a published slug never changes without a 301. A common Yandex-style scheme is in
[references/translation.md](references/translation.md).

<example>
Title «Как выбрать подрядчика для ремонта» on a site whose URLs read `remont-kvartir`, `smeta-za-den`, `pod-klyuch`
gives the slug `kak-vybrat-podryadchika-dlya-remonta` (ы→y, я→ya, й→j).
</example>

## Checklist for Russian SEO text

The checklist below is the minimum before a Russian text ships.

1. Main phrase and intent known; the lead answers the query in two sentences.
2. Phrase once in title, H1, description and lead, in natural grammar; body uses forms and synonyms.
3. Lemma count within the limit (`text-check.mjs --max`); no query chains as sentences.
4. Typography: «ёлочки», en-dash ranges, no-break spaces, `₽` after numbers, sentence-case headings.
5. No данный, является, осуществлять; no filler openers; varied sentence length.
6. No unproven superlatives; loanwords replaced where a Russian word exists.
7. `text-check.mjs` exits 0; the title, lead and H2s read aloud without a robot sentence.

## Gotchas in Russian SEO text

The gotchas below are specific to Russian and Yandex.

1. **Query chains in text.** Symptom: «ремонт квартир под ключ цена недорого позволяет…» sits in a sentence and reads
   as broken Russian. Cause: the writer wrote to the query string instead of the reader. Fix: write one grammatical
   sentence; Yandex matches the forms anyway.
2. **Counting only exact matches.** Symptom: the checker says 2 repeats, the page still drops. Cause: Yandex
   lemmatises; 14 inflected repeats are 14 repeats. Fix: count by lemma.
3. **Category word flagged as stuffing.** Symptom: «ремонт» ×22 on the renovation hub is reported as spam. Cause: stem
   counters cannot tell a topic noun from a stuffed phrase. Fix: judge the full phrase and its sentence shape.
4. **U+2011 in compounds.** Symptom: «интернет‑магазин» stops matching «интернет магазин» Cause: a typography plugin
   swapped the hyphen. Fix: use a plain hyphen in text and `nowrap` in markup.
5. **Literal translation of the query term.** Symptom: a translated article ranks for nothing. Cause: the English term
   was translated, not looked up. Fix: compare demand per candidate term before writing the title.
6. **Title Case from English sources.** Symptom: «Как Выбрать Подрядчика Для Ремонта» appears in headings and the
   checker fails it. Cause: English title habits carried over. Fix: use sentence case.
7. **Snippet promises the page does not keep.** Symptom: the description mentions prices, an address or a timeline the
   page lacks. Cause: the description was written apart from the page. Fix: mention only what is on the page.
8. **Density targets from text-analysis services.** Symptom: padding and keyword lists appear in the text. Cause: a
   service's score became the goal. Fix: cover sub-questions and proof instead, and ignore the scores.

## Anti-patterns in Russian SEO text

Anti-patterns in Russian text come from writing for a text-analysis service and not for a person.

| Do not | Do this instead |
|---|---|
| Chasing «тошнота», «водность» or uniqueness percentages | cover the reader's questions; Yandex publishes none of these numbers |
| Using ё inconsistently across a site | follow the site's usage, or е by default with ё in names |
| Translating a heading word for word | start from the Russian query |
| Using «лучший» or «№1» without proof | state the number or the fact behind the claim |
| Filling text with loanwords where a Russian word exists | use the Russian word in consumer-facing text and keep CRM, API and trademarks |

## References for Russian SEO text

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/seo-language.md](references/seo-language.md): morphology and operators, zones, lemma counting,
  metadata, headings, answering the query, topical completeness, over-optimisation signs, claims.
- [references/translation.md](references/translation.md): EN→RU workflow, demand-based term choice, term table,
  calques, formats, headlines, attribution, slugs.
- [references/typography-and-register.md](references/typography-and-register.md): register, typography, plurals,
  168-ФЗ vocabulary, section templates.
- [references/editing-passes.md](references/editing-passes.md): orthography, vocabulary and structure passes with
  full replacement tables.
- `scripts/text-check.mjs`: the pass 5 checker.

## See also for Russian SEO text

- `yandex-wordstat`: exact frequency for each candidate term
- `yandex-seo`: filters and Yandex Webmaster
- `on-page-seo`: page limits and heading rules
- `keyword-research`: choosing the main phrase
- `international-seo`: hreflang and localisation
