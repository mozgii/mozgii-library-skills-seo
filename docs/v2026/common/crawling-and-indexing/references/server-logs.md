---
title: Server log analysis for crawling
author: MOZGII, Inc.
lang: en
description: How to read web server access logs to see what Googlebot, Bingbot and AI crawlers actually fetch, how to verify that a bot is genuine, and the log checks behind crawl budget and indexing decisions.
---

# Server log analysis for crawling

Server access logs are the only record of what crawlers really requested, when, and what the server answered. Search
Console's Crawl stats report is a sample from Google's side; logs cover every bot. Use them when a site is large,
when pages are slow to be indexed, after a migration, or to see what AI crawlers take.

## Contents

1. What to collect
2. Verify that a bot is genuine
3. Log checks with standard tools
4. What the numbers mean

## What to collect from server logs

A useful log export covers at least 30 days and every host and server (CDN logs too, since a CDN may answer without
reaching the origin). Each line needs: time, client IP, method, URL with query string, status, bytes, response time
and user agent. Combined log format has all but response time; add it (`$request_time` in nginx, `%D` in Apache).
Logs contain IP addresses, which are personal data in many countries: keep only what the analysis needs and delete it
after.

## Verify that a bot is genuine

Anyone can send a Googlebot user agent, so verify the IP before trusting a "Googlebot" line. Two ways:

**Published IP ranges** (fast, scriptable): Google publishes JSON files of its crawler ranges under
`https://developers.google.com/static/crawling/ipranges/`: `common-crawlers.json` (Googlebot and the other common
crawlers), `special-crawlers.json` (AdsBot and similar), `user-triggered-fetchers-google.json`,
`user-triggered-fetchers.json` and `user-triggered-agents.json`. Bing publishes `https://www.bing.com/toolbox/bingbot.json`;
OpenAI publishes `https://openai.com/searchbot.json`, `https://openai.com/gptbot.json`,
`https://openai.com/chatgpt-user.json` and `https://openai.com/adsbot.json`.

**Reverse then forward DNS** (works for engines without a list):

```bash
host 66.249.66.1                          # → crawl-66-249-66-1.googlebot.com
host crawl-66-249-66-1.googlebot.com      # → 66.249.66.1: genuine
```

| Bot | Reverse DNS must end in |
|---|---|
| Googlebot and common Google crawlers | `googlebot.com` (or `geo.googlebot.com`) |
| Google special crawlers and user-triggered fetchers | `google.com`, or `gae.googleusercontent.com` for fetchers run on Google Cloud |
| Bingbot | `search.msn.com` |
| YandexBot | `yandex.ru`, `yandex.net` or `yandex.com` |

Some AI companies publish no IP ranges (Anthropic says it uses service providers' public IPs); for those, rely on the
user agent and robots.txt, and block by IP only what you have verified.

## Log checks with standard tools

The commands below run on a combined-format log (`access.log`) and need no extra software. Filter to verified bot IPs
first when the stakes are high.

Requests per Googlebot status code:

```bash
grep 'Googlebot' access.log | awk '{print $9}' | sort | uniq -c | sort -rn
```

Where Googlebot's crawl goes, by first path segment:

```bash
grep 'Googlebot' access.log | awk '{split($7,p,"/"); print "/"p[2]}' | sort | uniq -c | sort -rn | head -20
```

Parameter URLs Googlebot fetches (crawl waste candidates):

```bash
grep 'Googlebot' access.log | awk '$7 ~ /\?/ {split($7,q,"?"); print q[1]"?"substr(q[2],1,20)}' | sort | uniq -c | sort -rn | head -20
```

Money pages and when Googlebot last fetched each (`money.txt` holds one path per line):

```bash
grep 'Googlebot' access.log | grep -Ff money.txt | awk '{last[$7]=$4} END {for (u in last) print u, last[u]}'   # logs are in time order
```

AI crawler requests by bot:

```bash
grep -Eo 'GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|Claude-SearchBot|Claude-User|PerplexityBot|Perplexity-User|Google-Agent|bingbot' access.log | sort | uniq -c | sort -rn
```

## What the log numbers mean

The log numbers turn into decisions this way.

| Finding | Meaning | Action |
|---|---|---|
| a large share of crawl on parameters, filters, calendars or tag pages | crawl spent on URLs that should not rank | stop linking them; canonical or robots.txt rules (`canonical-urls`) |
| money pages fetched less than once a month | weak internal links or low priority | link them from hubs and the home page; keep them in the sitemap |
| many 3xx to Googlebot | internal links point to redirects | link final URLs |
| 5xx or 429 to Googlebot | the server sheds crawler load | capacity, rate limits, WAF rules; Google slows down on these |
| 404s on URLs with links or traffic | lost pages | 301 to the best match |
| URLs in logs but not in your crawl | orphan or legacy URLs still known to Google | link, redirect or let them 404 |
| slow average response time to bots | crawl capacity limited by speed | caching, faster backend |
