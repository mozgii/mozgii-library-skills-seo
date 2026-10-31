---
title: On-page contract details per page type
author: MOZGII, Inc.
lang: en
description: The full on-page contract per page type, metadata details, headings, commercial blocks, server-rendered text, the publish gate and where each element lives in common frameworks.
---

# On-page contract details per page type

The full on-page contract per page type, with commercial blocks, server-rendered text, the publish gate, and where
each element usually lives in common frameworks. Numbers are defaults; a project that sets its own writes them down
once and this file yields to it.

## Contents

1. Requirements per page type
2. Metadata details
3. Headings and sections
4. Commercial page blocks
5. Server-rendered text
6. Publish gate
7. Framework mapping

## Requirements per page type

Each page type has its own phrase zones, a coverage minimum and blocks it must contain.

| Type | Main phrase zones | Word minimum (coverage check) | Must also have |
|---|---|---|---|
| Service or product | title, H1, description, lead | 800 | price or range, timeline, what is included, proof (case, number), call to action, FAQ |
| Industry or location landing | title, H1, description, lead | 800 | at least one case or proof from that industry or place; specific tasks, not a word swap |
| Integration | title, H1, description, lead | 600 | what syncs in which direction, setup time, limits |
| Article | title or H1 (both preferred), lead | 800 | answer in the lead, sourced numbers, author, dates, related links |
| News | title or H1, lead | 600 | date of the event, source link, what it means for the reader |
| Case study | title, H1 | 450 | client type, task, solution, measured result with period, consent note |
| Comparison | title, H1, description | 800 | named criteria, a table, a verdict per situation |
| Hub or category | title, H1, description | 300 + cards | links to every child page, a short intro, FAQ where useful |
| Contacts, about, legal, navigation | brand or page name | exempt | contact details as text |

Word minimums catch thin pages; they are not ranking targets. A page that answers every buyer question in fewer words
passes with a one-line note.

## Metadata details

Metadata is written per page from the page's own content, never from a template that only swaps one word.

- **title**: unique; main phrase near the start; one concrete fact when it fits (price, term, count); brand last after
  " | " or " - " when it fits. Target ≤ 60 characters, hard max 70. Sentence case or the site's consistent style.
- **meta description**: unique; the most useful fact first; main phrase once; one soft call to action; no capitals
  for emphasis, no keyword lists. 120–160 characters, hard max 170.
- **canonical**: absolute, self-referencing, the final URL (no redirect, the site's trailing-slash rule).
- **robots**: indexable for published pages; `noindex` before publication and on utility pages; never `noindex` on a
  page that is in the sitemap.
- **html lang**: the page's language (`<html lang="en">`).
- Open Graph and JSON-LD: the `structured-data` skill.

## Headings and sections

Headings give the page a structure both readers and passage-level ranking use.

- Exactly one H1, the most prominent heading, consistent with the title's promise.
- Every content section opens with an H2; H3 only inside an H2; no skipped levels; no headings used for styling.
- H2s answer sub-questions; the first sentence under each answers its heading.
- When phrases are placed into an existing page, change at most about 40% of its H2s and add at most four FAQ items:
  more is a rewrite that needs its own decision.
- Every section carries a fact: a number, a term, a step, a name. A section without a fact is filler.

## Commercial page blocks

Commercial pages rank and convert on visible trust signals. Each service or product page shows, as text in the HTML:

- price or price range ("from" when it is a floor) and what it includes;
- timeline or delivery time;
- proof: a case with measured numbers, a client type, a guarantee in contract terms, reviews;
- contacts: phone with country or area code, email on the domain, address where relevant;
- the company's legal name and registration details (footer or contacts page, linked);
- a clear next step (call to action) above the fold and after the main content.

A snippet promising prices or contacts the page does not show loses the click.

## Server-rendered text

Search engines index the HTML the server returns first. Title, description, H1, all H2s, the lead, the main text,
navigation links and FAQ answers belong in that HTML:

```bash
curl -s https://www.example.com/page | grep -c '<h2'           # H2s present without JavaScript
curl -s https://www.example.com/page | grep -o '<h1[^>]*>[^<]*'  # H1 present without JavaScript
```

Text that appears only after client JavaScript (tabs filled by fetch, accordions rendered on click, text behind an
uncached loading boundary) may be indexed late or never.

## Publish gate

The publish gate keeps unfinished pages out of the index and gives new pages a fast start.

- Before publication: `noindex`, not in the sitemap, not linked from menus or other pages.
- On publication day: remove `noindex`, add the sitemap entry with the real date, add at least three internal links
  from related pages (`internal-linking`), notify Bing and Yandex with IndexNow (`xml-sitemaps`).
- After publication the URL never changes; if it must, a 301 from the old URL.

## Framework mapping

Each framework sets metadata in a known place; find the real place in the project before editing.

| Element | Usual place |
|---|---|
| Next.js (App Router) | `export const metadata` or `generateMetadata` in `app/<route>/page.tsx`; title template in `app/layout.tsx` (`title.template`, `title.absolute` to skip it); `app/sitemap.ts`; `app/robots.ts` |
| Nuxt | `useSeoMeta()` or `useHead()` in the page; `nuxt.config` `app.head` for defaults |
| Astro | props passed to a `<head>` layout component; `@astrojs/sitemap` |
| SvelteKit | `<svelte:head>` in `+page.svelte` with data from `+page.server.ts` |
| WordPress | the theme's `wp_head` plus an SEO plugin (Yoast, Rank Math); check which one writes the title |
| Shopify | `theme.liquid` `<title>` and `page_title`; product and collection SEO fields in the admin |

Search for the source of a title before changing it: `grep -rn "<title\|title:" src app --include=*.{ts,tsx,vue,astro,svelte,liquid,php}`.
