---
title: English to Russian translation for search
author: MOZGII, Inc.
lang: en
description: How to turn English articles and pages into Russian that reads as native and ranks for what Russians type - workflow, term choice by demand, term table, calques, formats, headlines, attribution and slugs.
---

# English to Russian translation for search

Translation for Russian search means localisation: the Russian page answers the Russian query; it does not mirror
English sentences. This file covers articles, research, product pages and video scripts.

## Contents

1. Workflow
2. Term choice by demand
3. Term table
4. Calques and English structures to rewrite
5. Formats: numbers, dates, money, units, names
6. Headlines and titles
7. Sources, quotes and attribution
8. URL slugs
9. Final checks

## Translation workflow

The translation workflow decides the Russian query before translating a sentence.

1. **Read the whole source first.** Decide the Russian page's query and intent; the English title is not the Russian
   title.
2. **Build the term sheet** (next section) before translating: every recurring concept gets one Russian term, chosen
   by demand.
3. **Translate meaning by paragraph**, not sentence by sentence. Merge, split or drop sentences when Russian needs it.
   Keep every fact, number and caveat.
4. **Localise the context**: replace US or EU-only examples, laws and prices with local equivalents when the page
   targets Russian-speaking markets, or state clearly that the fact is foreign («в США…»). Never present a foreign
   regulation as Russian.
5. **Run passes 2–5** of the skill on the Russian text as if it were original copy.

## Term choice by demand

Each key term is chosen by comparing quoted Wordstat frequencies of the candidates (or the free Wordstat copy, or
Yandex suggestions when no frequency source is available):

```text
"!смарт !часы"         vs  "!умные !часы"          vs  "!smart !watch"
"чат-бот"              vs  "чатбот"                vs  "бот"
"внедрение ии"         vs  "внедрение искусственного интеллекта"
```

- The higher-demand form goes into title, H1 and description; the other forms may appear in the body as synonyms,
  which also covers their queries.
- If demand is equal or unknown, prefer the Russian form (the state-language law for consumer text, and it reads
  native).
- Product and brand names stay as the owner writes them.
- Record the sheet in the article's front matter or brief so later edits keep the same terms.

## Term table

The term table gives default Russian terms for common web, business and technology vocabulary; check demand for the
ones that matter.

| English | Russian (default) | Note |
|---|---|---|
| AI | ИИ | «искусственный интеллект» once at first mention in long articles |
| AI assistant | ИИ-ассистент | «помощник» in plain-language copy |
| large language model | большая языковая модель (LLM) | abbreviation in parentheses on first use |
| neural network | нейросеть | |
| prompt | промпт, запрос | «запрос» for non-technical readers |
| workflow | процесс, сценарий | not «воркфлоу» |
| deployment | запуск, развертывание | |
| on-premise | на своих серверах | |
| use case | сценарий, пример применения | not «юзкейс» |
| case study | история клиента, кейс | «кейс» acceptable in body text |
| ROI | окупаемость, ROI | «окупаемость» in titles |
| lead | заявка, лид | «заявка» for buyers |
| conversion rate | конверсия | |
| checkout | оформление заказа | |
| shipping | доставка | |
| returns | возврат | |
| customer support | поддержка клиентов | |
| compliance | соответствие требованиям | name the law |
| data privacy | защита персональных данных | |
| enterprise | крупный бизнес | |
| SMB | малый и средний бизнес (МСБ) | |
| dashboard | панель, панель показателей | |
| landing page | страница, посадочная страница | not «лендинг» in consumer text |

## Calques and English structures to rewrite

Calques are English structures copied into Russian; each has a native rewrite.

