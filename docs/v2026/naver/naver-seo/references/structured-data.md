---
title: Naver structured data reference
author: MOZGII, Inc.
lang: en
tags: [naver, structured-data, schema-org, json-ld]
description: The Schema.org types Naver's guides list, the properties each needs, and JSON-LD templates for a Korean site.
---

# Naver structured data reference

Naver uses Schema.org markup in JSON-LD or Microdata to build results suited to the content, and its robot collects the
data automatically. Valid markup guarantees nothing. The guides name no Naver testing tool: validate with the Schema.org
validator, then read URL 검사.

## Site channels with sameAs

Linked channels (사이트 연관채널) tell Naver which profiles belong to a site. Put `Person` or `Organization` markup on the
root page with `name`, `url` and `sameAs`. Showing them is never guaranteed, and Naver names sites it favours for this:
a unique name with no ambiguity, public bodies, and sites users prefer.

| Group | Recognised channels (these can change) |
|---|---|
| Naver services | Naver Blog, SmartStore, Knowledge iN, Chzzk (치지직), Clip (클립) |
| Web channels | Karrot (당근), Threads, Instagram, YouTube, KakaoStory, Kakao Talk Channel, Tistory, TikTok, Facebook, X |

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "바삭 베이커리",
  "url": "https://www.example.co.kr/",
  "sameAs": [
    "https://blog.naver.com/example-bakery",
    "https://smartstore.naver.com/example-bakery",
    "https://www.instagram.com/example_bakery"
  ]
}
</script>
```

## Properties each Naver type needs

The table below lists the properties the guides name, with the limits that often fail.

| Type | Needs | Watch for |
|---|---|---|
| `PostalAddress` | `postalCode`, `addressRegion`, `addressLocality`, `streetAddress` | a page-specific address, not one site-wide footer repeated |
| `BreadcrumbList` | `itemListElement` of `ListItem` with `position`, item `@id` and `name` | broad to narrow; descriptive words, not "홈" or "top" |
| `ItemList` | `ListItem` with `name`, `image`, `url` and `position`, or an `item` holding them | one list per page, not a short list; original images with no duplicates |
| `AggregateRating` | `ratingValue`, and `ratingCount` or `reviewCount` | numbers of 0 or more; one per page; `ratingCount` shows first |
| `Review` | `reviewBody`, `reviewRating` with `ratingValue`, `bestRating` | nested in the reviewed thing; one reviewed thing per page; `bestRating` defaults to 5 |
| `Recipe` | `name`, `image`, `recipeYield`, `totalTime` (ISO 8601), `recipeIngredient`, `recipeInstructions` | not under `HowTo`; the finished dish, original image |
| `Restaurant` | `name`, `openingHours`, `telephone`, `image`, `url`, `servesCuisine`, `priceRange`, `description` | short facts, full phone with area code, currency in `priceRange` |
| `SoftwareApplication` | `name`, `applicationCategory`, `operatingSystem`, `url`, `screenshot`, `description` | one entry per system |
| `Movie` | `name`, `actor`, `director`, `genre`, `image`, `description` | the people to show first |
| `TVSeries` | `name`, `actor`, `creator`, `genre`, `image`, `description` | the people to show first |
| `VideoObject` | a partnership, then `name`, `description`, `url`, `thumbnailUrl`, `uploadDate`, `duration`, `cid` and `creator` | see "Video markup needs a partnership" |

## Video markup needs a partnership

Naver's video search takes external video only through a content partnership (서비스 콘텐츠 제휴, 동영상콘텐츠 제휴), which
differs from the other types here. The partner writes JSON-LD alone and pushes URLs through the crawl request API.

- A video page holds one top-level `VideoObject`, and a channel page one top-level `Person`, both as single objects with no
  `@graph`. Lists and playlists are not collected, and other JSON-LD on the page is ignored.
- Channels are always `Person`, even for a broadcaster or brand. The channel's name and URL sit in `creator`, and match
  the channel page.
- `cid`, `mobileUrl` and `mobileChannelUrl` are Naver extensions at the top level of `VideoObject`. Do not invent others.
- `uploadDate` is ISO 8601 with seconds and a time zone, and `duration` is an ISO 8601 duration such as `PT29M5S`.
- `name` is the video title alone, with no site suffix. `description` must match what the page shows.
- The URL in results, the URL a browser renders and the URL holding the markup must be the same.
- `offers` marks a video as paid and takes it out of results whatever the price, so never put it on a free video.
- A login-only video needs agreement first.

## A restaurant template for Naver

The template shows the facts a Naver restaurant result reads, with every value written for this example.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "바삭 베이커리 성수점",
  "openingHours": ["월-금 08:00-20:00", "토-일 09:00-19:00"],
  "telephone": "(02) 555-0100",
  "image": "https://www.example.co.kr/photos/seongsu.jpg",
  "url": "https://www.example.co.kr/stores/seongsu",
  "servesCuisine": ["소금빵", "바게트", "커피"],
  "priceRange": "3,500원 ~ 12,000원",
  "address": {
    "@type": "PostalAddress",
    "postalCode": "04790",
    "addressRegion": "서울",
    "addressLocality": "성동구",
    "streetAddress": "연무장길 00"
  }
}
</script>
```

## A breadcrumb and rating template for Naver

This template joins a breadcrumb with a product score, which is the pair most commerce pages need.

```html
<script type="application/ld+json">
[
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "item": {"@id": "https://www.example.co.kr/bread", "name": "식빵"}},
      {"@type": "ListItem", "position": 2, "item": {"@id": "https://www.example.co.kr/bread/milk", "name": "우유 식빵"}}
    ]
  },
  {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "우유 식빵 450g",
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.6", "bestRating": "5", "reviewCount": "128"}
  }
]
</script>
```
