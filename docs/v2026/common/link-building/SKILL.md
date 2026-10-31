---
name: link-building
description: 'Earns and audits backlinks within search engine rules: what links do for rankings, link spam policies, rel sponsored, ugc and nofollow, earning links with original data, tools and digital PR, unlinked mentions and broken-link reclaim, backlink audits, when the disavow tool is needed and when it is not, and reading the Search Console Links report. Use when planning link building or digital PR, reviewing a backlink profile, handling a manual action for unnatural links, buying or selling sponsored content, or asking whether to disavow.'
metadata:
  tags:
  - seo
  - link-building
  - backlinks
  - digital-pr
  - disavow
  - off-page
---

# Link building and backlink audits

Backlinks are links from other sites to yours. Search engines use them to discover pages and as one of many signals
of importance and trust; a link from a relevant, respected site that a person chose to place is worth more than any
number of links placed to influence rankings, which Google's spam systems try to ignore or penalise.

## Step 0: read the site's backlink state

Read the current link profile first, because past paid links, a disavow file or a manual action change what is safe to
do next. Collect Search Console › Links (top linked pages, top linking sites) and export the external links. Read
Manual actions, ask whether a disavow file exists and who uploaded it, and ask what any agency bought. Bing Webmaster
Tools shows backlinks too.

```bash
cut -d, -f1 latest-links.csv | awk -F/ 'NR>1 {print $3}' | sort | uniq -c | sort -rn | head -20   # linking domains, most links first
curl -sIL -o /dev/null -w '%{http_code} %{url_effective}\n' https://www.example.com/old-guide/      # a top linked page still answers 200
```

The first line expects the linking URL in the first column of the export. A top linked page that answers 404 is the
cheapest win on the site: redirect it to its closest live page.

## Link rules from search engines

Google's spam policies define link spam as links made mainly to manipulate rankings. Examples:

- paying for links that carry ranking value, or selling them, whether the price is money, goods, services or free
  products;
- excessive link exchanges ("link to me and I'll link to you");
- large-scale article marketing or guest posting with keyword-rich anchor links;
- automated programs or services that create links;
- links required by terms of service or contracts, widgets with hidden or keyword-rich links;
- low-quality directory or bookmark links, and keyword-rich links in footers or templates across many sites.

Bing and Yandex have similar rules; Yandex's Minusinsk filter targets bought links (`yandex-seo`).

## Link attributes

Link attributes tell search engines how a link was placed; Google treats them as hints.

| Attribute | Use for |
|---|---|
| `rel="sponsored"` | paid placements, affiliate links, sponsored posts, links given in exchange for products |
| `rel="ugc"` | links in comments, forum posts and other user-generated content |
| `rel="nofollow"` | any other link you do not want to vouch for |

Sponsored content is fine for marketing reach; the links in it must carry `sponsored` (or `nofollow`), and the
content should be labelled as sponsored for readers.

## Earning links

Links are earned by giving other sites a reason to cite you. Methods that work at scale without breaking the rules:

| Method | How |
|---|---|
| Original data | surveys, studies, indexes, benchmarks from your own data; publish the method and a press-ready summary |
| Useful tools and resources | calculators, templates, checklists, glossaries people link to from their own guides |
| Digital PR | newsworthy stories, expert commentary for journalists (journalist request services), reactive comment on news in your field |
| Unlinked mentions | find articles that name the brand without a link; ask politely for a link to the most relevant page |
| Broken link reclaim | your own pages that return 404 but have links: 301 them to the best current page |
| Broken link building | others' dead links to resources like yours: offer your page as a replacement |
| Partners and associations | suppliers, customers, associations, events you sponsor (with `sponsored` where paid) |
| Expert content | guest articles written for the audience, with at most a natural author link |

Reclaim your own lost link value first; it is the cheapest win. Find 404 pages with backlinks in Search Console ›
Links › Top linked pages, cross-checked with a crawl or server log of 404s.

## Backlink audit

A backlink audit checks what links point to the site and whether any create risk.

1. Export links from Search Console › Links (top linking sites, top linked pages, linking text), Bing Webmaster Tools ›
   Backlinks, and one third-party index for completeness.
2. Group by referring domain; review the top domains, the anchor text distribution and sudden spikes.
3. Flag: links you or a past agency paid for or exchanged without `sponsored`; networks of low-quality sites with
   exact-match anchors; hacked-site or spam-injection links.
4. Act: remove or add `sponsored` to links you control or paid for; leave random spam alone.

Most sites have spam links pointing to them; Google says it ignores most of them automatically. "Toxic score" figures
from tools are vendor estimates, not Google signals: Google says third-party tools have no access to its ranking data.
Judge a link from several facts together (source page, placement, anchor, history), never from one metric.

## Decide what to do with a flagged link

A flagged link gets one of four actions: remove it, mark it `sponsored`, disavow it or leave it. Who placed the link
and whether anyone can still change it decide which one.

| Action | Wins when | Why the others lose here |
|---|---|---|
| Remove | you or an agency placed it for rankings, it brings no real readers, and someone can still edit the page | `sponsored` keeps a link nobody needs; disavow leaves it live and is not needed while removal works; leaving it keeps the breach |
| Add `rel="sponsored"` | the link was paid for, still brings readers or reach, and the site will edit it | removal gives up traffic you paid for; disavow adds nothing once the attribute declares the payment; leaving it unmarked stays link spam |
| Disavow | a large set of artificial links has brought a manual action or looks set to, and requests to remove or mark them failed | removal and `sponsored` were tried and the sites did not act; leaving them keeps the manual action or the risk of one |
| Leave | random spam nobody on your side placed, with no manual action | removal requests spend hours on links Google says it ignores; `sponsored` is not yours to add; disavowing them is unnecessary and an overbroad file can cost good links |

