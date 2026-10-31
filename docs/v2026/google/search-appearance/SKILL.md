---
name: search-appearance
description: 'Fixes how a site looks in Google results: title links Google rewrote, snippets and meta descriptions it ignores, the wrong site name, a missing favicon, wrong dates, breadcrumbs and sitelinks, featured snippets, and the robots controls nosnippet, max-snippet and data-nosnippet. Use when Google shows a different title than the page has, the wrong site name or favicon, an old date, an unwanted snippet, or when someone asks how to get sitelinks or a featured snippet.'
metadata:
  tags:
  - seo
  - title-links
  - snippets
  - site-name
  - favicon
  - serp-features
---

# Search appearance: titles, snippets, site names and favicons

Search appearance is how a page shows in Google's results: the site name and favicon, the visible URL or breadcrumb,
the title link, the date, the snippet, and features such as sitelinks or a featured snippet. Google builds each from
the page and the site, and it may choose something other than what the page declares. The work is to give it one
clear, consistent answer for each element.

## Step 0: read what the site declares and what Google shows

Read both sides first, because the work is closing the gap between what the page declares and what appears in results.

```bash
curl -sL https://www.example.com/ | grep -ioE '<title>[^<]*</title>|<meta[^>]+og:site_name[^>]*>|<link[^>]+rel="[^"]*icon[^"]*"[^>]*>|"@type": *"WebSite"|"alternateName": *"[^"]*"'
curl -sI https://www.example.com/favicon.ico | grep -iE '^(HTTP/|content-type:)'
curl -s https://www.example.com/robots.txt | grep -iE '^(user-agent|disallow):'
```

Then search for `site:example.com` and for the brand name, and save a dated screenshot of the title link, site name,
favicon, date and snippet. Note what generates the title and the home page markup, usually a CMS template or an SEO
plugin.

## Title links Google rewrites

To control the title link in Google, make the `<title>` the clearest, most accurate title on the page. Google builds
title links from several sources: the `<title>` element, the main visible title, headings such as `<h1>`, `og:title`,
other prominent text, anchor text on the page and in links pointing to it, and `WebSite` structured data. It replaces
the `<title>` when it is one of these:

| Problem | Example | Fix |
|---|---|---|
| half-empty | `<title> - Example Outdoor</title>` | write a real title |
| obsolete | "Trail race results 2024" on the 2026 page | update the title with the content |
| inaccurate | "Free shipping on all shoes" on a returns page | describe the page |
| micro-boilerplate | the same title on every page of a series, only the page number differs | add what is specific to each page |
| no clear main title | several `<h1>` or a big promo line bigger than the headline | one main title, visually first |
| language or script mismatch | English title on a Russian page | same language and script as the content |
| site name repeated | "Example Outdoor - Shoes - Example Outdoor" | brand once, at the end |
| keyword stuffing | "Trail shoes, trail running shoes, best trail shoes" | one natural title |

Then the title, the `<h1>` and `og:title` should say the same thing. Check what Google shows with a `site:` search or
the Search Console Performance report's page list; a change shows after the page is recrawled.

## Snippets and meta descriptions

The snippet under the title is usually built from the page text that best matches the query, and only sometimes from
the meta description. So a meta description is a default, not a command.

- Write a unique description per page that summarises it in one or two sentences with the most useful fact first.
- Make the lead paragraph answer the main query: it becomes the snippet more often than the description does.
- Do not repeat the title or list keywords; Google ignores those descriptions.
- Programmatic pages: generate descriptions from page data ("Runner X, 280 g, 8 mm drop, from €129"), not one
  template sentence.

## Snippet and preview controls

Snippet controls set the maximum Google may show in results and AI features; they also limit what can be quoted.

| Control | Effect |
|---|---|
| `<meta name="robots" content="nosnippet">` | no text snippet and no video preview; the page can still rank; its text is also kept out of AI Overviews and AI Mode |
| `max-snippet:[n]` | at most n characters of text (`0` = none, `-1` = no limit) |
| `data-nosnippet` on a `span`, `div` or `section` | that part is never shown in snippets or AI features |
| `max-image-preview:[none\|standard\|large]` | size of image previews; `large` for Discover |
| `max-video-preview:[n]` | seconds of video preview |

Default: no controls, plus `max-image-preview:large`. Use `data-nosnippet` for parts that must not be quoted (prices
behind a login, legal disclaimers), rather than `nosnippet` on the whole page.

## Read more deep links in snippets

