---
name: google-rich-results
description: 'Decides which rich results a page can earn in Google Search: the structured data features Google supports (checked October 2026), merchant listings and product snippets, the properties Google added in 2026 such as Product category, hasAdultConsideration and sale dates in Offer and PriceSpecification, regional carousels, and the retired features to stop adding: FAQ rich results, HowTo, sitelinks search box, practice problems and the June 2025 group. Use when asking whether Google still shows FAQ or HowTo stars, which rich result fits a page type, why a rich result disappeared, what Search Console enhancement reports mean, or how to add sale dates to product markup.'
metadata:
  tags:
  - seo
  - google
  - rich-results
  - structured-data
  - merchant-listings
  - search-gallery
---

# Google rich results

A rich result is a Google Search listing with extra detail, such as a price, stars or event dates, and each one depends on
a feature Google still supports. The list changes often: types get retired and properties get added, and work spent on a
retired feature wins nothing. This skill says what Google shows today. How to write valid JSON-LD for any engine belongs
to `structured-data`.

## Step 0: read which features the site's pages already claim

Read the types each template emits, because the first question is whether any of them is retired or unsupported.

```bash
for u in https://www.example.com/ https://www.example.com/p/runner-x https://www.example.com/guides/fit; do
  printf '%s:' "$u"; curl -sL "$u" | grep -oE '"@type": *"[^"]+"' | sort | uniq -c | tr -s ' ' | tr '\n' ';'; echo
done
```

An empty result proves nothing on a page that adds JSON-LD with JavaScript, so read the rendered HTML in URL Inspection
too. Then open the enhancement reports in Search Console: they show which features Google already found on the site.

## Choose the rich result for a page

Pick from what the page is, because Google shows a feature only for content the page really holds.

| The page | Use | Why the others lose here |
|---|---|---|
| Sells a product, with a price and a way to buy | `Product` with `Offer` (merchant listing) | buyers purchase here; a merchant listing adds sizes, shipping and returns, and the page stays eligible for snippets |
| Reviews a product it does not sell | `Product` with `Review` (product snippet) | the merchant must be the seller, with `Offer`, not `AggregateOffer` |
| One question with answers from users | `QAPage` | `FAQPage` earns nothing in Google since 2026-05-07 |
| Questions the site answers itself | normal headings and text | FAQ rich results ended, so the value is in the text |
| Steps to do a job | normal headings and text | HowTo rich results were removed in 2023 |
| A forum thread | `DiscussionForumPosting` | `Article` does not describe people talking to each other |
| A person's profile on a platform | `ProfilePage` | `Person` alone does not earn creator details |

For merchant listings, Google recommends a global return policy under `Organization`; use one at `Offer` level only to
override it for products with their own terms.

## Google-supported rich result types in October 2026

Google's Search Gallery listed these structured data features on 2026-10-16. A type outside this list may still help
understanding but gets no rich result in Google. schema.org itself is at version 30.1 (September 2026).

| Page | Type(s) | Rich result |
|---|---|---|
| Any | `Organization` (home or about page) | logo, knowledge panel details |
| Any deep page | `BreadcrumbList` | breadcrumb trail in the result |
| News, blog | `Article`, `NewsArticle`, `BlogPosting` | better title, image and date |
| Product page | `Product` with `Offer` (merchant listing), or `Product` with `review`, `aggregateRating` or `offers` (product snippet) | price, availability, ratings, shipping, returns |
| Review | `Review`, `AggregateRating` inside a supported type | stars |
| Local business | `LocalBusiness` subtypes | business details |
| Event | `Event` | dates and venue |
| Video | `VideoObject` | video badge, key moments |
| Recipe | `Recipe` | image, time, ratings |
| Jobs | `JobPosting` | job listing experience |
| People | `ProfilePage` | creator details in forums and perspectives |
| Forums | `DiscussionForumPosting` | discussion results |
| Q&A pages | `QAPage` (one question with user answers) | Q&A result |
| Education | Education Q&A (`Quiz`), Math solver, Course list | education features |
| Data | `Dataset` | Dataset Search |
| Other | Carousel (with Recipe, Course, Restaurant or Movie), Employer aggregate rating, Image metadata, Movie, Software app, Speakable (beta), Subscription and paywalled content, Vacation rental | per feature |

## Properties Google added in 2026

Google's 2026 documentation changes added these properties to supported types:

| Type | Property | Use |
|---|---|---|
| `Product` | `category` | `Text` for your own product type, or `CategoryCode` with `inCodeSet` and `codeValue` for a Google Product Category |
| `Product`, variants | `hasAdultConsideration` | value `https://schema.org/SexualContentConsideration`; sellers of adult products must label them |
| `Offer` | `validFrom` with `validThrough` or `priceValidUntil` | sale dates; give start and end in ISO 8601 with a time zone |
| `PriceSpecification` | `validFrom`, `validThrough` | same dates; `priceValidUntil` does not apply to this type |
| `VideoObject` | `creator`, `interactionStatistic` | who made the video (`Person` or `Organization`, with a name); `InteractionCounter` is now preferred over `interactionCount` |

In the European Economic Area, South Africa and Türkiye, structured data carousels (beta) are a regional feature with
their own query types; Google's "regional differences" page lists them.

## Retired rich results: stop adding them

