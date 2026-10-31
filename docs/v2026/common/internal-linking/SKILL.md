---
name: internal-linking
description: 'Designs site architecture and internal links so search engines find, understand and rank the important pages: hierarchy and hubs, click depth, URL structure, navigation, breadcrumbs, contextual links and anchor text, orphan pages, link audits from a crawl, and safe link placement rules. Use when planning a site structure or new section, when pages are orphaned or too deep, when choosing anchor text, or when deciding which pages should link to a new page.'
metadata:
  tags:
  - seo
  - internal-links
  - site-architecture
  - anchor-text
  - breadcrumbs
  - hubs
---

# Internal linking and site architecture

Internal links are the links between pages of the same site. They are how crawlers discover pages, how search
engines learn what a page is about (from anchor text and context), and how importance flows through a site. Unlike
backlinks, the site controls them completely.

## Step 0: read how the site links today

Read the site's link state first, because menus and templates decide most internal links and a fix there reaches every
page. Run a crawl that exports `source,target` pairs with click depth and status, and note which links come from a
template and which from editors. Then compare what the server sends with what the site says it has:

```bash
curl -s https://www.example.com/ | grep -oE '<a [^>]*href="[^"]*"' | wc -l     # links in the home page's server HTML
curl -s https://www.example.com/sitemap.xml | grep -o '<loc>' | wc -l          # pages the site lists
```

A low first number with a full menu on screen means the menu is built by JavaScript: read the rendered HTML in URL
Inspection before planning anything.

## Choose where an internal link goes

The right place for a link depends on how many pages need it and how much the words around it matter.

| Situation | Link from | Why the others lose here |
|---|---|---|
| A section matters across the whole site | main menu | contextual links reach only a few pages; the footer suits legal pages and a few hubs |
| Detail pages need a path up to their section | breadcrumbs, with `BreadcrumbList` markup | a menu cannot hold every level; related blocks do not show the hierarchy |
| A reader would want the target next | a contextual link with a descriptive anchor | navigation has no surrounding words to describe the target |
| A new or orphan page | its hub, plus three to ten related indexed pages | a sitemap entry gets it found, but passes on no context |
| A long list of items | a hub with crawlable pagination links | "load more" without `<a href>` hides everything past the first screen |
| A low-value page nobody needs | no new links; merge it or remove it | linking it spends template links on a page that should not rank |

## Site architecture: hierarchy and hubs

Site architecture is the shape of the link graph. A good default is a shallow hierarchy: home, then sections (hubs),
then detail pages, with sideways links between related pages.

```text
Home
├── /running-shoes/                hub: category or topic page
│   ├── /running-shoes/trail/      sub-hub
│   │   └── /running-shoes/trail/runner-x     detail
│   └── /running-shoes/road/
└── /guides/                       hub for articles
    └── /guides/choosing-trail-shoes  links up to /running-shoes/trail/ and to products
```

- Every page belongs to one hub; hubs link to all their children (with pagination if needed).
- Money pages are within three clicks of the home page. Depth is measured in clicks, not in URL folders.
- Topic clusters: an article hub covers one topic broadly and links to every narrower article; each narrower article
  links back to the hub and to the commercial page it supports.

## URL structure

URL structure helps people more than rankings, but stable, readable URLs avoid migrations later.

- Lowercase words joined by hyphens: `/running-shoes/trail/`. No IDs or dates unless the content needs them.
- Folders that match the hierarchy where it is stable; leave category folders out of product URLs when products move
  between categories (`/p/runner-x` or `/runner-x` beats a URL that changes with the menu).
- Never change a published URL without a 301 (`site-migrations`).

## Navigation and breadcrumbs

Navigation links appear on every page, so they decide which pages get the most internal links.

- Main menu: hubs only; a mega-menu with hundreds of links dilutes the signal and slows the page.
- Breadcrumbs on every page below a hub, as links, with `BreadcrumbList` markup (`structured-data`).
- Footer: legal, contact and a few key hubs; not a keyword list of links.
- Navigation must be `<a href>` links in the HTML, also on mobile (Google indexes the mobile version).

## Contextual links and anchor text

Contextual links inside body text carry the most meaning, because the words around them describe the target.

- Anchor text says what the target is: "trail running shoes with a rock plate", not "click here" or "read more".
- Vary anchors naturally; the same exact-match anchor from hundreds of pages looks generated.
- One link to a target per page is enough; extra links to the same URL add little.
- Link where a reader would want to go next, near the sentence that raises the question.
- Page that owns a search phrase: other pages that mention the phrase link to it with that phrase as the anchor
  (the owner rule in `keyword-research`).

<example>
Good: "For muddy routes, pick [trail shoes with 5 mm lugs](/running-shoes/trail/) and a gusseted tongue."
Bad: "Trail shoes are popular. [Click here](/running-shoes/trail/)."
Bad: a "Related searches" block with 40 links to keyword-stuffed tag pages.
</example>

## Link to a new page

A new page needs links from pages that are already crawled and relevant, on the day it is published.

