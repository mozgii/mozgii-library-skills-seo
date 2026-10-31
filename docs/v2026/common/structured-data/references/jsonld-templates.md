---
title: JSON-LD templates per page type
author: MOZGII, Inc.
lang: en
description: Ready-to-edit JSON-LD for Organization, WebSite, BreadcrumbList, Article, Product, ProductGroup, LocalBusiness, Event, VideoObject and ProfilePage.
---

# JSON-LD templates per page type

These JSON-LD templates are starting points: replace every value with data from the page, delete properties the
page cannot support, and validate with the Rich Results Test. All examples use `example.com`.

## Contents

1. Organization and WebSite
2. BreadcrumbList
3. Article
4. Product with Offer, shipping and returns
5. ProductGroup for variants
6. LocalBusiness
7. Event
8. VideoObject
9. ProfilePage

## Organization and WebSite JSON-LD

The Organization block sits once on the home page, or on the about page instead, with an `@id` other blocks reference. Google
uses `logo`, `url`, `sameAs`, contact and legal details; `MerchantReturnPolicy` and shipping can be set here for the
whole store.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.example.com/#organization",
      "name": "Example Outdoor",
      "legalName": "Example Outdoor Ltd",
      "url": "https://www.example.com/",
      "logo": "https://www.example.com/img/logo-512.png",
      "sameAs": ["https://www.linkedin.com/company/example-outdoor", "https://www.youtube.com/@exampleoutdoor"],
      "contactPoint": {"@type": "ContactPoint", "telephone": "+1-555-0100", "contactType": "customer service"},
      "hasMerchantReturnPolicy": {
        "@type": "MerchantReturnPolicy",
        "applicableCountry": "US",
        "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
        "merchantReturnDays": 30,
        "returnMethod": "https://schema.org/ReturnByMail",
        "returnFees": "https://schema.org/FreeReturn"
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://www.example.com/#website",
      "url": "https://www.example.com/",
      "name": "Example Outdoor",
      "publisher": {"@id": "https://www.example.com/#organization"}
    }
  ]
}
```

`WebSite` with `name` helps Google show the site name in results; the sitelinks search box it once enabled is retired.

## BreadcrumbList JSON-LD

BreadcrumbList mirrors the visible breadcrumb trail; the last item may omit `item` (the current page).

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Running shoes", "item": "https://www.example.com/running-shoes/"},
    {"@type": "ListItem", "position": 2, "name": "Trail", "item": "https://www.example.com/running-shoes/trail/"},
    {"@type": "ListItem", "position": 3, "name": "Runner X"}
  ]
}
```

## Article JSON-LD

Article markup has no required properties in Google; `headline`, `image`, `datePublished`, `dateModified` and
`author` with a `url` to an author page are the useful ones. Images: at least 50,000 pixels (width × height), in
16x9, 4x3 and 1x1 if possible.

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "How to choose trail running shoes",
  "image": ["https://www.example.com/img/guide-16x9.jpg", "https://www.example.com/img/guide-4x3.jpg", "https://www.example.com/img/guide-1x1.jpg"],
  "datePublished": "2026-09-02T08:00:00+00:00",
  "dateModified": "2026-10-14T10:20:00+00:00",
  "author": [{"@type": "Person", "name": "Alex Doe", "url": "https://www.example.com/authors/alex-doe", "jobTitle": "Running coach"}],
  "publisher": {"@id": "https://www.example.com/#organization"}
}
```

## Product with Offer, shipping and returns

Product markup with an `Offer` makes a page eligible for merchant listings (price, availability, shipping, returns);
`name`, `image` and `offers.price` with `priceCurrency` are required. Ratings need visible reviews.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Runner X trail shoe",
  "image": ["https://www.example.com/img/runner-x-1x1.jpg"],
  "description": "Trail running shoe with 5 mm lugs and a rock plate.",
  "sku": "RX-2026-BLU-42",
  "gtin13": "0123456789012",
  "brand": {"@type": "Brand", "name": "Example Outdoor"},
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.6, "reviewCount": 128},
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.com/p/runner-x",
    "price": 129.00,
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": {"@type": "MonetaryAmount", "value": 0, "currency": "USD"},
      "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "US"},
      "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
        "transitTime": {"@type": "QuantitativeValue", "minValue": 2, "maxValue": 5, "unitCode": "DAY"}
      }
    }
  }
}
```

The return policy here comes from the Organization block. Add `hasMerchantReturnPolicy` to an offer only when that
product's policy differs; a per-offer policy overrides the organization one.

## ProductGroup JSON-LD for variants

ProductGroup describes one product sold in several variants (size, colour); each variant is a `Product` with its own
URL or URL parameter, SKU and offer.