Google retired these rich results; the markup is harmless but wins nothing in Google, so do not add it for that
reason and do not report it as an error.

| Feature | Status |
|---|---|
| FAQ rich results (`FAQPage`) | limited to government and health sites in 2023; ended for all sites on 2026-05-07; documentation removed 2026-06-15; reporting removed mid-2026 |
| HowTo rich results | removed in 2023 |
| Sitelinks search box (`WebSite` + `SearchAction`) | removed in late 2024 |
| Book actions, Course info, ClaimReview (fact check), Estimated salary, Learning video, Special announcement, Vehicle listing | retired in June 2025 |
| Practice problems | deprecated 2025-11-05; documentation removed 2026-01-06 |

Bing and other consumers may still read some of these; keep accurate markup that is already in place.

## Worked example: a sale that needs dates, and FAQ blocks nobody should write

Request: a shoe store plans a sale from 1 to 7 November and asks for FAQ markup on every product page "for the stars".

The FAQ request ends at the table of retired features: `FAQPage` earns nothing in Google since 2026-05-07, so the team
adds the questions as normal text where buyers need them and skips the markup. The existing `FAQPage` blocks stay, because
they are harmless and may be read by others.

The sale is real work. The `Offer` already carries `price` and `priceCurrency` from the object that renders the page, so
it gains the dates in ISO 8601 with a time zone:

```json
{
  "@type": "Offer",
  "price": 79.00,
  "priceCurrency": "EUR",
  "availability": "https://schema.org/InStock",
  "validFrom": "2026-11-01T00:00:00+01:00",
  "validThrough": "2026-11-07T23:59:59+01:00"
}
```

Check: the Rich Results Test on three products shows a merchant listing with no errors, the Merchant listings report stays
flat on the first day of the sale, and the page shows the same price and end date.

## Verify rich result eligibility

Eligibility is proved by Google's own test and report, not by a schema validator. Run these in order.

1. **Rich Results Test** (search.google.com/test/rich-results): Google eligibility per feature, on a URL or a code
   snippet, with the rendered HTML.
2. **Search Console enhancement reports** (Merchant listings, Product snippets, Breadcrumbs, Videos and others): errors
   and warnings by template after crawling.
3. List the retired types still served, so a report can name them as harmless and nobody spends more on them:

```bash
curl -sL https://www.example.com/help | grep -oE '"@type": *"(FAQPage|HowTo|ClaimReview|SpecialAnnouncement)"' | sort | uniq -c
```

Fix errors (they block the feature); fix warnings when the data exists (they limit it). Schema.org validity and Google
eligibility are separate results: passing one says nothing about the other.

## Checklist for rich results

The checklist runs per template.

1. The type is on the supported list, or a reason is recorded for using another.
2. No new markup added for a retired feature.
3. Retired markup already in place is true, and is not reported as an error.
4. Sale dates carry a time zone; `priceValidUntil` is not used on `PriceSpecification`.
5. Adult products carry `hasAdultConsideration`.
6. The Rich Results Test passes for the chosen feature.
7. Enhancement reports checked two weeks after release.

## Gotchas with rich results

The gotchas below are the common reasons rich results do not appear.

1. **Expecting FAQ or HowTo stars.** Symptom: the markup validates and no stars appear. Cause: these features are
   retired. Fix: add the questions as normal content if readers need them.
2. **Rich result valid but not shown.** Symptom: the test passes and results stay plain. Cause: eligibility is not a
   promise; Google shows rich results when it judges them useful for the query and the site. Fix: keep the markup
   true, and judge by the enhancement report.
3. **Markup for AI answers.** Symptom: schema is added for AI Overviews and nothing changes. Cause: Google says no
   special schema is needed for AI Overviews or AI Mode; markup helps understanding and rich results, nothing more.
   Fix: add it only for those two reasons.
4. **A carousel missing in Europe.** Symptom: a structured data carousel looks different by country. Cause: in the
   European Economic Area, South Africa and Türkiye these carousels are a beta regional feature with their own query
   types. Fix: read Google's "regional differences" page before planning for one.
5. **Old advice on search boxes.** Symptom: a plugin still adds `WebSite` with `SearchAction` to get a search box. Cause:
   the sitelinks search box was removed in late 2024. Fix: leave the block alone or remove it; expect nothing from it.
6. **`priceValidUntil` refused on a price.** Symptom: sale dates on `PriceSpecification` do nothing. Cause: that property
   does not apply to the type. Fix: use `validFrom` and `validThrough` there.

## Anti-patterns with rich results

Anti-patterns here chase a feature and forget whether the page holds the content.

| Do not | Do this instead |
|---|---|
| Adding `FAQPage` to every page for stars | write the questions as text where readers need them |
| Reporting retired markup as an error | note it as harmless and leave it |
| Choosing a type because it earns a feature | choose the type that states what the page is |
| Promising a rich result to a client | promise eligibility, and report what the enhancement report shows |
| Trusting a list from an old article | read the Search Gallery, because the list changes |

## See also for rich results

- `structured-data`: JSON-LD rules, templates and validation for any engine
- `search-appearance`: titles, snippets, dates and site names
- `ecommerce-seo`: merchant listings in context
- `news-and-discover-seo`: `NewsArticle` in context
- `search-console`: reading the enhancement reports beside the others
- `bing-seo`, `naver-seo`: how those engines read markup
