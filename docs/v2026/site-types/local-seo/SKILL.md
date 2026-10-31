---
name: local-seo
description: 'Improves visibility in local search and maps for businesses that serve customers in a place: Google Business Profile setup and guidelines, categories, service areas, reviews and responses, consistent name, address and phone (NAP), local citations, location pages that are not doorways, LocalBusiness markup, Bing Places, Apple Business and Yandex Business, and local rank tracking. Use for ''near me'' and city searches, the map pack, a Business Profile that is suspended or not showing, multi-location sites, or reviews strategy.'
metadata:
  tags:
  - seo
  - local-seo
  - google-business-profile
  - reviews
  - citations
  - maps
---

# Local SEO and business listings

Local SEO makes a business appear when people search for what it offers near them: the map pack, maps apps, and
local organic results. Google says local results depend on three things: relevance (how well the listing matches the
search), distance (from the searcher or the place named), and prominence (how well known the business is, from
reviews, links, articles and its overall web presence).

## Step 0: read the listings and the site as they stand

Read what already exists before editing, because a second profile for one place is a duplicate and key edits can
trigger re-verification. Collect who owns the Business Profile, every location, the primary category, whether the
address shows, and the service areas. Then read the facts the site states:

```bash
curl -s https://www.example.com/locations/leeds/ | grep -ioE '"(@type|name|telephone|streetAddress|addressLocality)": *"[^"]*"'
curl -s https://www.example.com/sitemap.xml | grep -oE '<loc>[^<]*(location|store|area)[^<]*' | wc -l
```

Compare the name, address and phone with the profile, then with the top directories.

## Storefront, service-area or hybrid business

Whether customers come to the business, the business goes to them, or both decides what the profile shows, so answer
it before any other profile edit.

| Type | Test | Address on the profile | Service area | Location pages |
|---|---|---|---|---|
| Storefront | customers come to a staffed address with permanent signage | show it | none needed | one per real address |
| Service-area business | it visits or delivers to customers and serves nobody at its address | remove it | up to 20 areas, no radius, about two hours' drive from base at most | one per area, only where it has jobs, photos and reviews |
| Hybrid | it serves customers at its address and also visits or delivers | show it | set it as well; the site must be staffed and open in its stated hours | one per real address, plus areas with real work |

Each wrong choice has a cost. A home-based plumber shown as a storefront breaks the address rule and risks suspension.
A shop that hides its address loses direction requests, and a hybrid set up as storefront-only says nothing about the
towns it serves. Businesses tied to age-restricted products (alcohol, cannabis, weapons) cannot be service-area
businesses without a storefront.

## Google Business Profile setup

The Google Business Profile is the listing behind the map pack, and it must follow Google's guidelines exactly or it
is suspended.

