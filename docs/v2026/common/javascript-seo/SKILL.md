---
name: javascript-seo
description: 'Makes JavaScript sites (React, Next.js, Vue, Nuxt, Angular, Svelte, Astro, single-page apps) crawlable and indexable: choosing SSR, static generation or client rendering, metadata and canonicals in the server HTML, real links and History API routing, 404 status codes in SPAs, lazy loading, the 2 MB fetch limit, blocked API calls, caching and testing raw against rendered HTML. Use when a JS site is not indexed, Google sees an empty page, a framework migration is planned, or a developer asks how to make an app SEO-friendly.'
metadata:
  tags:
  - seo
  - javascript-seo
  - rendering
  - ssr
  - nextjs
  - single-page-app
---

# JavaScript SEO

JavaScript SEO keeps a site that builds its pages with JavaScript visible to search engines. Google fetches the HTML,
queues every page that answers 200 for rendering in an up-to-date headless Chromium, runs the JavaScript, then
indexes the rendered result and follows the links it finds. Bing renders too. Most other consumers (social previews,
many AI fetchers, smaller engines) read only the first HTML. So the rule is simple: what must rank goes in the HTML
the server sends.

## Step 0: read the framework versions the project runs

The server-side APIs for metadata, redirects and status codes change between majors, so read what is installed before
choosing a recipe. The recipes here target the October 2026 majors: Next.js 16, Nuxt 4, SvelteKit 3, Astro 7 and React
Router 8.

```bash
npm ls next nuxt @sveltejs/kit astro react-router 2>/dev/null
```

No framework in the list means a plain client-only app or a server stack of its own: start from "Choose the rendering
strategy" and the client-only section of the recipes.

## Choose the rendering strategy

The rendering strategy decides what a crawler receives on the first request, and it is the one decision that settles
most JavaScript SEO problems. Default: server-side rendering or static generation for every page that should rank.

| Strategy | First HTML holds | Use for |
|---|---|---|
| Static generation (SSG) | full content | pages that change on publish: articles, docs, marketing pages |
| Server-side rendering (SSR) | full content per request | catalogues, prices, stock, personalised but public pages |
| Incremental or on-demand regeneration (ISR) | full content, refreshed in the background | large catalogues where SSR per request is costly |
| Client-side rendering only (CSR) | an empty shell | logged-in apps, dashboards, anything that should not rank |

Do not build new "dynamic rendering" (pre-rendered HTML for bots only, the app for people): Google calls it a
workaround it no longer recommends. Hydration (SSR first, then the app takes over in the browser) is fine as long as
the server HTML and the hydrated page show the same content.

## What must be in the server HTML

Some elements are read before or without rendering, so they belong in the first HTML on every indexable page:

- `<title>`, meta description, `<link rel="canonical">`, meta robots, hreflang, Open Graph tags.
- The main text, headings and the internal links to other pages.
- Structured data, when other consumers than Google must read it (Google can read JSON-LD added by JavaScript).

Rules Google states for JavaScript changes to these:

- **noindex**: a `noindex` in the first HTML can stop rendering, so JavaScript cannot remove it later. Never ship
  `noindex` in the shell and "fix it" on the client.
- **canonical**: set it in the HTML. If JavaScript sets it, it must match the HTML one, and the page must end up with
  exactly one canonical tag.
- **titles and descriptions**: JavaScript may set them, but other engines and previews will not see them.

## Links and routing

Links are followed only when they are `<a>` elements with a real URL in `href`. Routes need real paths.

```html
<a href="/shoes/trail">Trail shoes</a>                      <!-- followed -->
<a href="/shoes/trail" onclick="go(event)">Trail shoes</a>   <!-- followed: href is real -->
<span onclick="go('/shoes/trail')">Trail shoes</span>        <!-- not a link -->
<a href="javascript:void(0)">Trail shoes</a>                 <!-- not followed -->
<a href="#/shoes/trail">Trail shoes</a>                      <!-- fragment: same URL as the page -->
```

Use the History API (`pushState`) router mode, never hash routing, for anything that should be indexed. A fragment
(`#/...`) never becomes a separate URL in Google.

## Status codes in single-page apps

A single-page app answers 200 for every route unless told otherwise, which turns missing pages into soft 404s. Pick
one, in this order:

1. Server or framework rendering returns a real 404 (or 410) for unknown routes and deleted items.
2. In a client-only app, send unknown routes to a URL the server answers with 404 (for example `/not-found`).
3. As a last resort, add `<meta name="robots" content="noindex">` to the error view with JavaScript.

Redirects belong on the server (301 or 308). A JavaScript redirect (`location.replace`) is followed by Google but
later and less reliably; other crawlers may not follow it at all.

## Lazy loading, interaction and storage

Googlebot renders with a tall viewport and does not click, type, scroll like a person, grant permissions or keep
state between pages. So:

- Content that appears only after a click (a tab filled by fetch, "load more" without links) is not indexed. Put it
  in the HTML, or load it on page load.
- Use native `loading="lazy"` for images and `IntersectionObserver` for content; give infinite scroll and "load
  more" real paginated URLs (`?page=2`) linked with `<a href>`.
- Do not depend on cookies, `localStorage` or `sessionStorage` to show content: each render starts empty.
- Permission prompts (location, camera, notifications) are declined; the page must work without them.
- WebSockets and WebRTC are not supported for rendering; load content over plain HTTP requests.
- Web components: Google flattens shadow DOM and light DOM; content must be visible in the rendered HTML (use
  `<slot>` to project light DOM content).

## Fetch limits, blocked resources and caching

Rendering only sees what Googlebot was allowed and able to fetch.

- **2 MB per file**: Googlebot reads the first 2 MB of an HTML file and of each JavaScript or CSS file, measured
  uncompressed (64 MB for PDFs). Content after the cut does not exist for Google. Watch large inline JSON (state
  blobs such as framework data scripts) that push the main text past the limit.
