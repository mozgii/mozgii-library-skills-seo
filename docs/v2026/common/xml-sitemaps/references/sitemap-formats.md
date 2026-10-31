---
title: Image, video, news and hreflang sitemaps
author: MOZGII, Inc.
lang: en
description: Examples and required tags for the image, video and news sitemap extensions and for hreflang alternates in sitemaps.
---

# Image, video, news and hreflang sitemaps

Sitemap extensions add media and language data to the normal `<url>` entries. Each needs its namespace declared on
`<urlset>`. Google supports all four below; other engines support a subset.

## Image sitemap extension

The image sitemap extension lists images a page uses, which helps Google find images loaded by JavaScript or served
from a CDN host. Up to 1,000 images per page entry; only `image:loc` is used (Google retired caption, title,
geo_location and license tags in 2022).

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://www.example.com/shoes/trail-runner</loc>
    <image:image><image:loc>https://cdn.example.com/img/trail-runner-side.jpg</image:loc></image:image>
    <image:image><image:loc>https://cdn.example.com/img/trail-runner-sole.jpg</image:loc></image:image>
  </url>
</urlset>
```

## Video sitemap extension

The video sitemap extension describes videos embedded on a page. Required: `video:thumbnail_loc`, `video:title`,
`video:description`, and either `video:content_loc` (the file) or `video:player_loc` (the embed player).

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  <url>
    <loc>https://www.example.com/guides/lacing</loc>
    <video:video>
      <video:thumbnail_loc>https://cdn.example.com/thumbs/lacing.jpg</video:thumbnail_loc>
      <video:title>How to lace trail shoes for downhill running</video:title>
      <video:description>Three lacing methods that stop toes hitting the front of the shoe.</video:description>
      <video:content_loc>https://cdn.example.com/video/lacing.mp4</video:content_loc>
      <video:duration>214</video:duration>
      <video:publication_date>2026-09-02T08:00:00+00:00</video:publication_date>
    </video:video>
  </url>
</urlset>
```

## News sitemap extension

The news sitemap extension is for publishers in Google News. It lists articles published in the last two days only,
at most 1,000 URLs per file; older articles move to the normal sitemap.

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  <url>
    <loc>https://www.example.com/news/city-marathon-route-2026</loc>
    <news:news>
      <news:publication><news:name>Example News</news:name><news:language>en</news:language></news:publication>
      <news:publication_date>2026-10-27T07:15:00+00:00</news:publication_date>
      <news:title>City marathon publishes 2026 route</news:title>
    </news:news>
  </url>
</urlset>
```

## hreflang alternates in a sitemap

hreflang alternates in a sitemap replace `<link rel="alternate">` tags in the HTML; use one method, not both. Every
`<url>` entry lists all versions including itself.

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://www.example.com/en/shoes/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.example.com/en/shoes/"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://www.example.com/de/schuhe/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://www.example.com/en/shoes/"/>
  </url>
  <url>
    <loc>https://www.example.com/de/schuhe/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.example.com/en/shoes/"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://www.example.com/de/schuhe/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://www.example.com/en/shoes/"/>
  </url>
</urlset>
```

Full hreflang rules: the `international-seo` skill.
