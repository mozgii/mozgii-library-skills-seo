---
name: structured-data
description: 'Writes, validates and debugs schema.org structured data in JSON-LD for any search engine: choosing the format, the rules every markup must follow, ready templates for Organization, Article, Product, LocalBusiness, BreadcrumbList, Event, Video, ProfilePage and more, plus Open Graph and social cards. Use when adding schema markup to a template, when a validator or Search Console reports structured data errors, when markup and page disagree, or when writing JSON-LD by hand.'
metadata:
  tags:
  - seo
  - structured-data
  - schema-org
  - json-ld
  - rich-results
  - open-graph
---

# Structured data in JSON-LD

Structured data is machine-readable markup, written with the schema.org vocabulary, that states what a page is
about: a product with a price, an article with an author, a business with opening hours. Search engines use it to
understand pages and, for some types, to show rich results (stars, prices, event dates, breadcrumbs). It is not a
ranking boost by itself, and it is not required to appear in AI answers.

## Step 0: read the markup the site already outputs

Read what each template emits first, because a theme, a plugin and a tag manager can each add their own block, and a
second copy of a type is a common cause of errors.

```bash
for u in https://www.example.com/ https://www.example.com/p/runner-x https://www.example.com/guides/fit; do
  printf '%s:' "$u"; curl -sL "$u" | grep -oE '"@type": *"[^"]+"' | sort | uniq -c | tr -s ' ' | tr '\n' ';'; echo
done
```

An empty result proves nothing on a page that adds JSON-LD with JavaScript, so read the rendered HTML in URL Inspection
too. Then read the Search Console enhancement reports and find what writes each block.

## Choose JSON-LD

JSON-LD is the format Google recommends where a site's setup allows it: one `<script type="application/ld+json">`
block, separate from the HTML, easy to generate from the same data that renders the page. Google rates all three formats
"equally fine" when the markup is valid, so Microdata and RDFa also work. Put the block in the server HTML; Google can
read JSON-LD injected by JavaScript, but other consumers often cannot.

| Format | Use it when | What it costs |
|---|---|---|
| JSON-LD in the server HTML | almost always | it stays apart from the HTML, so it must come from the same data as the page or the two drift |
| JSON-LD added by JavaScript | a tag manager is the only way in | Google can read it, but other consumers often cannot; on `Product` markup, Google warns that dynamic generation can leave Shopping crawls less frequent and less reliable, a risk for fast-changing prices and availability |
| Microdata | a template already carries it | it ties the markup to the HTML, so a redesign can break it |
| RDFa | an existing system emits it | Google and Bing read it, but Naver recommends only JSON-LD or Microdata |

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to choose trail running shoes",
  "datePublished": "2026-09-02T08:00:00+00:00",
  "dateModified": "2026-10-14T10:20:00+00:00",
  "author": [{"@type": "Person", "name": "Alex Doe", "url": "https://www.example.com/authors/alex-doe"}],
  "image": ["https://www.example.com/img/trail-shoes-16x9.jpg"]
}
</script>
```

Which types earn a rich result in Google today, which are retired, and the properties added in 2026: the
`google-rich-results` skill.

## Rules every markup must follow

Google's structured data guidelines make markup eligible only when it describes the page truthfully.

- Mark up only content visible on the page; values in JSON-LD match what users see (price, rating, date, author).
- Mark up the main item of the page, not every item on a listing page (listing pages use `ItemList` only where a
  feature asks for it).
- No reviews written by the business about itself on `LocalBusiness` or `Organization` (self-serving reviews are not
  eligible for stars). The same applies to reviews of the business shown through an embedded third-party widget.
- No fake reviews, and no reviews given in exchange for cash, discounts, vouchers or free products unless the page
  clearly discloses the incentive (a guideline added in July 2026; it covers the page as well as the markup).
- Never invent a value. A rating, price, date, author or address that neither the page nor the owner confirms stays
  out; when a required fact is missing, list what you need instead of shipping a template with a guess in it.
- Use the most specific type (`ShoeStore`, not `Store`, when it fits); required properties present, recommended ones
  where the data exists.
- Absolute URLs; ISO 8601 dates with a time zone; prices as numbers with `priceCurrency`.
- One entity per thing across the site: give it an `@id` (`https://www.example.com/#organization`) and reference it.

Violations can lead to a manual action for structured data in Search Console, which removes rich results sitewide.

## Verify

Structured data is validated before release and monitored after.

1. **Rich Results Test** (search.google.com/test/rich-results): Google eligibility per feature, on a URL or a code
   snippet, with the rendered HTML.
2. **Schema Markup Validator** (validator.schema.org): schema.org validity for any type, including ones Google does
   not use.
3. **Search Console enhancement reports** (Merchant listings, Product snippets, Breadcrumbs, Videos and others): errors
   and warnings by template after crawling.