- **robots.txt blocks**: Google does not render JavaScript from blocked files. `Disallow: /api/` or a blocked CDN host
  leaves the page empty if its content comes from there. Allow the scripts, styles and API routes the page needs.
- **Caching**: Google's renderer may ignore cache headers and use an old bundle. Put a content hash in file names
  (`main.2bb85551.js`) so each release gets new URLs.
- **Errors**: a script error or a timeout in rendering leaves the content out. URL Inspection's "More info" shows
  console errors and blocked resources.

## Verify

The raw against rendered HTML test compares what the server sends with what Google renders. Run it on one URL per template.

1. Raw HTML: does it hold the title, canonical, H1, main text and links?

```bash
curl -s https://www.example.com/shoes/trail | grep -ciE '<h1|<h2|<a href'
curl -s https://www.example.com/shoes/trail | wc -c        # bytes; compare with the 2 MB limit
```

2. Rendered HTML: Search Console › URL Inspection › Test live URL › View tested page (HTML, screenshot, "More info"
   for resources and console). Without Search Console access, the Rich Results Test uses the same renderer.
3. Compare: anything that ranks but is only in the rendered HTML is a risk for Google and missing for everyone else.
   Move it to the server.

Framework-specific ways to put metadata, canonicals, sitemaps and 404s on the server are in
[references/framework-recipes.md](references/framework-recipes.md).

## Worked example: a React shop that Google sees as empty

Situation: a Vite and React shop has 40,000 product URLs; Search Console shows 1,200 indexed and many "Soft 404" and
"Crawled - currently not indexed".

Findings: `curl` on a product URL returns a 2 KB shell with `<div id="root">`; the products load from `/api/products`,
which robots.txt disallows; unknown product IDs render "Product not found" with status 200; category links are
`<div onClick>`.

Plan, in order: allow `/api/` in robots.txt the same day (rendering starts working); replace clickable divs with
`<a href>`; move product and category pages to server rendering (here a move to a React framework with SSR); return
404 for unknown products from the server; check five templates with URL Inspection; watch "Indexed" in the Page
indexing report over the next four to eight weeks.

## Checklist for a JavaScript site

The checklist confirms a JavaScript site is as visible as a static one.

1. Every indexable template is SSR or static; CSR only for pages that should not rank.
2. Raw HTML holds title, description, canonical, robots, H1, main text and links.
3. No `noindex` in the shell; one canonical per page.
4. Links are `<a href>` with real paths; History API routing, no hash routes.
5. Unknown routes return 404; redirects are server-side 301 or 308.
6. Scripts, styles and API routes the page needs are not blocked by robots.txt.
7. HTML and each script under 2 MB uncompressed; file names carry content hashes.
8. URL Inspection "Test live URL" shows the content and no blocking errors on each template.

## Gotchas in JavaScript SEO

The gotchas below are behind most "Google sees an empty page" tickets.

1. **Blocking the API in robots.txt.** Symptom: URL Inspection shows the page rendered without its content. Cause: the
   page calls an endpoint the crawler may not fetch. Fix: allow the endpoints the page calls.
2. **noindex in the shell, removed by JavaScript.** Symptom: the page never joins the index. Cause: rendering may
   never run, so the page stays out. Fix: serve the right robots tag from the server.
3. **Soft 404s from client routing.** Symptom: every typo URL answers 200 with "not found". Cause: the shell answers
   200 for all routes. Fix: return 404 from the server.
4. **Content behind a click.** Symptom: the text is on screen and missing from URL Inspection. Cause: tabs and "show
   more" filled by fetch are not indexed. Fix: put the text in the HTML, or load it on page load.
5. **Hash routes.** Symptom: `/#/product/1` and `/#/product/2` are one URL to Google, so one page is indexed. Cause: a
   fragment is not part of the URL for Google. Fix: use History API routing.
6. **Huge inline state.** Symptom: text at the end of long pages is not found in search. Cause: a 3 MB HTML file with
   the main text near the end loses that text. Fix: move the state out, or put the main text first.
7. **Testing in your own browser.** Symptom: the page works for the team and fails for Google. Cause: your browser has
   your cookies, cache and permissions. Fix: test with URL Inspection and `curl`.
8. **Relying on Google rendering for everyone.** Symptom: Google indexes the page while social previews and AI
   fetchers show nothing. Cause: Bing renders less often, social and many AI fetchers not at all. Fix: use server
   HTML, which serves them all.

## Anti-patterns in JavaScript SEO

Anti-patterns in JavaScript sites assume every reader of the page runs the app the way a person's browser does.

| Do not | Do this instead |
|---|---|
| Building new dynamic rendering for bots | use SSR or static generation for everyone |
| Keeping `noindex` on a page until the client decides | decide on the server |
| Adding a second canonical in JavaScript | keep one tag, in the server HTML |
| Using `location.replace` for permanent redirects | use a server 301 or 308 |
| Shipping bundles with the same file name each release | put a content hash in the name |

## References for JavaScript SEO

The reference files below hold the detail for this skill; open one only when the task needs it.

- [references/framework-recipes.md](references/framework-recipes.md): metadata, canonical, sitemap, robots and 404
  handling in Next.js, Nuxt, SvelteKit, Astro, React Router and client-only apps, plus single-page app metrics.

## See also for JavaScript SEO

- `crawling-and-indexing`: robots.txt and status codes
- `search-console`: Page indexing reasons and URL Inspection
- `core-web-vitals`: hydration cost and single-page app metrics
- `structured-data`: JSON-LD in server HTML
- `site-migrations`: moving a client app to a server framework
- `xml-sitemaps`: sitemaps from framework routes
