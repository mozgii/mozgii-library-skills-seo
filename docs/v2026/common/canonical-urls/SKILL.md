---
name: canonical-urls
description: 'Fixes duplicate content and makes every document resolve to one canonical URL: rel=canonical rules, protocol, host and trailing-slash normalisation, URL parameters, pagination, faceted navigation, syndicated copies, and why Google picks a different canonical than the one declared. Use when Search Console reports duplicates or ''Google chose different canonical'', when the same page answers on several URLs, when setting canonical tags in a template, or when deciding between canonical, redirect and noindex.'
metadata:
  tags:
  - seo
  - canonical
  - duplicate-content
  - pagination
  - parameters
  - technical-seo
---

# Canonical URLs and duplicate content

A canonical URL is the one address a search engine indexes for a document that is reachable at several. Duplicate
URLs are normal (tracking parameters, sort orders, print views, http and https) and are not penalised; the cost is
that crawling and ranking signals spread across copies, and the engine may index a copy you did not want.

## Step 0: read how the site answers today

Read the URL variants and the tags first, because the fix depends on what the site already does. Run this on the home
page and on one URL per template:

```bash
for u in http://example.com/shoes/ http://www.example.com/shoes/ https://example.com/shoes/ https://www.example.com/shoes/ https://www.example.com/shoes; do
  curl -sIL -o /dev/null -w "$u -> %{url_effective} %{http_code} (%{num_redirects} hops)\n" "$u"
done
curl -sL https://www.example.com/shoes/ | grep -ioE '<link[^>]+rel="?canonical"?[^>]*>'
curl -sI https://www.example.com/shoes/ | grep -i '^link:'
```

Every variant should end on one URL in one hop, and the tag should name that URL. Then find what writes the canonical
(a CMS setting, a plugin, a framework helper, a template), and read "Google-selected canonical" in URL Inspection for
three URLs of each template.

## How search engines choose the canonical

Search engines choose the canonical from several signals; `rel="canonical"` is a strong hint, not an order. Google
weighs, roughly from strongest: redirects, `rel="canonical"` (in HTML or the HTTP header), sitemap inclusion,
internal links, hreflang, https over http, and shorter, cleaner URLs. When signals disagree, Google picks its own,
and Search Console shows "Duplicate, Google chose different canonical than user". The fix is to make every signal
point to the same URL.

## Choose the right tool: redirect, canonical or noindex

Redirects, canonicals and noindex solve different duplicate problems.

| Situation | Use | Why |
|---|---|---|
| The old URL should not exist for users either | 301 to the canonical | strongest signal; users land on the right page |
| Both URLs must work for users (tracking, sort, print, variants) | `rel="canonical"` to the main URL | users keep their view, signals consolidate |
| The page must not be in search at all | `noindex` | removes it; does not pass signals reliably |
| A non-HTML file (PDF) duplicates an HTML page | `Link: <https://...>; rel="canonical"` header | HTML tags cannot be added |
| Content syndicated to another site | ask the partner to block indexing of its copy with `noindex` | Google does not recommend canonicals for syndication, because the copies often differ, and may otherwise pick the bigger site |

Never combine `noindex` with a canonical to another URL: the two signals contradict each other.

## Canonical tag rules

The canonical tag works when it follows these rules every time.

```html
<link rel="canonical" href="https://www.example.com/shoes/trail-runner">
```

- Absolute URL with protocol and host; relative URLs work but break when content is copied or proxied.
- In the `<head>` of the server HTML; one per page; not injected late by JavaScript.
- Points to a URL that answers 200, is indexable and is not itself canonicalised elsewhere (no chains).
- Every indexable page has a self-referencing canonical, which defends against parameter copies.
- The canonical URL is the one used in internal links, sitemaps and hreflang.
- HTTP header form, for PDFs and other files: `Link: <https://www.example.com/guide>; rel="canonical"`.

## Normalise protocol, host, slash and case

URL normalisation removes duplicates at the server, before any tag is needed. Pick one form and 301 every other form
to it in one hop:

```nginx
server {
  listen 80;
  server_name example.com www.example.com;
  return 301 https://www.example.com$request_uri;
}
server {
  listen 443 ssl;
  server_name example.com;
  return 301 https://www.example.com$request_uri;
}
```

Trailing slash: choose `/shoes/` or `/shoes` for directory-like URLs and redirect the other. Case: paths are
case-sensitive; redirect upper-case variants to lower case when the platform allows them. Index files:
`/index.html` and `/` are two URLs; redirect one.

New URLs follow one shape from the start. Separate words with hyphens, not underscores and not run together
(`/green-dress`, never `/green_dress` or `/greendress`); use one case; percent-encode non-ASCII characters in links;
and never change content with a `#fragment`, which Google Search generally does not support.

## URL parameters

URL parameters create duplicates when they change tracking or presentation but not content. Search Console's URL
Parameters tool was retired in 2022, so handle them on the site:

| Parameter type | Example | Handle |
|---|---|---|
| Tracking | `?utm_source=`, `?gclid=`, `?fbclid=` | self canonical on the clean URL; never link internally with them |
| Sort and view | `?sort=price`, `?view=grid` | canonical to the unsorted URL |
| Session | `?sid=` | remove: use cookies |
| Filter that creates a page worth ranking | `/shoes/trail/` | a clean path with its own canonical (`ecommerce-seo`) |
| Filter without search demand | `?color=red&size=9` | canonical to the category, or block crawling when volume is huge |
| Pagination | `?page=2` | self canonical (see below) |

Keep parameter order fixed in generated links (`?color=red&size=9`, never also `?size=9&color=red`).

## Pagination

Paginated series need each page to be indexable and linked, because items on page 5 are found only through page 5.

