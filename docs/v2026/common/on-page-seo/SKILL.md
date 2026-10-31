---
name: on-page-seo
description: 'Applies the on-page SEO contract every indexable page must meet and places target phrases on a page without over-optimising: title and meta description, one H1, H2 per section, the main phrase in title, H1, description and lead, repeat limits, server-rendered text, unique metadata, alt text, page-type requirements, a publish gate, and a table of real fixes versus fake fixes that only satisfy a checker. Use when optimising a page for a query, writing titles and meta descriptions, reviewing a page before publishing, handling keyword stuffing or thin pages, or deciding whether an SEO fix is real.'
metadata:
  tags:
  - seo
  - on-page
  - title-tag
  - meta-description
  - headings
  - content-optimisation
---

# On-page SEO contract

The on-page contract is what every indexable page must carry, and how target phrases are placed on it, so the page
ranks without over-optimisation. It is framework-agnostic. The phrase list comes from the `keyword-research` skill;
the brief and writing from `content-briefs`; JSON-LD and Open Graph from `structured-data`.

## Step 0: read what the page serves and what writes it

Read the served page first, because a CMS, a theme or a plugin may write the title and headings, and the fix belongs in
that template and not on the page.

```bash
curl -sL https://www.example.com/page | grep -ioE '<title[^>]*>[^<]*|<meta[^>]+name="(description|generator)"[^>]*>|<h1[^>]*>[^<]*|<link[^>]+rel="canonical"[^>]*>'
```

Then note the page's type, whether its text is in the server HTML, and which template or field sets each of these.

## Routing on-page tasks

On-page tasks start from the contract and branch by request.

| Task | Read |
|---|---|
| New page: what it must contain | the contract below, then [references/page-contract.md](references/page-contract.md) for the page type |
| Place a phrase list on an existing page | "Placement by tier" below |
| "Main phrase not in title", "keyword stuffing", "thin content" | the contract + [references/fake-fixes.md](references/fake-fixes.md) |
| Decide whether a proposed fix is real | [references/fake-fixes.md](references/fake-fixes.md) |
| Review a page before publishing | "Verify a page" below + the publish gate in the page contract reference |
| Images and alt text on the page | "Images on the page" below; image and video search: the `image-and-video-seo` skill |

## The contract

The contract gives defaults with a reason for each number. When the project's own SEO specification sets other
numbers, it wins; look for one first.

| Element | Rule | Why |
|---|---|---|
| title | unique; main phrase near the start; one concrete fact (price, term) when it fits; brand last; target ≤ 60 characters, hard max 70 | Google truncates by pixel width, near 60 characters; Bing and Yandex show a little more |
| meta description | unique; most useful fact first; main phrase once; 120–160 characters, hard max 170 | a full snippet when the engine uses it; engines often rewrite it from page text |
| H1 | exactly one; main phrase in natural grammar | the page's topic for readers and engines |
| lead (first paragraph) | answers the query; main phrase or a close form once | the first screen decides whether the visit continues |
| H2s | one per content section; each answers a sub-question | structure for readers and for passage ranking and AI answers |
| main phrase in body | exact sequence ≤ 3; other forms and synonyms elsewhere | keyword stuffing is judged on repeats written for robots |
| canonical | absolute, self-referencing, the final URL | one URL per document (`canonical-urls`) |
| robots | indexable on published pages; `noindex` until publication | unfinished pages never enter the index |
| text delivery | title, H1, H2s, lead, body and FAQ answers in the server HTML | engines index server HTML first; client-only text may be missed |
| uniqueness | no two pages share a title, description or main phrase | duplicates and cannibalisation |
| word minimum | coverage check by type (service 800, article 800, news 600, case study 450; hubs and utility pages exempt) | catches thin pages; never a reason to pad |

Google rewrites titles it finds stuffed, boilerplate, inaccurate or missing, and builds most snippets from page text.
A precise title and a lead that answers the query are what control the result's text. Diagnosing a title link, site name or snippet that Google already rewrote is the `search-appearance` skill.

## Placement by tier

A phrase list from keyword research comes with tiers. Place phrases top-down, once each.

