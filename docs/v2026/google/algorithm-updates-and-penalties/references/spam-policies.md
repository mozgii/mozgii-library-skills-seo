---
title: Google spam policies and how to check a site
author: MOZGII, Inc.
lang: en
description: Every Google web search spam policy as of October 2026, what it looks like on a real site, how to check for it, how to fix it, and the common patterns of hacked sites.
---

# Google spam policies and how to check a site

Google's spam policies name the practices that its automated spam systems demote and its reviewers act on with
manual actions. This file restates each one in plain terms (Google's page was updated 28 August 2026), with the check
an auditor runs and the fix. The policy text itself is at https://developers.google.com/search/docs/essentials/spam-policies.

## Contents

1. Content policies
2. Link and reputation policies
3. Deception and technical policies
4. Other reasons for demotion or removal
5. Common hacked-site patterns

## Content spam policies

The content policies cover pages made to rank rather than to help a reader.

| Policy | Looks like | Check | Fix |
|---|---|---|---|
| Scaled content abuse | hundreds of pages from a template or a model with no unique data; "[service] in [city]" for every town | crawl: group by template; sample 20 pages and ask what each adds | remove, merge or `noindex` the set; keep pages with unique data (`programmatic-seo`) |
| Doorway abuse | many near-identical pages for close queries, each funnelling to one page | crawl: near-duplicate clusters with one main outlink | merge into one useful page; 301 the rest |
| Thin affiliation | product pages with the merchant's text and images and an affiliate link | compare text with the merchant feed | add original testing, comparison, photos; or `noindex` |
| Scraping | copied or lightly rewritten articles from other sites | search distinctive sentences in quotes | remove; write original content |
| Keyword stuffing | phrase lists, repeated city names, blocks of keywords in footers | read the page aloud; count repeats | rewrite for readers |
| Hidden text and links | text the same colour as the background, off-screen CSS, 1-pixel links | compare rendered page with HTML text | remove; legitimate collapsed content (tabs, accordions) is fine |
| User-generated spam | spam comments, forum posts, profiles, uploaded files | `site:example.com` plus spam words (casino, viagra, loan) | moderation, `rel="ugc"`, captchas, `noindex` new profiles until trusted, `noindex` by default on pages made for direct sharing (Google's October 2026 guidance); alert on sudden surges of public pages |

## Link and reputation spam policies

The link and reputation policies cover borrowed or bought ranking strength.

| Policy | Looks like | Check | Fix |
|---|---|---|---|
| Link spam | paid links without `rel="sponsored"`, link exchanges, PBNs, keyword anchors in widgets | backlink export; outbound links in posts | `sponsored` or `nofollow` on paid links; remove schemes (`link-building`) |
| Site reputation policy (often called site reputation abuse) | a third party's coupon, casino or loan section on a strong host, little control by the host | sections whose author, design and topic differ from the site; same text on other hosts | remove the section or `noindex` it; real first-party editorial control |
| Expired domain abuse | a lapsed domain bought and filled with unrelated low-value content | Wayback Machine history against current topic | do not do it; a redirect of an unrelated old domain passes nothing useful |

The site reputation policy has a regional difference since 30 August 2026: the impact of its manual actions no longer
applies to results shown in the European Economic Area, where such a section may instead be separated in Google's
systems and, over time, rank apart from the host site. Outside the EEA the manual action still affects the section
concerned, and the rest of the site stays untouched. Site owners still get the manual action notice in Search Console
wherever their readers are, and can file a reconsideration request; eligible sites can then take a dispute to
mediation. A page with such an action can therefore lose ground for users outside the EEA and none inside it
([Google's post of 28 August 2026](https://developers.google.com/search/blog/2026/08/update-site-reputation-policy)).
Wire services, syndicated news, user-generated sections, clearly labelled native advertising, normal affiliate links
and ad units do not break this policy.

## Deception and technical spam policies

The deception policies cover what users or crawlers are shown, and where they are sent.

| Policy | Looks like | Check | Fix |
|---|---|---|---|
| Cloaking | Googlebot gets a keyword page, users get something else | fetch with a Googlebot user agent and a browser user agent from the same IP; compare | serve the same content; paywalls use paywall markup |
| Sneaky redirects | mobile users or search visitors sent to another site | open results on a phone; check third-party scripts and ad tags | remove the redirect or the script |
| Back button hijacking | the back button reloads the page, opens an ad page or a "you may also like" page instead of the results | from a Google result, click in, press Back: you must land on the results | remove history manipulation (`history.pushState` loops, injected entries); audit ad and recommendation scripts |
| Malicious practices | malware, unwanted downloads, deceptive installs | Security issues report; Safe Browsing site status | remove; request review |
| Misleading functionality | a "free tool" that only shows ads or sends users elsewhere | use the tool | deliver the promised function or remove the page |
| Machine-generated traffic | automated queries to Google, rank-checking by scraping | your own tools and scripts | use Search Console and licensed data |

Back button hijacking was added under malicious practices in April 2026; enforcement began 15 June 2026, and Google
sends Search Console warnings before or with the action.

## Other reasons for demotion or removal

Google can also demote or remove sites for reasons outside the spam list:

- **Legal removals**: many valid copyright or defamation removals against one site can demote the rest of it.
- **Personal information removals**: sites with exploitative removal practices (pay to remove).
- **Policy circumvention**: moving violating content to a new subdomain, folder or domain extends the action.
- **Scam and fraud**: impersonating businesses or official support, fake contact details.

## Common hacked-site patterns

Hacked sites show recognisable patterns, and knowing them makes the cleanup faster.

| Pattern | Signs | Where to look |
|---|---|---|
| Japanese or Chinese keyword hack | thousands of new URLs with Japanese or Chinese titles in `site:` results; often a hijacked Search Console owner added | Search Console users list; new folders; database posts |
| Cloaked keyword pages | spam pages shown only to Googlebot or only to visitors from Google | server config (`.htaccess`, nginx includes), PHP files that read the user agent or referrer |
| Injected links | hidden links in footers or posts, visible only in source | theme files, database content, widgets |
| Malicious redirects | visitors from search or from mobile sent to scam sites | `.htaccess`, JavaScript injected in templates or tag managers |
| Malware downloads | Safe Browsing warning in Chrome | uploads folder, modified JavaScript bundles |

After cleanup, check the Search Console users and owners list and remove anyone unknown: a hacker who verified
themselves can submit their own sitemaps.