- Each page has a self canonical (`/shoes/?page=2` canonicalises to itself), not to page 1.
- Pages link to each other with plain `<a href>` links; page 1 is the clean URL without `?page=1`.
- Google has not used `rel="next"` and `rel="prev"` since 2019; they do no harm and other engines may read them.
- Infinite scroll and "load more" also expose paginated URLs that work without JavaScript.
- A "view all" page can be the canonical for the series only when it loads fast enough to be the page users get.

## Find duplicates on a site

Duplicates are found by grouping URLs that return the same content. In a crawl export, group by title plus H1, or by a
hash of the main text; in Search Console, read the three "Duplicate" reasons in the Page indexing report and inspect
examples with URL Inspection ("User-declared canonical" against "Google-selected canonical").

Check what one variant declares, from the HTML and the HTTP header:

```bash
URL="https://www.example.com/shoes/?utm_source=news"
curl -sL "$URL" | grep -ioE '<link[^>]+rel="canonical"[^>]*>'
curl -sIL "$URL" | grep -iE '^(HTTP/|location:|link:)'
```

## Worked example: "Google chose different canonical than user" on product pages

Situation: 2,300 product URLs show "Duplicate, Google chose different canonical than user"; URL Inspection on one
says user-declared `https://www.example.com/p/runner-x`, Google-selected `https://www.example.com/p/runner-x?color=blue`.

Diagnosis: the canonical tag is right, but every other signal points elsewhere: category pages link to
`?color=blue` (the default colour), the sitemap lists the `?color=` URLs, and the clean URL answers 302 to the
coloured one. Fix: the clean URL answers 200 and shows the default colour; category links and the sitemap use the
clean URL; colour URLs keep a canonical to it. Check: after recrawl, URL Inspection shows the two canonicals agree;
the count in that Page indexing reason falls over the following weeks.

## Verify

Verify canonical URLs from outside first: every form of a URL ends on one address in one hop, and that address names
itself. Run this on one URL per template:

```bash
CANON=https://www.example.com/shoes/
for u in http://example.com/shoes/ http://www.example.com/shoes/ https://example.com/shoes/ https://www.example.com/shoes; do
  curl -sIL -o /dev/null -w '%{url_effective} %{num_redirects}\n' "$u"                 # expect $CANON and 1
done
curl -sL "$CANON" | grep -ioE '<link[^>]+rel="?canonical"?[^>]*>'                      # expect href="$CANON"
curl -sL "$CANON?utm_source=news" | grep -ioE '<link[^>]+rel="?canonical"?[^>]*>'      # expect the same href
```

Then read URL Inspection on three URLs per template: user-declared and Google-selected canonical must match. After
recrawl, the count under "Duplicate, Google chose different canonical than user" falls in the Page indexing report.

## Checklist for canonical URLs

The canonical checklist confirms every document has one URL and every signal agrees.

1. One host and protocol; all other forms 301 in one hop.
2. One trailing-slash convention; the other form redirects.
3. Every indexable page has an absolute self canonical in the server HTML.
4. Canonical targets answer 200, are indexable, and are not canonicalised again.
5. Internal links, sitemaps and hreflang use canonical URLs only.
6. Tracking, sort and session parameters never appear in internal links.
7. Paginated pages self-canonical and linked.
8. URL Inspection: user-declared and Google-selected canonical match on key templates.

## Gotchas with canonical URLs

The gotchas below are the canonical mistakes that cost the most traffic.

1. **Every page canonicalises to the home page.** Symptom: pages drop out of the index in weeks. Cause: a template bug
   writes one URL into every canonical tag. Fix: fix the template and check one URL per template after each release.
2. **Canonical to page 1 on paginated lists.** Symptom: products deep in a category stop being found. Cause: items
   deeper in the series lose their only path. Fix: give each page a self canonical.
3. **Canonical to a redirected or 404 URL.** Symptom: URL Inspection shows a Google-selected canonical you never
   declared. Cause: Google ignores the hint and guesses. Fix: point the tag at the final URL that answers 200.
4. **http canonical on an https site.** Symptom: Google-selected canonical shows the http address and signals split
   between protocols. Cause: the tag was left from before the move. Fix: update the template to https and keep the 301
   from http.
5. **Cross-domain canonical by accident.** Symptom: the production site loses pages to a staging or white-label copy.
   Cause: a canonical across domains went live on the copy by mistake. Fix: make each host self-canonical and keep
   staging behind authentication.
6. **Different content behind one canonical.** Symptom: Google ignores the declared canonical. Cause: the declared URL
   is not substantially the same page. Canonicals are for duplicates, not for "related" pages. Fix: use a normal link
   between related pages, and merge true duplicates.

## Anti-patterns in canonical URLs

Anti-patterns with canonicals come from asking one tag to do the job of a redirect or a block.

| Do not | Do this instead |
|---|---|
| Using a canonical where users should not land on the old URL at all | 301 it; a redirect is the strongest signal and fixes the page for people too |
| Blocking duplicates in robots.txt to consolidate them | leave them crawlable with a canonical, because a blocked page cannot show its tag |
| Declaring the clean URL in the tag while linking to parameter URLs | link the clean URL everywhere so every signal agrees |
| Setting the canonical late with JavaScript | put it in the server HTML, once per page |
| Relying on the retired URL Parameters tool's old settings | handle parameters on the site with canonicals, clean links and redirects |

## See also for canonical URLs

- `crawling-and-indexing`: noindex and robots.txt
- `search-console`: the Duplicate reasons in Page indexing
- `site-migrations`: redirect maps and one-hop redirects
- `ecommerce-seo`: filters, variants and sort parameters
- `international-seo`: canonicals per locale alongside hreflang
- `xml-sitemaps`: listing canonical URLs only