| English pattern | Literal (wrong) | Native Russian |
|---|---|---|
| "X is a Y that…" | «X является Y, который…» | «X — это Y: …» or a verb sentence |
| passive "is used by" | «используется компаниями» | «компании используют» |
| "while" (contrast) | «в то время как» | «а», «но», «при этом» |
| "in order to" | «для того чтобы» at every turn | «чтобы» |
| "it is important to note that" | «Важно отметить, что» | state the fact |
| "solution" for anything | «решение» | name it: программа, сервис, услуга |
| "provide" | «предоставлять» | «давать», «дает» |
| "allow to" | «позволяет осуществлять» | a direct verb |
| "a number of" | «целый ряд» | «несколько», a number |
| possessive chains | «эффективность работы отдела продаж компании» | split: «как работает отдел продаж» |
| Title Case Headline | «Как Выбрать Диван Для Сна» | «Как выбрать диван для сна» |
| "you" capitalised | «Вы» | «вы» (site register) |

## Formats: numbers, dates, money, units, names

Russian formats differ from English ones in separators, order and units.

| Item | English | Russian |
|---|---|---|
| Thousands and decimals | 1,500,000.5 | 1 500 000,5 (no-break space U+00A0 from ru-RU `Intl`) |
| Millions and billions | $5M, 2.3B | 5 млн долларов or $5 млн; 2,3 млрд |
| Date | October 11, 2026 or 10/11/2026 | 11 октября 2026 or 11.10.2026 |
| Range | 5-7 days | 5–7 дней (en dash, no spaces) |
| Percent | 40% | 40% (keep the site's convention) |
| Currency conversion | — | keep the original currency; add the ruble equivalent only with the rate date |
| Units | miles, °F, lbs | km, °C, kg (keep the original in parentheses for quotes) |
| Names | a person's name | the established Russian spelling; Latin in parentheses on first mention when the person is not widely known |
| Companies | foreign company names | Latin, no quotes; Russian legal forms in quotes: ООО «Ромашка» |

## Headlines and titles

English headlines rely on wordplay, Title Case and teaser structure that Russian results punish. Rewrite from the
Russian query (transcreation):

| English headline | Literal | Russian for search |
|---|---|---|
| "Your Sofa Is Lying to You" | «Ваш диван вам лжет» | «Как понять, что диван пора менять: 6 признаков» |
| "The 7 Mistakes That Ruin a Kitchen Remodel" | «7 ошибок, которые губят ремонт кухни» | «7 ошибок при ремонте кухни и как их избежать» |
| "Why Most Kitchen Renovations Go Over Budget" | «Почему большинство ремонтов кухни выходят за рамки бюджета» | «Ремонт кухни дороже сметы: пять причин» |

The title carries the query; the headline voice may stay in the H1 or the lead.

## Sources, quotes and attribution

Sources stay traceable through translation.

- Keep every source link; add the publisher and date in Russian: «по данным исследования (август 2026)».
- Quotes: translate, mark as a translation if wording matters, keep at most 15 words from the original.
- Numbers from the source are rechecked against the original, not against the translation.
- A claim the source attributes to a vendor stays attributed («по словам компании»).

## URL slugs

Slugs are transliterated Russian, not English. Derive the site's scheme from its existing URLs before writing a new
slug, because one site must use one scheme. Look for й, х, щ, ц, ж, я, ю, ь in the sitemap to see how they are
written.

A common Yandex-style scheme (verify against the site):

```text
а a, б b, в v, г g, д d, е/ё e, ж zh, з z, и i, й j or y, к k, л l, м m, н n, о o, п p, р r, с s, т t, у u, ф f, х h,
ц c, ч ch, ш sh, щ shh, ъ (drop), ы y, ь (drop), э e, ю yu, я ya
```

- Lower case, words joined by hyphens, digits kept (`7-oshibok-pri-remonte-kuhni`).
- Drop stop words only when the slug stays readable; keep the query words.
- A published slug never changes; if it must, add a 301.

## Final checks for a translation

The final checks confirm the translation is consistent and in Russian formats.

- Every term from the term sheet is used consistently.
- No English left except names, product names and accepted abbreviations.
- Numbers, dates and units are in Russian formats.
- `node scripts/text-check.mjs <file> --phrase "<main phrase>"` exits 0.
