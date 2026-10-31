---
title: Open Graph and social cards
author: MOZGII, Inc.
lang: en
description: The Open Graph and X card tags that control link previews in social networks, messengers and chat tools, with sizes and checks.
---

# Open Graph and social cards

Open Graph tags (`og:*`) control how a link looks when shared in social networks, messengers, chat tools and many
AI assistants. They are not schema.org and do not affect rankings, but a good preview raises clicks from shares.

## The Open Graph tags every page needs

Every indexable page carries these Open Graph tags in the server HTML; crawlers of social apps do not run JavaScript.

```html
<meta property="og:type" content="article">
<meta property="og:title" content="How to choose trail running shoes">
<meta property="og:description" content="Lugs, rock plates and drop: what matters on which terrain.">
<meta property="og:url" content="https://www.example.com/guides/choosing-trail-shoes">
<meta property="og:image" content="https://www.example.com/img/og/choosing-trail-shoes.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Three trail shoes side by side on a rocky path">
<meta property="og:site_name" content="Example Outdoor">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
```

- `og:url` equals the canonical URL.
- `og:image`: absolute https URL, 1200×630 px (1.91:1), under about 5 MB, JPEG or PNG; text on it stays readable at
  small sizes.
- `og:title` may be shorter than the `<title>` and drop the brand; keep the same promise.
- X (formerly Twitter) falls back to Open Graph for title, description and image; `twitter:card` is the one tag
  it needs.

## Open Graph in frameworks

Open Graph tags are set where the page's metadata is set, and page-level values must not wipe out site-level ones.
In Next.js, `openGraph` in a page's `metadata` replaces the layout's `openGraph` object instead of merging it, so a
page that sets only `title` loses `siteName` and `images`. Spread a shared object:

```ts
// app/shared-metadata.ts
export const baseOpenGraph = { siteName: "Example Outdoor", locale: "en_US", type: "website" as const };

// app/guides/[slug]/page.tsx
export async function generateMetadata({ params }) {
  const guide = await getGuide((await params).slug);
  return {
    title: guide.title,
    openGraph: { ...baseOpenGraph, type: "article", title: guide.title, images: [guide.ogImage] },
  };
}
```

## Check link previews

Link previews are checked with each platform's own tool, because each caches the first fetch.

- Facebook Sharing Debugger (developers.facebook.com/tools/debug): shows tags and forces a refetch.
- LinkedIn Post Inspector (linkedin.com/post-inspector).
- Quick local check: `curl -s https://www.example.com/page | grep -oE '<meta (property|name)="(og|twitter):[^>]+>'`.

A wrong preview after a fix is usually the platform's cache; refetch with the tool above.
