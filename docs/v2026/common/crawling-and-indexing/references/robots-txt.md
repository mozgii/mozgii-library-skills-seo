---
title: robots.txt syntax and examples
author: MOZGII, Inc.
lang: en
description: How robots.txt is parsed by Google, Bing and Yandex, with wildcards, precedence rules, tested examples and the differences between engines.
---

# robots.txt syntax and examples

robots.txt is a plain text file at the root of each host (`https://www.example.com/robots.txt`) that tells crawlers
which paths they may fetch. It is defined by RFC 9309 (Robots Exclusion Protocol, 2022). It is a request, not access
control: anything private needs authentication.

## Contents

1. Where robots.txt applies
2. Groups and user agents
3. Matching and precedence
4. Wildcards
5. Examples
6. Differences between engines
7. AI crawlers in robots.txt
8. Testing robots.txt

## Where robots.txt applies

robots.txt applies to one protocol, host and port. `https://example.com/robots.txt` does not cover
`https://www.example.com/` or `https://shop.example.com/`; each host needs its own file. It must be UTF-8 text.
Google reads the first 500 KiB and ignores the rest; Yandex treats a file over 500 KB as allowing everything.

## Groups and user agents in robots.txt

A robots.txt group starts with one or more `User-agent` lines and holds the rules for those crawlers. Each
crawler follows one group, the most specific match for its name, and ignores `*` when a group names it directly. Rules are not
merged across groups, so a `Googlebot` group must repeat every rule from `*` that should apply to Google.

```text
User-agent: *
Disallow: /private/

User-agent: Googlebot
Disallow: /private/
Disallow: /experiments/
```

## Matching and precedence in robots.txt

robots.txt rules match the URL path from its start, and are case-sensitive. When several rules match, Google and
Bing use the most specific one (the longest path); on a tie `Allow` wins. An empty `Disallow:` allows everything.

| Rule | Matches | Does not match |
|---|---|---|
| `Disallow: /shop` | `/shop`, `/shop/`, `/shopping`, `/shop?x=1` | `/Shop` |
| `Disallow: /shop/` | `/shop/`, `/shop/item` | `/shop` |
| `Allow: /shop/sale/` with `Disallow: /shop/` | `/shop/sale/x` is allowed | — |

## Wildcards in robots.txt

robots.txt supports two wildcards in Google, Bing and Yandex: `*` for any sequence of characters and `$` for the
end of the URL.

```text
Disallow: /*?sort=          # any URL with a sort parameter as the first parameter
Disallow: /*&sort=          # sort parameter later in the query string
Disallow: /*.pdf$           # URLs ending in .pdf
Allow: /*.css$
Allow: /*.js$
```

## Examples of robots.txt files

The robots.txt examples below cover the common cases.

Allow everything and list the sitemap:

```text
User-agent: *
Disallow:

Sitemap: https://www.example.com/sitemap.xml
```

Block a whole staging host (and also protect it with a password; robots.txt alone leaks URLs):

```text
User-agent: *
Disallow: /
```

E-commerce site with internal search and filters:

```text
User-agent: *
Disallow: /search
Disallow: /cart
Disallow: /checkout
Disallow: /account
Disallow: /*?*color=
Disallow: /*?*size=
Allow: /*?page=

Sitemap: https://www.example.com/sitemap-index.xml
```

## Differences between engines in robots.txt

Search engines agree on the core rules and differ on extensions.

| Directive | Google | Bing | Yandex |
|---|---|---|---|
| `Allow`, `Disallow`, `*`, `$` | yes | yes | yes |
| `Sitemap:` | yes | yes | yes |
| `Crawl-delay` | ignored | honoured | ignored since 2018; set crawl rate in Yandex Webmaster |
| `Clean-param` | no | no | yes: tells Yandex to ignore listed parameters |
| `Host` | no | no | retired in 2018; use a 301 to the main host |
| `Noindex:` in robots.txt | not supported since 2019 | no | no |

## AI crawlers in robots.txt

To stop OpenAI and Anthropic training on your content while you still appear in ChatGPT search and Claude's
answers, disallow `GPTBot` and `ClaudeBot` and allow `OAI-SearchBot` and `Claude-SearchBot`. AI crawlers each have their own user agent token, so a site can allow search and AI answers while refusing model
training. Tokens and their purposes as documented by each company (checked October 2026):

| Token | Company | Purpose |
|---|---|---|
| `Googlebot` | Google | Search, including AI Overviews and AI Mode; never block it to avoid AI features |
| `Google-Extended` | Google | not a crawler: controls training for Gemini Apps and the Vertex AI API for Gemini, and grounding in Gemini Apps and Grounding with Google Search on Vertex AI; does not affect Search |
| `GPTBot` | OpenAI | training of foundation models |
| `OAI-SearchBot` | OpenAI | ChatGPT search results |
| `ChatGPT-User` | OpenAI | fetches made when a user asks; robots.txt may not apply |
| `OAI-AdsBot` | OpenAI | checks landing pages of ads shown in ChatGPT; not used for training |
| `ClaudeBot` | Anthropic | training |
| `Claude-SearchBot` | Anthropic | Claude's search index |
| `Claude-User` | Anthropic | fetches made when a user asks |
| `PerplexityBot` | Perplexity | Perplexity's search index |
| `Perplexity-User` | Perplexity | fetches made when a user asks; robots.txt may not apply |
| `Google-Agent` | Google | agents on Google's infrastructure that browse a site for a user; a user-triggered agent, not a crawler |
| `Applebot-Extended` | Apple | controls use for Apple's model training; Applebot still crawls for search |
| `bingbot` | Microsoft | Bing search and Copilot answers |
| `__usage_ai-training` | shared, from IETF AIPREF work | not a crawler: one training preference for every participating company. Microsoft reads it from 1 February 2027; Google plans support in early 2027 |

Allow search and answers, refuse training:

```text
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: __usage_ai-training
Disallow: /

User-agent: *
Disallow: /cart/
```

The `__usage_ai-training` group is a policy token, so no crawler identifies itself by that name. Google plans to read
its Disallow as `Google-Extended` disallowed, unless the file names `Google-Extended`. A site that wants to stay eligible
for grounding in Gemini Apps must allow that token explicitly, and the allow also permits Gemini training, because
`Google-Extended` controls both:

```text
User-agent: __usage_ai-training
Disallow: /

User-agent: Google-Extended
Allow: /
```

## Testing robots.txt

robots.txt changes are tested before they ship, because one wrong line can hide a site.

- Search Console › Settings › robots.txt: the version Google fetched, when, and parse errors; request a recrawl
  after a fix.
- Bing Webmaster Tools › robots.txt Tester.
- Locally, with Google's open-source parser (github.com/google/robotstxt, Apache-2.0):
  `robots_main robots.txt Googlebot https://www.example.com/shop/item`.
- Python's `urllib.robotparser` gives a quick answer but does not implement longest-match precedence; do not trust it
  for `Allow` overrides.