```json
{
  "@context": "https://schema.org",
  "@type": "ProductGroup",
  "name": "Runner X trail shoe",
  "productGroupID": "RX-2026",
  "variesBy": ["https://schema.org/size", "https://schema.org/color"],
  "hasVariant": [
    {"@type": "Product", "sku": "RX-2026-BLU-42", "size": "42", "color": "Blue",
     "offers": {"@type": "Offer", "url": "https://www.example.com/p/runner-x?size=42&color=blue", "price": 129.00, "priceCurrency": "USD", "availability": "https://schema.org/InStock"}},
    {"@type": "Product", "sku": "RX-2026-BLK-43", "size": "43", "color": "Black",
     "offers": {"@type": "Offer", "url": "https://www.example.com/p/runner-x?size=43&color=black", "price": 129.00, "priceCurrency": "USD", "availability": "https://schema.org/OutOfStock"}}
  ]
}
```

## LocalBusiness JSON-LD

LocalBusiness markup describes a physical location; use the most specific subtype and one block per location page.
The details must match the Google Business Profile and the visible page.

```json
{
  "@context": "https://schema.org",
  "@type": "SportingGoodsStore",
  "@id": "https://www.example.com/stores/springfield#store",
  "name": "Example Outdoor Springfield",
  "url": "https://www.example.com/stores/springfield",
  "telephone": "+1-555-0142",
  "image": "https://www.example.com/img/store-springfield.jpg",
  "priceRange": "$$",
  "address": {"@type": "PostalAddress", "streetAddress": "100 Main St", "addressLocality": "Springfield", "addressRegion": "IL", "postalCode": "62701", "addressCountry": "US"},
  "geo": {"@type": "GeoCoordinates", "latitude": 39.7990, "longitude": -89.6440},
  "openingHoursSpecification": [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "19:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "10:00", "closes": "17:00"}
  ],
  "parentOrganization": {"@id": "https://www.example.com/#organization"}
}
```

## Event JSON-LD

Event markup needs `name`, `startDate` and `location`; online events use `VirtualLocation` and
`eventAttendanceMode`. Update `eventStatus` when an event moves or is cancelled instead of deleting the page.

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Springfield trail running clinic",
  "startDate": "2026-11-14T09:00:00-06:00",
  "endDate": "2026-11-14T12:00:00-06:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {"@type": "Place", "name": "Example Outdoor Springfield", "address": {"@type": "PostalAddress", "streetAddress": "100 Main St", "addressLocality": "Springfield", "addressRegion": "IL", "postalCode": "62701", "addressCountry": "US"}},
  "offers": {"@type": "Offer", "url": "https://www.example.com/events/clinic", "price": 0, "priceCurrency": "USD", "availability": "https://schema.org/InStock"},
  "organizer": {"@id": "https://www.example.com/#organization"}
}
```

## VideoObject JSON-LD

VideoObject markup needs `name`, `thumbnailUrl` and `uploadDate`; `contentUrl` or `embedUrl` lets Google fetch the
file. `Clip` or `SeekToAction` enable key moments. `creator` and `interactionStatistic` are recommended; Google
accepts `WatchAction`, `LikeAction`, `CommentAction` and `ShareAction` as the interaction type.

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "How to lace trail shoes for downhill running",
  "description": "Three lacing methods that stop toes hitting the front of the shoe.",
  "thumbnailUrl": ["https://cdn.example.com/thumbs/lacing.jpg"],
  "uploadDate": "2026-09-02T08:00:00+00:00",
  "duration": "PT3M34S",
  "contentUrl": "https://cdn.example.com/video/lacing.mp4",
  "creator": {"@type": "Person", "name": "Alex Doe", "url": "https://www.example.com/authors/alex-doe"},
  "interactionStatistic": {"@type": "InteractionCounter", "interactionType": {"@type": "WatchAction"}, "userInteractionCount": 18420},
  "hasPart": [{"@type": "Clip", "name": "Heel lock", "startOffset": 35, "endOffset": 92, "url": "https://www.example.com/guides/lacing?t=35"}]
}
```

## ProfilePage JSON-LD

ProfilePage marks a page about one person or organization, such as an author page or a forum profile; `mainEntity`
holds the person.

```json
{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "dateCreated": "2024-03-01T00:00:00+00:00",
  "mainEntity": {
    "@type": "Person",
    "name": "Alex Doe",
    "jobTitle": "Running coach",
    "image": "https://www.example.com/img/alex-doe.jpg",
    "sameAs": ["https://www.linkedin.com/in/alex-doe-example"]
  }
}
```