- **Name**: the real-world business name as on signage and documents. Adding keywords or a city ("Joe's Plumbing
  Springfield Emergency 24/7") is against the guidelines and a common cause of suspension.
- **Address**: a real location where staff meet customers in staffed hours. No virtual offices or mailboxes.
  Service-area businesses (plumbers, cleaners) hide the address and list the areas they serve.
- **Categories**: the primary category is the strongest relevance signal; choose the most specific one ("Running
  store", not "Store"), then a few secondary categories that are true.
- **Hours** including holiday hours; **phone** with a local number; **website** linking to the matching location page.
- **Services or products**, attributes, photos (exterior, interior, team, work) and a short description without
  links or promotions.
- **Verification**: by video, phone, email or postcard as Google offers; edits to key fields may trigger
  re-verification.

## Reviews

Reviews are a prominence signal and the main thing searchers read. Ask every customer, at the moment of
satisfaction, with a direct review link (Business Profile › Ask for reviews).

- Never pay or give discounts for reviews, never ask only happy customers ("review gating"), never post reviews for
  yourself or competitors. All are against Google's policies and against consumer-protection law in many countries.
- Reply to every review within a few days, especially negative ones: thank, address the issue, move details to a
  private channel.
- Report reviews that break policy (spam, conflicts of interest, off-topic) through the profile; do not argue in
  replies.
- Do not mark up your own reviews of yourself with `AggregateRating` on the site; self-serving review stars are not
  eligible.

## NAP consistency and citations

NAP is the business's name, address and phone. Search engines cross-check it across the web, and inconsistent copies
weaken trust in the listing.

1. Write one canonical NAP (exact spelling, suite numbers, phone format) and use it everywhere.
2. Fix the core listings first: Google Business Profile, Bing Places, Apple Business, Facebook, and the main
   directories of the country and industry (Yelp in the US, Yandex Business and 2GIS in Russian-speaking markets).
3. Search for old addresses and phone numbers (`"old street name" "business name"`) and update or remove those
   listings.
4. Prefer quality and relevance to volume: a listing on an industry association site beats a hundred generic
   directories.

## Location pages

Location pages give each physical location or service area its own page on the site. They rank when each page
carries information specific to that place, and are doorways when only the city name changes.

Each location page carries: the NAP as text, opening hours, a map embed or directions, staff or team photos, services
available at that location, local reviews or cases, parking and access details, a `LocalBusiness` JSON-LD block
(`structured-data`), and links to and from the locations hub. The Business Profile's website field links to this
page, not to the home page.

Service-area pages (one business, many towns): publish a page for a town only when you have something specific to
say: jobs done there, local regulations, prices or response times that differ, local reviews.

## Other local platforms

Local platforms beyond Google each have their own listing and audience.

| Platform | Where it shows | Note |
|---|---|---|
| Bing Places for Business | Bing, Copilot, Windows maps | can import from Google Business Profile |
| Apple Business | Apple Maps, Siri, Spotlight | brand and location details, photos, actions |
| Yandex Business (Яндекс Бизнес) | Yandex Search and Maps | essential for Russian-speaking markets; see `yandex-seo` |
| 2GIS | 2GIS maps and app | strong in Russia and Central Asia |
| Industry directories | vertical search (restaurants, health, legal) | often rank in local organic results themselves |

## Business Profile changes to know

Google has removed several Business Profile features in recent years: the free Business Profile websites
(`business.site`) were shut down in 2024 and now link nowhere useful, and chat and call history were retired.
Link the profile to a page on your own site, and use the profile's own fields (services, products, photos, updates)
rather than relying on removed features.

## Track local rankings

Local rankings change with the searcher's location, so a single rank number is misleading. Use a grid rank tracker
that checks the same query from points across the service area, and read Business Profile performance (searches,
views, calls, direction requests, website clicks) together with Search Console filtered to the location pages.

## Worked example: a plumber with three vans and no office

Situation: a plumbing business works from the owner's home and serves 12 towns; the profile shows the home address
and the name "Joe's Plumbing Springfield 24/7 Emergency Plumber".

Fix: rename to the registered name "Joe's Plumbing"; switch to a service-area business (address hidden, the 12 towns
listed); primary category "Plumber"; add a review request link to the invoice email; build one service-area page per
town only where the team has jobs, photos and reviews from that town (five of twelve), each with `LocalBusiness` markup
listing `areaServed`. Check: profile insights (calls, direction requests are not expected now) and a grid rank report
for "plumber" across the service area after two months.

## Verify listings and location pages

Local work is checked in two places: the location pages, which a script can read, and the listings, which a person
reads. Compare every location page's name, address and phone with the one canonical NAP:

```bash
for url in https://www.example.com/locations/leeds https://www.example.com/locations/york; do
  curl -sL "$url" | python3 -c '
import json, re, sys
html = sys.stdin.read()
for block in re.findall(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", html, re.S | re.I):
    try:
        data = json.loads(block)
    except ValueError as bad:
        print("INVALID JSON-LD:", bad)
        continue
    for item in data if isinstance(data, list) else data.get("@graph", [data]):
        if isinstance(item, dict) and "address" in item:
            print(item.get("name"), "|", item.get("telephone"), "|", item.get("address"))'
done
```

Each line must match the canonical NAP exactly, and that phone number must also appear as text on the page. Then open
each listing (Google Business Profile, Bing Places, Apple Business, Yandex Business or 2GIS where they matter)
and confirm the name, the hours and the website field, which must point to the matching location page. Search each old
address and old phone number in quotes: nothing current should show them. Results follow in Business Profile
performance and in a grid rank report after about two months.

## Checklist for local SEO

The local checklist covers the listing, the site and reputation.

1. Business Profile verified; real name; correct primary category; hours, phone and website set.
2. Address or service areas follow the guidelines; no virtual office.
3. One canonical NAP; core listings (Google, Bing, Apple, main local directories) match it.
4. Review requests built into the customer process; every review answered.
5. One location page per location with specific content and `LocalBusiness` markup; the profile links to it.
6. Local performance reviewed monthly (profile insights, Search Console, grid tracking).

## Gotchas in local SEO

The gotchas below cause suspensions and lost map rankings.

1. **Keywords in the business name.** Symptom: a higher map rank for a while, then the profile is suspended or edited
   by Google. Cause: the name no longer matches the guidelines. Fix: use the real-world name.
2. **Virtual offices and co-working addresses.** Symptom: the profile is suspended. Cause: such an address has no
   staffed presence. Fix: use a real staffed location, or a service-area profile.
3. **Changing the name, address and category at once.** Symptom: the profile asks for verification again and drops
   from view. Cause: editing key fields together triggers re-verification. Fix: change one at a time.
4. **Review campaigns with incentives.** Symptom: reviews vanish and a warning shows on the profile. Cause: incentives
   break the policy and carry legal risk. Fix: ask every customer, and offer nothing.
5. **City-swap doorway pages.** Symptom: pages for every town in a 50 km radius stay unindexed or draw a manual
   action. Cause: only the city name changes, which makes them doorways. Fix: publish a town page only with something
   specific to say.
6. **Profile website link to the home page.** Symptom: a multi-location business's profiles compete for one vague
   page. Cause: each profile sends its traffic to the home page. Fix: link each profile to its location page.

## Anti-patterns in local SEO

Anti-patterns in local search trade a short gain for a suspended listing.

| Do not | Do this instead |
|---|---|
| Asking only happy customers for reviews | ask every customer at the moment of satisfaction |
| Arguing with reviewers in public replies | thank them, address the issue and move details to a private channel |
| Buying bulk directory submissions | fix the core listings, then a few relevant directories |
| Marking up your own testimonials as `AggregateRating` | leave them out, since self-serving stars are not eligible |
| Linking the profile to a retired `business.site` page | link a page on your own site |

## See also for local SEO

- `structured-data`: `LocalBusiness` markup
- `google-rich-results`: what Google shows for it
- `programmatic-seo`: location pages at scale without doorways
- `yandex-seo`: Yandex Business and regions
- `link-building`: local links and citations
- `search-console`: performance by location page