1. Link it from its hub (and from the hub's listing or pagination).
2. Find three to ten related indexed pages: `site:example.com "trail shoes"` in Google, or the crawl's text search.
3. Add one contextual link from each, with a descriptive anchor.
4. Add it to the sitemap and, for Bing and Yandex, submit with IndexNow (`xml-sitemaps`).

## Audit internal links from a crawl

An internal link audit uses a crawl export with inlinks, outlinks, click depth and status per URL.

| Find | How | Fix |
|---|---|---|
| Orphan pages | URLs in sitemaps, analytics or Search Console with zero inlinks in the crawl | link from the hub and related pages, or remove |
| Deep money pages | click depth > 3 | link from hubs or the home page; flatten pagination |
| Links to redirects and 404s | inlinks whose target status is not 200 | update the link to the final URL |
| Weak important pages | money pages with fewer inlinks than low-value pages | move links from tag and archive pages to them |
| Link to non-canonical URLs | link target differs from its canonical | link the canonical |
| Nofollowed internal links | `rel="nofollow"` on internal links | remove: it hides your own pages |

A quick inlink count from a crawl CSV with `source,target` columns:

```bash
cut -d, -f2 links.csv | sort | uniq -c | sort -n | head -30     # pages with the fewest internal links
```

## Worked example: a guide hub that never ranked

Situation: 60 guides about trail running are indexed but get few impressions; the commercial category gets none of
their traffic.

Audit: the guides sit five clicks deep (blog pagination only), link to each other only through "Recent posts", and
never link the category. Fix: a `/guides/trail-running/` hub linked from the main menu's Running section, listing all
60 by sub-topic; each guide links up to the hub and, where a reader would buy, to the matching category with a
descriptive anchor; the category links back to the three most useful guides. Check: click depth 2 for every guide in
the next crawl; impressions per guide and clicks to the category from guides, eight weeks later.

## Verify

Verify internal links with a fresh crawl after the change, because it proves what a crawler can reach. Export `links.csv`
with `source,target` columns of absolute URLs, then compare it with the sitemap (for a sitemap index, read each child):

```bash
curl -s https://www.example.com/sitemap.xml | grep -oE '<loc>[^<]+' | cut -c6- | sort -u > listed.txt
cut -d, -f2 links.csv | sort -u > linked.txt
comm -23 listed.txt linked.txt                                    # expect nothing: listed pages with no internal link
while read -r u; do curl -s -o /dev/null -w "%{http_code} $u\n" "$u"; done < linked.txt | grep -v '^200'    # expect nothing
```

A line from the last command names a link target that redirects or fails. Then confirm in the crawl that money pages sit
within three clicks, and read impressions for the changed pages in Search Console over the next eight weeks.

## Checklist for internal linking

The internal linking checklist confirms important pages are easy to reach and clearly described.

1. Every indexable page has at least one internal link from an indexed page.
2. Money pages are within three clicks and receive more links than archive or tag pages.
3. Menus and breadcrumbs are crawlable `<a href>` links on mobile and desktop.
4. Anchors describe targets; no "click here"; no repeated exact-match anchors sitewide.
5. No internal links to redirects, 404s, parameters or non-canonical URLs.
6. New pages get hub and contextual links on publication day.

## Gotchas with internal links

The gotchas below are the internal linking mistakes that most often hide pages.

1. **JavaScript-only menus.** Symptom: a crawl from the raw HTML finds few pages. Cause: links render only on hover or
   click, so crawlers see none. Fix: put the menu in the HTML as `<a href>` links.
2. **Mobile menu with fewer links.** Symptom: sections lose rankings although the desktop menu looks fine. Cause:
   mobile-first indexing uses the mobile set. Fix: give both menus the same links.
3. **Tag pages outranking categories.** Symptom: a thin tag page shows for a query the category should own. Cause:
   every post links to every tag, so tags collect the most links. Fix: limit tags, or `noindex` thin ones.
4. **Faceted links everywhere.** Symptom: crawl goes to filter URLs and category pages feel diluted. Cause: thousands
   of filter links per category page eat crawl and dilute links. Fix: link only filters that have their own indexable
   page.
5. **Internal nofollow to "sculpt PageRank".** Symptom: a site adds `nofollow` and sees no gain, or pages fade. Cause:
   it does not move value elsewhere; it only drops it. Fix: remove it and cut the links you do not want.
6. **Sitewide footer link blocks.** Symptom: a footer of exact-match anchors to every service and city shows up in a
   review. Cause: such blocks are low value and look manipulative. Fix: keep legal, contact and a few key hubs.

## Anti-patterns in internal links

Anti-patterns in link structure spread links evenly where importance is not even.

| Do not | Do this instead |
|---|---|
| Linking to a redirect because the old URL still works | link the final URL |
| Using "click here" or "read more" as anchors | say what the target is |
| Repeating one exact-match anchor from hundreds of pages | vary anchors naturally |
| Burying money pages in blog pagination | link them from hubs, within three clicks of home |
| Publishing a page and adding links later | add hub and contextual links on publication day |

## See also for internal links

- `canonical-urls`: linking the canonical form of every URL
- `keyword-research`: the owner rule for anchors
- `site-migrations`: updating internal links after a move
- `seo-audit`: crawl exports and the full audit
- `programmatic-seo`: links at scale for generated pages