## When to use the disavow tool

The disavow tool asks Google to ignore specific links. Google recommends it only when many low-quality, artificial
or spam links point to your site, and those links have caused or are likely to cause a
manual action. Typical cases: a manual action for unnatural links, or a known history of paid link building you
cannot get removed. Do not disavow random spam links, and never disavow good links in bulk.

```text
# disavow.txt (UTF-8, one entry per line)
# paid links from the 2023 campaign, removal requested 2026-09-10, no response
domain:spammy-links.example
https://blog.example.net/sponsored-post-123
```

Upload at Search Console's disavow links tool, per property. Bing has a similar tool in Bing Webmaster Tools.

## Manual action for unnatural links

A manual action for unnatural links appears in Search Console › Security and manual actions. To recover:

1. Read which type it is: links to your site, or links from your site (selling links).
2. Collect all links (Search Console, Bing, third-party index), identify the unnatural ones.
3. Remove what you can; add `sponsored` or `nofollow` where you control the link; disavow the rest.
4. Send Google a reconsideration request: the cause, the links you took down (with examples), and the process change
   that keeps it from recurring.

## Worked example: a backlink audit after an agency change

Situation: a new client's previous agency "built 400 links"; there is no manual action.

Export from Search Console and Bing, grouped by domain: 1,900 referring domains; 310 are guest-post sites selling to
anyone, with exact-match anchors to service pages, dated 2024 to 2025. Decision: no manual action, so no disavow;
ask the sites that still exist to add `rel="sponsored"` where the client paid (invoices exist for 120); stop the
programme. Plan instead: a yearly pricing survey with the data published, and a reclaim of 46 broken pages with
backlinks by 301s. Review: quarterly; disavow only if a manual action arrives.

## Verify links, redirects and the disavow file

Link work is checked at the source, because a report only shows what someone claims. Read the attribute on a paid
link, follow a reclaimed URL, and lint a disavow file before uploading it:

```bash
curl -sL https://partner.example/sponsored-review | grep -ioE '<a [^>]*href="https://www\.example\.com[^>]*>'   # expect rel="sponsored"
curl -sIL https://www.example.com/old-guide | grep -iE '^(HTTP/|location:)'                                      # expect one 301, then 200
grep -nvE '^(#.*|domain:[a-z0-9.-]+|https?://[^ ]+)$' disavow.txt                                                # expect no output
```

Then read Search Console › Links again after recrawl: the reclaimed pages show under Top linked pages at their new
URL, and a spike has a named cause. After a manual action, Manual actions shows no entry once the review passes.
Earned links are counted by the referring pages you can name, not by a tool's score.

## Checklist for link building

The link building checklist keeps link work effective and within the rules.

1. Paid, affiliate and exchanged links carry `rel="sponsored"`.
2. Pages that lost backlinks to 404 are redirected to the best current page.
3. Link-earning assets planned around original data, tools or expertise.
4. Backlink profile reviewed quarterly; spikes explained.
5. Disavow used only for a manual action or known paid links that cannot be removed.

## Gotchas in link building

The gotchas below waste budget or create risk.

1. **Buying "guest posts" with dofollow anchors.** Symptom: a backlink export shows guest-post sites selling to
   anyone. Cause: such posts are link spam by definition, and often come from sites that sell to anyone. Fix: stop
   buying them, and ask for `rel="sponsored"` on what you paid for.
2. **Disavowing based on a tool's toxic score.** Symptom: good links lose value and nothing improves. Cause: toxic
   scores are vendor estimates, and disavowing can remove the value of good links; it is usually unnecessary. Fix:
   disavow only as the section above says.
3. **Exact-match anchors everywhere.** Symptom: an anchor report shows one commercial phrase on most links. Cause:
   natural anchors are mostly brand names, URLs and plain phrases. Fix: stop asking for specific anchors.
4. **Counting links instead of judging them.** Symptom: the count rises, rankings do not. Cause: one link from a
   respected site in your field beats hundreds of directory links. Fix: report the links worth having by name.
5. **Redirecting an expired domain.** Symptom: a bought domain with an old backlink profile points at the site and
   rankings do not improve, or a penalty follows. Cause: it borrows links, which is expired domain abuse. Fix: remove
   the redirect and earn links on your own domain.

## Anti-patterns in link building

Anti-patterns in link work buy a number that search engines were built to ignore.

| Do not | Do this instead |
|---|---|
| Paying for links without an attribute | use `rel="sponsored"` or `nofollow`, and label sponsored content for readers |
| Mass emailing "link exchange" offers | earn links with data, tools and useful resources |
| Hiding links in widgets or templates across other sites | use plain, earned links |
| Starting outreach before reclaiming lost links | reclaim your own 404 pages with backlinks first; it is the cheapest win |
| Disavowing random spam links | leave them; Google says it ignores most of them |

## See also for link building

- `algorithm-updates-and-penalties`: manual actions and reconsideration requests
- `yandex-seo`: the Minusinsk filter on bought links
- `site-migrations`: keeping link value through a move
- `search-console`: reading the Links report
- `seo-measurement`: traffic results
- `content-briefs`: content others want to cite