| Tier | Slot | Example |
|---|---|---|
| main | title, H1, description, lead (contract above) | "Trail running shoes" |
| A or strategic | one weighty spot: an H2, the lead, a card title, or an FAQ question | H2 "How much do trail running shoes cost?" |
| B | one body sentence or FAQ answer; word forms welcome | "...a trail shoe with a rock plate costs more..." |
| C | only where a sentence fits naturally; otherwise skip silently | — |
| owned by another page | never targeted; one natural link to the owner page with the phrase as anchor | "see our [waterproof trail shoes](/running-shoes/trail/waterproof/)" |

Limits that keep it a placement, not a rewrite: change at most about 40% of the page's H2s, add at most four FAQ
items, never change facts, prices, terms or the order of sections. A phrase that can only be placed with a fact the
business does not have is skipped with "needs fact".

<example>
Good H2: "Waterproof trail shoes: when the membrane is worth it" (phrase plus a promise of content).
Bad H2: "Waterproof trail shoes best waterproof trail running shoes 2026" (a list of keywords).
Good FAQ: "How long do trail running shoes last?" answered with "Most last 500–800 km; check the lugs..."
Bad FAQ: "Trail shoes price cost buy?"
</example>

## Images on the page

Images on an indexable page follow four rules that need no separate tool. Content images are `<img>` elements with
a `src`, `width` and `height`; the file name describes the image; `alt` says in about 5–15 words what the image shows
(empty `alt=""` for decoration); any text inside an image, such as a price or a chart value, is also in the HTML.
Getting images and video into image and video search is the `image-and-video-seo` skill.

## On-page workflow

The on-page workflow compares the built page with the contract and fixes only what is real.

1. **Read the page as built**, not as remembered: fetch the HTML (production or a local build) and extract title,
   description, H1, H2s, canonical, robots and word count ("Verify a page" below).
2. **Read the inputs**: the page's main phrase and tiered list, the source of facts (offer, prices), the project's
   SEO specification.
3. **Compare with the contract**; list each violation with the element, the actual value and the rule.
4. **Fix with real fixes only** ([references/fake-fixes.md](references/fake-fixes.md)).
5. **Verify** on the rebuilt HTML; every validation line in the fake-fixes reference must hold.

## Verify a page

The verification extracts the contract fields from the built HTML. The `seo-audit` skill's `page_check.py` does it
in Python. When the file is not on disk (a pack install), read this script from the library that served this page and save it first.
The Node one-liner below needs Node 18 or later and no packages:

```bash
curl -s https://www.example.com/page | node -e '
const h=require("fs").readFileSync(0,"utf8");
const g=(re)=>(h.match(re)||[])[1]||"";
const strip=(s)=>s.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim();
const title=strip(g(/<title[^>]*>([\s\S]*?)<\/title>/i));
const desc=g(/<meta[^>]+name="description"[^>]+content="([^"]*)"/i);
const h1=[...h.matchAll(/<h1[^>]*>([\s\S]*?)<\/h1>/gi)].map(m=>strip(m[1]));
const h2=[...h.matchAll(/<h2[^>]*>([\s\S]*?)<\/h2>/gi)].map(m=>strip(m[1]));
const main=strip((h.match(/<main[\s\S]*?<\/main>/i)||[h])[0]);
console.log({title,titleLen:title.length,desc,descLen:desc.length,h1,h2,
 canonical:g(/<link[^>]+rel="canonical"[^>]+href="([^"]*)"/i),
 robots:g(/<meta[^>]+name="robots"[^>]+content="([^"]*)"/i),
 words:main.split(" ").length});'
```

Count exact repeats of the main phrase in the page text:

```bash
curl -s https://www.example.com/page | sed 's/<[^>]*>/ /g' | tr 'A-Z' 'a-z' | grep -o "trail running shoes" | wc -l
```

Done means: no contract violation left, the validation lines hold, and each skipped phrase has a reason.

## Worked example: a category page stuffed with its main phrase

Request: the "trail running shoes" category of an outdoor shop sits on page two, and an SEO tool reports "low keyword
density". The tier list gives the main phrase and two A-tier phrases, and the project has no SEO specification of its
own, so the contract's defaults apply.

Reading the built page with the extraction in "Verify a page" gives this, compared with the contract:

| Element | Actual | Rule | Fix |
|---|---|---|---|
| title | "Trail Running Shoes \| Trail Shoes \| Best Trail Running Shoes 2026 \| Example Outdoor", 83 characters | ≤ 60 target, 70 hard max; one concrete fact | "Trail running shoes with 60-day returns \| Example Outdoor", 57 characters |
| description | missing | 120–160 characters, most useful fact first | "Trail running shoes for mud, rock and long days, fitted in store or at home, with 60-day returns and free UK delivery over £50.", 127 characters |
| H1 | two: the logo and "Shoes" | exactly one, main phrase in natural grammar | logo out of the H1; "Trail running shoes" |
| lead | none, the grid starts at once | answers the query | two sentences on how to choose by terrain, above the grid |
| main phrase in body | 9 exact repeats, 7 of them in a block below the grid | ≤ 3 exact | block cut to one sentence: 3 repeats, other forms elsewhere |
| canonical | `/running-shoes/trail/?sort=new` | self-referencing, final URL | `/running-shoes/trail/` |

The "low keyword density" report is a fake fix: it would have added repeats to a page that already had too many. The
A-tier phrases go into one H2 ("Waterproof trail shoes: when the membrane is worth it") and one FAQ question. Only two of
the page's six H2s change, and no price or fact does. The 60-day returns and free delivery figures came from the offer
file, so nothing needed a "needs fact" mark.

Check: the extraction on the rebuilt HTML shows a 57-character title, one H1 and a self-referencing canonical; the
repeat count prints 3. Search Console queries for the page are read four to six weeks later.

## Checklist for an indexable page

The page checklist is the publish gate in short form.

1. Title unique, main phrase near the start, ≤ 60 characters target.
2. Description unique, 120–160 characters, one fact, the phrase once.
3. One H1; H2 per section; no skipped heading levels.
4. Lead answers the query in the first two sentences.
5. Main phrase exact repeats ≤ 3; no sentence written only for robots.
6. Self canonical; indexable; in the server HTML.
7. Images sized, described and not carrying text that is missing from the HTML.
8. Links in from at least three related pages (`internal-linking`).

## Gotchas in on-page SEO

The gotchas below are the on-page mistakes that look like fixes but are not.

1. **Editing the source, checking the source.** Symptom: the fix "works" but production shows the old title. Cause:
   the title is set in two places (layout template, CMS field, plugin), or an SEO plugin overrides it. Fix: check the
   built HTML.
2. **Padding to a word minimum.** Symptom: 300 new words, no new answers, worse engagement. Cause: the minimum is a
   coverage check, not a target. Fix: add answers, or leave the page and note why.
3. **Doorway location or industry pages.** Symptom: 20 pages with the same text and a swapped word stay unindexed or
   draw an action. Cause: the pages have nothing of their own. Fix: publish one only with specific proof for that
   location or industry.
4. **Text behind client JavaScript.** Symptom: H2s exist in the browser but `curl` shows none. Cause: the text arrives
   only after scripts run. Fix: render on the server, and keep FAQ answers in the HTML even when collapsed.
5. **Two pages, one main phrase.** Symptom: rankings alternate. Cause: both pages target one query. Fix: keep one
   owner; the other links to it.
6. **Snippet promises the page does not keep.** Symptom: low CTR or quick returns. Cause: the description says more
   than the page does. Fix: mention only facts present on the page.
7. **Year in the title.** Symptom: readers and engines notice stale "2025" titles. Cause: the year was added without
   updating the content each year. Fix: update the content yearly, or drop the year.

## Anti-patterns in on-page SEO

Anti-patterns on a page satisfy a checker and leave the reader with nothing new.

| Do not | Do this instead |
|---|---|
| Repeating the phrase to reach a target count | keep exact repeats at 3 or fewer and use forms and synonyms |
| Rewriting a whole page to place a phrase | change at most about 40% of the H2s and at most four FAQ items |
| Inventing a fact to fit a phrase | skip the phrase with "needs fact" |
| Listing keywords in an H2 | write a heading that promises content |
| Using identical titles across a template | generate each from the page's own data |

## References for on-page SEO

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/page-contract.md](references/page-contract.md): requirements per page type, metadata details,
  headings, commercial blocks, server-rendered text, publish gate, framework mapping.
- [references/fake-fixes.md](references/fake-fixes.md): real versus fake fixes, the ignore list, the nine validation
  lines.

## See also for on-page SEO

- `keyword-research`: the phrase list and owner pages
- `content-briefs`: briefs and writing
- `structured-data`: JSON-LD and Open Graph
- `search-appearance`: title links and snippets Google rewrote
- `russian-language-seo`: the same work in Russian
