---
title: Image and video markup and the Video indexing report
author: MOZGII, Inc.
lang: en
description: ImageObject licence metadata, VideoObject with Clip key moments, a video sitemap entry, and every reason in Search Console's Video indexing report with its fix.
---

# Image and video markup and the Video indexing report

This file holds the templates and the report reasons for image and video search. Values in the examples are
placeholders; generate them from the same data that renders the page.

## Contents

1. Image licence metadata with ImageObject
2. VideoObject with Clip key moments
3. Video sitemap entry
4. Video indexing report reasons and fixes

## Image licence metadata with ImageObject

Image licence metadata makes an image eligible for the "Licensable" badge and credit details in Google Images. Add it
on the page that shows the image, or embed the same facts in the file as IPTC fields (Web Statement of Rights,
Licensor URL, Creator, Credit Line, Copyright Notice).

```json
{
  "@context": "https://schema.org",
  "@type": "ImageObject",
  "contentUrl": "https://cdn.example.com/img/ridge-trail-sunrise.jpg",
  "license": "https://www.example.com/image-licence",
  "acquireLicensePage": "https://www.example.com/buy/ridge-trail-sunrise",
  "creator": {"@type": "Person", "name": "Alex Doe"},
  "creditText": "Alex Doe / Example Outdoor",
  "copyrightNotice": "© 2026 Example Outdoor"
}
```

## VideoObject with Clip key moments

`VideoObject` describes the video on its watch page; `Clip` entries mark key moments with labels and offsets in
seconds. Since September 2026 Google also documents `creator` (who made or published the video) and recommends
`interactionStatistic` over `interactionCount`.

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "How to lace trail shoes for downhill running",
  "description": "Three lacing methods that stop toes hitting the front of the shoe.",
  "thumbnailUrl": ["https://cdn.example.com/thumbs/lacing-16x9.jpg"],
  "uploadDate": "2026-09-02T08:00:00+00:00",
  "duration": "PT3M34S",
  "contentUrl": "https://cdn.example.com/video/lacing.mp4",
  "embedUrl": "https://www.example.com/player/lacing",
  "hasPart": [
    {"@type": "Clip", "name": "Heel lock", "startOffset": 18, "endOffset": 85,
     "url": "https://www.example.com/videos/lacing?t=18"},
    {"@type": "Clip", "name": "Window lacing", "startOffset": 86, "endOffset": 150,
     "url": "https://www.example.com/videos/lacing?t=86"}
  ]
}
```

For a live stream add `"publication": {"@type": "BroadcastEvent", "isLiveBroadcast": true, "startDate": "...",
"endDate": "..."}`. For a video that should leave results on a date add `"expires"`.

## Video sitemap entry

A video sitemap entry gives the same facts for crawlers that find the page late. Required: thumbnail, title,
description, and the file or the player URL.

```xml
<url>
  <loc>https://www.example.com/videos/lacing</loc>
  <video:video>
    <video:thumbnail_loc>https://cdn.example.com/thumbs/lacing-16x9.jpg</video:thumbnail_loc>
    <video:title>How to lace trail shoes for downhill running</video:title>
    <video:description>Three lacing methods that stop toes hitting the front of the shoe.</video:description>
    <video:content_loc>https://cdn.example.com/video/lacing.mp4</video:content_loc>
    <video:duration>214</video:duration>
  </video:video>
</url>
```

The `<urlset>` must declare `xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"`.

## Video indexing report reasons and fixes

The Video indexing report in Search Console (Indexing › Videos) lists why a video found on an indexed page was not
indexed.

| Reason | Fix |
|---|---|
| Video isn't on a watch page | give the video its own page where it is the main content |
| Cannot determine video position and size | load the player with the page; no click-to-load cover image |
| MRSS failure; try using schema.org instead | replace the media RSS feed with `VideoObject` markup |
| No thumbnail URL provided | add `thumbnailUrl` in markup or `video:thumbnail_loc` in the sitemap |
| Unsupported thumbnail format | use BMP, GIF, JPEG, PNG, WebP, SVG or AVIF with the right extension |
| Invalid thumbnail size | at least 60×30 px; larger is better |
| Thumbnail blocked by robots.txt | allow the thumbnail host and path |
| Thumbnail is transparent | use an opaque image (at least 80% of pixels nearly opaque) |
| Thumbnail could not be crawled due to hostload | raise server capacity or wait; the crawl limit was reached |
| Thumbnail could not be reached | fix 404s, passwords or wrong URLs on the thumbnail |
| Invalid thumbnail | check the thumbnail against all requirements |
| Video not processed | Google chose not to index it; improve the watch page and its demand |
| Video not processed yet | wait a few days |
| Video not found on host service | the hosted video is private, deleted or unreachable; fix it on the host |