A "read more" link inside a snippet takes the searcher to one section of the page. Google shows it more often when the
section's text is in the open rather than in a tab or collapsed block, when no script sets the scroll position on load,
and when code that touches the History API or `location.hash` on load keeps the `#fragment` in the URL.

## Site names in results

The site name Google shows above the URL comes from the home page. Google supports site names for domains and
subdomains, not for subfolders (`example.com/blog` cannot have its own). To set it:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Example Outdoor",
  "alternateName": ["ExOut", "exampleoutdoor.com"],
  "url": "https://www.example.com/"
}
</script>
```

Put it on the home page only, on every version of it (http and https, www and bare), and use the same name in the
home page `<title>`, `og:site_name`, the logo text and the Organization markup. If Google still shows another name
after a recrawl: check the markup with the Schema Markup Validator (the Rich Results Test does not show site names),
check that redirects to the home page work, add `alternateName`, and as a last resort use the domain as `name`.

## Favicons in results

The favicon Google shows comes from the home page's icon link. Requirements:

```html
<link rel="icon" href="/favicon-96.png" sizes="96x96" type="image/png">
```

- Square (1:1), at least 8×8 px; Google recommends more than 48×48 px (96×96, 192×192) so it stays sharp on every surface.
- `rel` is `icon`, `shortcut icon` (legacy), `apple-touch-icon` or `apple-touch-icon-precomposed`; formats BMP, GIF,
  ICO, PNG, JPEG, PPM and TIFF. SVG is not on Google's list, so a site with an SVG icon links a raster file as well.
- One favicon per host name; a subfolder site cannot have its own.
- Googlebot must reach the home page and Googlebot-Image the icon file; neither blocked by robots.txt.
- A stable URL, relative or on a CDN; a change takes days to weeks to show after the home page is recrawled.
  Inappropriate icons are replaced with a default.

## Search profile and its badge

A Search profile is one page on Google (`https://profile.google.com/@handle`) that gathers a creator's or publisher's
site and social posts; people who follow it are more likely to see that content in Discover. Claim the profile first
(Google's Search profile help), then point readers to it from the site with Google's badge or a plain text link in a
byline or bio.

```html
<a href="https://profile.google.com/@exampleoutdoor" aria-label="Find us on Google Search">
  <img src="/badges/search-profile.png" alt="Google Search" width="48" height="48">
</a>
```

Use the assets from Google's download. Keep the clickable area at least 44×44 px on the web, do not stretch or recolour
the G icon, and beside a Preferred Sources badge use the labelled profile button, not the bare icon.

## Dates in results

Google shows a date when it can tell one, and picks it from visible dates on the page and from structured data. Show
one clear date near the headline ("Published 2 Sep 2026, updated 14 Oct 2026"), use the same values in
`datePublished` and `dateModified` with a time zone, and keep other dates (comments, related posts, a copyright year)
away from the headline. A wrong date in results usually means the page shows several dates or the markup disagrees
with the visible one.

## Breadcrumbs, visible URL and sitelinks

The line above the title shows the site name and the URL or a breadcrumb. On mobile Google shows a simplified visible
URL (the domain) since early 2025; breadcrumbs from `BreadcrumbList` markup still help Google understand the site's
structure and show on desktop.

Sitelinks (extra links under a result) are automatic. There is no markup for them and no way to request them. They
come with a clear structure: descriptive, unique titles, a navigation that names the main sections, and internal
links with plain anchor text. Remove an unwanted sitelink by `noindex`-ing or improving that page.

## Featured snippets and People also ask

A featured snippet is a quoted answer shown above or within the results; People also ask shows related questions
with quoted answers. There is no markup to opt in. Pages win them by answering a question directly: a heading that
matches the question, then a short answer (practitioners aim for 40–60 words), a list or a table right under it. Opt out with `nosnippet` (page) or
`data-nosnippet` (the part), which also removes normal snippets for that text.

## Worked example: Google shows "Home" and the wrong brand

Situation: results for a shop show "Home" as the title link of the home page and "Shopify Store" as the site name.

Diagnosis: the home page `<title>` is "Home"; there is no `WebSite` markup; `og:site_name` is the platform's default.
Fix: title "Example Outdoor: trail running shoes and gear"; `WebSite` JSON-LD with name "Example Outdoor" and
`alternateName` "exampleoutdoor.com"; `og:site_name` set; the same name in Organization markup. Then URL Inspection ›
Request indexing for the home page. Check: the site name and title link in results over the next one to three weeks.

## Verify title, site name, favicon and date

The home page and one page per template carry the inputs Google reads. Print them from the served HTML and compare
with what the results show:

```bash
curl -sL https://www.example.com/ > home.html
python3 - home.html <<'EOF'
import json, re, sys
html = open(sys.argv[1], encoding="utf-8", errors="replace").read()
find = lambda pattern: re.findall(pattern, html, re.S | re.I)
print("title:", find(r"<title[^>]*>(.*?)</title>"))
print("h1:", [re.sub(r"<[^>]+>", " ", h).strip() for h in find(r"<h1[^>]*>(.*?)</h1>")])
print("og:site_name:", find(r'property="og:site_name"[^>]*content="([^"]*)"'))
print("icons:", find(r'<link[^>]+rel="(?:shortcut icon|icon|apple-touch-icon(?:-precomposed)?)"[^>]*href="([^"]+)"'))
print("robots:", find(r'<meta[^>]+name="robots"[^>]*content="([^"]*)"'))
for block in find(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>"):
    try:
        data = json.loads(block)
    except ValueError as bad:
        print("INVALID JSON-LD:", bad)
        continue
    for item in data if isinstance(data, list) else data.get("@graph", [data]):
        if isinstance(item, dict) and item.get("@type") == "WebSite":
            print("WebSite:", item.get("name"), item.get("alternateName"))
EOF
curl -sI -A Googlebot-Image https://www.example.com/favicon-96.png | head -1     # the icon file: expect 200
```

Expect one title, matching `og:site_name` and `WebSite` name, a raster icon and `max-image-preview:large`. Then URL
Inspection › Test live URL confirms Google can fetch both the page and the icon. What Google really shows is read in
results with a `site:` search after the page is recrawled, which takes one to three weeks for a site name and days to
weeks for a favicon.

## Checklist for search appearance

The checklist runs on the home page and one page per template.

1. Unique, accurate `<title>` per page; it matches the `<h1>` and `og:title`; brand once at the end.
2. Unique meta descriptions; the lead answers the main query.
3. `WebSite` markup with `name` and `alternateName` on the home page; the same name everywhere.
4. A square raster favicon larger than 48×48 px, crawlable, linked from the home page.
5. One visible date near the headline, matching `datePublished` and `dateModified`.
6. `BreadcrumbList` on deep pages; clear section navigation.
7. `max-image-preview:large` set; `nosnippet` only where the owner decided it.

## Gotchas with search appearance

The gotchas below are the common reasons results look wrong.

1. **Expecting the title tag to be used as written.** Symptom: results show a different title from the page. Cause:
   Google rewrites unclear, stuffed or boilerplate titles. Fix: fix the title, not the snippet.
2. **Site name markup on a subfolder.** Symptom: `example.com/blog` still shows the main site's name. Cause: site
   names are not supported there, only on domains and subdomains. Fix: accept the host's name, or move the section to
   a subdomain.
3. **Favicon missing from results.** Symptom: the default globe icon shows beside the site. Cause: the file is blocked
   by robots.txt, or served from a URL that changes every deploy. Fix: allow it and keep one stable URL.
4. **Two dates near the headline.** Symptom: results show the wrong date. Cause: with "Updated" and an event date side
   by side, Google may show the wrong one. Fix: keep one clear date near the headline.
5. **`nosnippet` to hide from AI answers.** Symptom: clicks fall along with AI exposure. Cause: it removes the normal
   snippet too. Fix: to leave Google's AI features and keep normal results, use Search Console › Settings › Search
   generative AI (`google-ai-features`).
6. **Asking for sitelinks.** Symptom: a request or markup brings no change. Cause: they cannot be requested; they
   follow structure. Fix: improve titles, navigation and internal links.

## Anti-patterns in search appearance

Anti-patterns in search appearance try to dictate to Google what it only accepts as a hint.

| Do not | Do this instead |
|---|---|
| Writing a different title for search, `<h1>` and `og:title` | say the same thing in all three |
| Repeating the title in the meta description | lead with the most useful fact |
| Putting `nosnippet` on a whole page to protect one paragraph | use `data-nosnippet` on that part |
| Marking up FAQ to win a bigger snippet | answer in the text; that markup wins nothing now |
| Using an SVG-only favicon | link a raster file as well |

## See also for search appearance

- `on-page-seo`: writing titles and descriptions for a new page
- `structured-data`: `WebSite`, `Organization` and `BreadcrumbList` markup
- `google-rich-results`: rich results Google supports and the ones it retired
- `news-and-discover-seo`: preferred sources and Discover previews
- `google-ai-features`: leaving AI features without touching normal results
- `image-and-video-seo`: preferred image and thumbnails
