---
name: ecommerce-seo
description: 'Applies SEO to online stores: category and product page templates, faceted navigation and filter URLs (index, canonicalise or block), product variants, pagination, out-of-stock and discontinued products, product structured data and merchant listings, Google Merchant Center free listings, product reviews, internal search pages, and catalogue-scale crawl control. Use when working on a shop''s categories, filters, product pages, variants, stock changes, Shopping visibility or crawl problems from millions of filter URLs.'
metadata:
  tags:
  - seo
  - ecommerce
  - faceted-navigation
  - product-pages
  - merchant-center
  - category-pages
---

# E-commerce SEO

E-commerce SEO deals with large catalogues that generate far more URLs than they have products: filters, sorts,
variants and pagination. The work is to give every page that matches real demand (categories, useful filtered
views, products) one strong URL, and to keep the rest from consuming crawl and splitting signals.

## Step 0: read the store's platform and URL counts

Read the platform and the crawl pattern first, because filters, variants and canonicals are set in the platform's
templates or apps, and the ratio of crawled URLs to products shows how big the problem is.

```bash
curl -s https://www.example.com/ | grep -ioE '<meta name="generator"[^>]*>|cdn\.shopify\.com|woocommerce|magento|bigcommerce' | sort -u
curl -s https://www.example.com/robots.txt | grep -iE '^(disallow|sitemap):'
awk '{print $7}' access.log | grep -oE '[?&][a-zA-Z_]+=' | tr -d '?&=' | sort | uniq -c | sort -rn | head -20
```

The last line needs an access log in the common format, and it ranks the URL parameters crawlers and visitors request.
Then note the number of live products and categories, the indexed and crawled counts from Page indexing and Crawl stats,
whether Merchant Center is connected, and who can change filter templates.

## Category pages

Category pages usually earn most of a store's organic traffic, because they match broad commercial queries ("trail
running shoes"). A strong category page has:

- A title and H1 for the category's main phrase (`keyword-research`), not "Products".
- A short intro above the products (one or two sentences) and helpful content below them: buying advice, size
  guides, FAQ written for buyers, links to sub-categories and guides.
- Crawlable links to every product, through pagination with real URLs (`canonical-urls`, pagination).
- Products in stock first; sort orders that do not change the URL, or that canonicalise to the default.
- `BreadcrumbList` markup; no `Product` markup for the whole listing.

## Faceted navigation and filters

Faceted navigation (filters by size, colour, brand, price) can create millions of URLs from one category. Decide per
filter, using search demand:

| Filter combination | Search demand | Treatment |
|---|---|---|
| category + one valuable attribute ("waterproof trail shoes", brand + category) | yes | an indexable page: clean path (`/trail-shoes/waterproof/`), unique title, H1 and intro, self canonical, in the sitemap, linked from the category |
| attribute combinations without demand (size + colour + price) | no | crawlable for users, `rel="canonical"` to the category, or blocked in robots.txt when the volume of URLs is large |
| sort, view, items per page | never | canonical to the default; never linked as separate pages |
| empty results | never | 404 (Google's faceted navigation guide), not a 200 "no products" page |

Google's faceted navigation guide (updated December 2025) says: when filtered URLs are not needed in Search, prevent their
crawling with robots.txt; use the standard `&` separator for parameters; keep filter order consistent; return 404 for
empty or nonsensical combinations; canonical tags reduce crawling of variants more slowly than robots.txt; fragment
(`#`) filters are not crawled at all.

```text
User-agent: *
Disallow: /*?*size=
Disallow: /*?*price=
Disallow: /*?*sort=
```

## Product pages

Product pages rank for specific product and model queries, and feed Shopping and merchant listings.

- Unique title: brand + model + key attribute ("Example Outdoor Runner X trail shoe, men's").
- Your own description: what it is for, specifications, sizing advice, materials, care. Manufacturer copy appears on
  every reseller site and adds nothing.
- Price, availability, delivery and returns as visible text, matching the structured data.
- Real customer reviews on the page; original photos and video.
- `Product` markup with `Offer` (merchant listing), shipping and return policy (`structured-data`, `google-rich-results`).
- Links to the category, related products and guides.

## Product variants

Product variants (sizes, colours) either share one URL or get one each; both work if signals agree.

| Approach | When | How |
|---|---|---|
| One URL, variants selected on the page | variants differ only in size or minor attributes | one canonical product URL; variant selection does not change the indexed URL, or variant parameters canonicalise to it |
| One URL per variant | variants are searched separately (colours, materials) | each variant URL self-canonical, distinct title and images; `ProductGroup` with `hasVariant` markup; each variant has its own `Offer` |

The Merchant Center feed, the structured data and the page must agree on each variant's URL, price and availability.

## Out-of-stock and discontinued products

Stock changes are handled so that URLs with value keep it.

| Situation | Action |
|---|---|
| temporarily out of stock | keep the page live (200), show availability and a restock date or alternatives; `availability: OutOfStock` in markup |
| discontinued, with a direct successor | 301 to the successor |
| discontinued, with similar products | keep the page with alternatives if it still gets traffic or links; otherwise 301 to the closest category |
| discontinued, no equivalent, no traffic or links | 404 or 410 |
| seasonal products | keep the URL every year; update content and stock |

## Google Merchant Center and free listings

Google Merchant Center sends product data to the Shopping tab, free product listings, Google Images and AI shopping
experiences. Free listings need no ad spend: create a Merchant Center account, verify and claim the site, add
shipping and returns, and submit products by feed, by Merchant API, or automatically from structured data on product
pages. Keep feed prices and availability in sync with the page; mismatches cause disapprovals. Google's AI guide
names current Merchant Center data as one of the things that helps in AI features.

## Shipping, returns and loyalty data

Shipping, returns and member prices can be shown with products in Google when Google knows the policies. Since
November 2025 a store can give them once for the whole site instead of per product: shipping and return policies in
Search Console's settings (no Merchant Center account needed; these take precedence over markup), or organization-level
structured data (`MerchantReturnPolicy` and `ShippingService` nested under `Organization`); loyalty programmes and
member prices use `MemberProgram` markup (since June 2025). Product-level `shippingDetails` and
`hasMerchantReturnPolicy` override organization-level markup only, so they carry exceptions to that markup; a policy
set in Search Console outranks them, and Google then uses only the Search Console setting. Check property names
against Google's merchant listing documentation before shipping, and keep the policies identical to the visible
policy pages.

Google's merchant listing docs gained three items in 2026: `category` on `Product` (your own text, or a Google Product
Category through `CategoryCode`), `hasAdultConsideration` for adult products, and sale dates on `Offer` (`validFrom`
with `validThrough` or `priceValidUntil`, in ISO 8601 with a time zone).

## Rewrite a catalogue in approved batches

A bulk rewrite of titles, descriptions or alt text can damage hundreds of products in one run, so it moves in steps.
Export the originals first. Rank products by revenue or traffic. Show three complete rewrites and get a yes on the
style, then apply about 25 at a time with an approval per batch and a check of the live pages. Mark any fact you cannot
confirm for the owner (material, weight, certification, delivery time) and leave it blank; a generated guess on a
product page is a false claim to a buyer.

## Internal search result pages

Internal search result pages (`/search?q=`) are infinite and low quality as landing pages. Keep them out of the index
with `noindex` and do not link to them; disallow `/search` in robots.txt when crawlers waste many requests there. If
a search query shows real demand, build a proper category or filtered page for it instead.

## Worked example: 3 million filter URLs on a 20,000-product store

Situation: Crawl stats show 3.1 million URLs crawled in 90 days for a store with 20,000 products; new products wait
three weeks to be crawled.

Logs: 82% of Googlebot requests hit `?size=`, `?price=`, `?sort=` and combinations. Decision per filter: brand and
"waterproof" get clean indexable pages (demand measured); size, price, sort and every combination are blocked in
robots.txt, and the filter controls for them stop rendering as `<a href>` links; empty combinations return 404. Check: Crawl stats show parameter URLs under 10% of requests within a month; new products
indexed within days.

## Verify store templates and filters

Store rules are proven on live URLs, one per template. Check filters first, then a product against its markup:

```bash
BASE=https://www.example.com
curl -s -o /dev/null -w 'empty filter: %{http_code}\n' "$BASE/trail-shoes/?size=99&color=none"      # expect 404
curl -sL "$BASE/trail-shoes/?sort=price" | grep -ioE '<link[^>]+rel="canonical"[^>]*>'              # expect the category URL
curl -s "$BASE/robots.txt" | grep -iE '^(Disallow|Allow):.*(size|price|sort)'                       # the filter rules you decided
curl -sL "$BASE/p/runner-x" > product.html
python3 - product.html <<'EOF'
import json, re, sys
html = open(sys.argv[1], encoding="utf-8", errors="replace").read()
for block in re.findall(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", html, re.S | re.I):
    try:
        data = json.loads(block)
    except ValueError as bad:
        print("INVALID JSON-LD:", bad)
        continue
    for item in data if isinstance(data, list) else data.get("@graph", [data]):
        offers = item.get("offers") if isinstance(item, dict) else None
        for offer in offers if isinstance(offers, list) else [offers] if offers else []:
            price = str(offer.get("price"))
            print(price, offer.get("priceCurrency"), offer.get("availability"), "on page" if price in html.replace(block, "") else "NOT ON PAGE")
EOF
```

A line marked `NOT ON PAGE` is a price the markup claims and the page does not show (a formatted price such as
`1,299.00` needs a manual look). Then read the Merchant listings report and Merchant Center diagnostics for price or
availability disapprovals, and Crawl stats with the server logs: parameter URLs should be a small share of Googlebot's
requests. The check on a discontinued product is its answer: 301 to the successor or category, or 404 or 410, as the
stock table says.

## Checklist for e-commerce SEO

The e-commerce checklist covers the templates that make or lose most of the traffic.

1. Each category has a unique title, H1, intro and helpful content; products linked through crawlable pagination.
2. Each filter decided: indexable page, canonical to category, or blocked; empty combinations return 404.
3. Product pages have own descriptions, visible price, availability, delivery and returns, and valid merchant
   listing markup.
4. Variant URLs, canonicals, markup and the feed agree.
5. Out-of-stock and discontinued rules implemented in the platform.
6. Merchant Center free listings active; feed in sync; no disapprovals for price or availability.
7. Internal search pages `noindex` and unlinked.
8. Crawl stats and Page indexing report show crawl spent on categories and products, not parameters.

## Gotchas in e-commerce SEO

The gotchas below are the most expensive store mistakes.

1. **Indexable filter combinations by the million.** Symptom: important products are crawled late, and Crawl stats
   show parameter URLs everywhere. Cause: crawl budget and the index fill with near-duplicates. Fix: decide per
   filter, and block the combinations without demand.
2. **Canonical from every product to its category.** Symptom: products disappear from search. Cause: a template bug
   points each product at its category. Fix: restore a self canonical and check one product per template after each
   release.
3. **Deleting out-of-stock products.** Symptom: links and traffic vanish, and the product returns later under a new
   URL. Cause: pages with value were deleted and re-created instead of kept. Fix: keep the URL and follow the stock
   table.
4. **Manufacturer descriptions.** Symptom: product pages are indexed but never rank above other resellers. Cause:
   copied text on thousands of products means nothing distinguishes the store. Fix: write your own description,
   starting with the best sellers.
5. **Price in markup or feed differs from the page.** Symptom: merchant listings drop after a sale, with Merchant
   Center disapprovals. Cause: the sale changed one source and not the others. Fix: generate the page, the markup and
   the feed from one price.
6. **Sort parameters linked from every category.** Symptom: logs show Googlebot crawling each category once per sort
   order. Cause: each sort is a duplicate URL crawled across the catalogue. Fix: canonical to the default and stop
   linking sorts as pages.

## Anti-patterns in e-commerce SEO

Anti-patterns in stores usually come from catalogue defaults nobody decided on.

| Do not | Do this instead |
|---|---|
| Adding `Product` markup to whole category listings | use `BreadcrumbList` there and keep `Product` for the product page |
| Serving "no products" with status 200 | answer 404 for empty or nonsensical filter combinations |
| Blocking all filters to be safe | measure demand first and give valuable filters a clean, indexable path |
| Using fragment filters for pages that should rank | use real URLs, since fragment filters are not crawled at all |
| Letting a script rewrite the catalogue in one run | show three rewrites, then move in approved batches of about 25 |

## See also for e-commerce SEO

- `structured-data`: Product and Offer markup
- `google-rich-results`: merchant listings, product snippets and the 2026 properties
- `canonical-urls`: parameters and pagination
- `crawling-and-indexing`: robots.txt rules, Crawl stats and server logs
- `image-and-video-seo`: product images and video
- `keyword-research`: demand for categories and filters