4. List the types a page's JSON-LD carries and catch blocks that do not parse:

```bash
curl -sL https://www.example.com/p/runner-x | python3 -c '
import json, re, sys
html = sys.stdin.read()
for block in re.findall(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", html, re.S | re.I):
    try:
        data = json.loads(block)
    except ValueError as e:
        print("INVALID_JSON", e); continue
    items = data if isinstance(data, list) else data.get("@graph", [data])
    print([i.get("@type") for i in items if isinstance(i, dict)])'
```

The script reads raw HTML, so an empty result proves nothing on a page that injects JSON-LD through a tag manager or
JavaScript; check the rendered HTML in URL Inspection or the Rich Results Test before reporting markup as missing.

Fix errors (they block the feature); fix warnings when the data exists (they limit it). Schema.org validity and Google
eligibility are separate results: passing one says nothing about the other.

## Templates per page type

Ready-to-edit JSON-LD for the common page types (Organization, WebSite, BreadcrumbList, Article, Product with Offer,
shipping and returns, ProductGroup variants, LocalBusiness, Event, VideoObject, ProfilePage) is in
[references/jsonld-templates.md](references/jsonld-templates.md). Open Graph and social card tags, which are not
schema.org but control previews in social apps and chat tools, are in
[references/open-graph.md](references/open-graph.md).

## Worked example: product snippets lost after a sale

Situation: Search Console's Merchant listings report jumps from 0 to 1,900 invalid items the day a sale starts;
price rich results disappear.

Diagnosis: the JSON-LD comes from a cached product feed that still holds pre-sale prices, while the page shows sale
prices; some offers also lost `priceCurrency` when the sale plugin rewrote them. Fix: generate the `Offer` from the
same price object the page renders, with `price` as a number and `priceCurrency`; add `priceValidUntil` for the sale
end. Check: Rich Results Test on three products, then Validate fix in the report.

## Checklist for structured data

The structured data checklist runs per template, not per page.

1. Type chosen for what the page is, the most specific that fits, with the engines that read it in mind.
2. JSON-LD in the server HTML, generated from the same data as the visible page.
3. Required properties present; values match the visible content.
4. Rich Results Test passes; Schema Markup Validator shows no errors.
5. Organization and WebSite defined once with `@id` and referenced elsewhere.
6. Search Console enhancement reports checked two weeks after release.

## Gotchas with structured data

The gotchas below are the common reasons rich results disappear.

1. **Price in markup differs from the page.** Symptom: rich results disappear after a sale or currency switch. Cause:
   the markup and the page come from different sources. Fix: generate both from one source.
2. **Ratings marked up with no visible reviews.** Symptom: a warning or a manual action for structured data. Cause:
   stars have no reviews on the page, or reviews collected about the business are shown as its own stars. Fix: mark up
   only reviews shown and eligible.
3. **Markup only on desktop templates.** Symptom: the enhancement report shows fewer items than expected. Cause:
   mobile-first indexing reads the mobile HTML. Fix: put the same markup on both.
4. **Several conflicting Organization blocks.** Symptom: the validator lists duplicates with different names or logos.
   Cause: plugins each add their own. Fix: keep one, referenced by `@id`.
5. **Markup for AI answers.** Symptom: schema is added for AI Overviews and nothing changes. Cause: Google says no
   special schema is needed for AI Overviews or AI Mode; markup helps understanding and rich results, nothing more.
   Fix: add it only for those two reasons.
6. **"No schema found" from a plain fetch.** Symptom: `curl` reports nothing on a page that has markup. Cause: the
   markup is added after load, so a raw fetch misses it. Fix: inspect the rendered page before writing the finding.
7. **Warnings read as errors.** Symptom: a report lists missing recommended properties as failures. Cause: a missing
   recommended property limits a feature and does not remove it. Fix: add it when the data is real; do not fill it to
   silence a validator.

## Anti-patterns in structured data

Anti-patterns with markup treat it as a ranking trick and not a true description of the page.

| Do not | Do this instead |
|---|---|
| Inventing a rating, price or date to pass a test | list what you need from the owner |
| Marking up every item on a listing page | mark up the main item |
| Reporting retired markup as an error | leave it; it is harmless |
| Hand-editing JSON-LD per page | generate it from the data that renders the page |
| Checking only one validator | run the Rich Results Test and the Schema Markup Validator, since they answer different questions |

## See also for structured data

- `google-rich-results`: which features Google supports, retired ones and the 2026 properties
- `search-appearance`: how markup feeds titles, dates and site names
- `ecommerce-seo`: merchant listings in context
- `local-seo`: `LocalBusiness` in context
- `news-and-discover-seo`: `NewsArticle` in context
- `ai-search-visibility`: what markup does for AI answers
- `naver-seo`: the types Naver reads
