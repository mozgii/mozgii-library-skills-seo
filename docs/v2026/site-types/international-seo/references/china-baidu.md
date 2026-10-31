---
title: China and Baidu reference
author: MOZGII, Inc.
lang: en
tags: [china, baidu, icp, hosting, simplified-chinese]
description: A short reference on search in mainland China - Baidu's official tools and how old they are, licensing, hosting, Simplified Chinese, and where the sources conflict.
---

# China and Baidu reference

Search in mainland China runs on Baidu and a few local engines, under rules that differ from every other market in this
library. This page says what the official sources support and marks the rest, checked on 31 October 2026.

Official Baidu documentation is thin and old. The main handbook was last updated in 2020 and the SEO guide in 2014. The
newer material is a stream of short notices. Agency sources conflict on ICP and hosting. Treat anything below marked as
third-party as a question for a PRC lawyer, not as advice.

## Baidu's share in China

Baidu leads China by StatCounter's third-party estimate, though less clearly than older guides say. For September 2026:
Baidu 46.85%, Bing 21.61%, Yandex 15.01%, Haosou 12.22%, Sogou 2.57%, Google 1.45%. The Yandex figure looks odd for this
market and may reflect the tracker's sample, so check your own referrals before planning around any of these.

## Baidu's official sources and their age

Baidu's site owner hub is the Search Resource Platform (搜索资源平台, `ziyuan.baidu.com`). A site needs an account and a
verified site, and most tools sit behind login.

| Source | Date | Use it for |
|---|---|---|
| 平台工具使用手册, the tool handbook | last chapter 2020-08-14 | verification, submission, dead links, site moves, robots |
| 百度搜索算法规范详解, algorithm rules | 2020-06-18 | content, user need, experience and fairness rules |
| 百度移动搜索建站优化白皮书 | 2017-11-22 | mobile site building |
| 百度搜索引擎优化指南 2.0 | 2014-12-12 | history only |
| 百度搜索违规低质页面问题说明, low-quality pages | 2023-08-29 | a current checklist: thin content, mismatched titles, intrusive ads, slow pages |
| Notices at `ziyuan.baidu.com/wiki/7` | up to October 2026 | what changed recently |

Notices we read: 22 September 2023, sitemap submission closed and API quotas cut for accounts without real-name
verification and for low-quality sites; 18 November 2025, the mobile site logo moved to 200×150 px (4:3); 6 March 2026,
sites should recognise HarmonyOS phones as mobile; 23 June 2026, hijacked third-party scripts; 15 September 2026, Search
Mini Tools (搜索小工具) in limited testing; 28 October 2026, Index Volume data for 14 to 23 October is unreliable.

The console also lists 权威溯源 (authoritative sources) and AI流量分析 (AI traffic analysis). Reports in the trade press
say the second appeared around 15 September 2026, with citations, impressions, clicks and CTR, and dashboards still empty
at launch; we could not open Baidu's own notice.

## Baidu's submission tools

The handbook documents these mechanics, in its 2020 state. Baidu can change quotas per site at any time.

| Tool | Facts |
|---|---|
| API push (普通收录) | `POST http://data.zz.baidu.com/urls?site=SITE&token=TOKEN`, `Content-Type: text/plain`, one URL per line, up to 2,000 per request; answers `success`, `remain`, `not_same_site`, `not_valid`; errors include 400 `over quota` and 401 `token is not valid` |
| Sitemap | text or XML; 50,000 URLs and 10 MB per file; index files are no longer accepted; text may be UTF-8 or GBK |
| Dead links (死链提交) | a text or XML file of dead URLs, in the sitemap format; no index files; takes effect about a week after it is crawled; prefer real 404s over soft ones |
| Site closure protection (闭站保护) | for a site closing temporarily, up to 180 days; keeps index volume, not rankings |
| Site move (网站改版) | a 2020 Baidu Q&A says authority takes half a year or more to reach a new domain |

Resubmitting old URLs wastes quota, and Baidu says it may cut a site's quota for doing so.

## ICP licensing and hosting

ICP (Internet Content Provider) registration is the legal question that comes before SEO. Baidu's pages that we read say
nothing about ICP or hosting. Its own footer shows a licence number, which is all the first-party evidence here.

What vendors and consultancies say, all third-party: a filing (ICP 备案) is the basic registration, and a commercial
licence (ICP 经营许可证) covers paid or transactional services; both tie to hosting in mainland China; and both need a
legal entity there, which a foreign company often lacks. They conflict on the points that matter most:

| Question | Where sources disagree |
|---|---|
| Who needs the commercial licence | every transactional site, or only a business selling directly through the site |
| Whether Hong Kong hosting avoids it | one says it avoids the process, others say Baidu and speed suffer |
| Whether offshore hosting hurts Baidu rankings | vendor blogs claim so, and we found no Baidu statement |
| What a foreign company can do alone | a local partner, a joint venture or a subsidiary, depending on the source |

Check the MIIT filing system (`beian.miit.gov.cn`), your hosting provider's filing guide (Alibaba Cloud publishes one) and
a PRC lawyer before deciding. Do not promise a client a ranking effect from hosting.

## Simplified Chinese and localisation

Mainland readers use Simplified Chinese, so write `zh-Hans` or `zh-CN` content rather than converting from Traditional
without review. Keep the `hreflang` rules in `international-seo`: `zh-Hans` and `zh-Hant` are valid, and `cn` is not a
language code. Google's hreflang rules do not bind Baidu, and none of the official Baidu pages we read mention `hreflang`.

## What the official record lacks

Baidu's tools are documented well enough for procedure, and its notices are current. What is missing is any official
word on hosting, ICP or ranking, and the handbook's limits are six years old. Test API quotas and sitemap acceptance on a
real verified site before planning around them.

Sources: [Search Resource Platform](https://ziyuan.baidu.com/), [tool handbook](https://ziyuan.baidu.com/college/courseinfo?id=267),
[algorithm rules](https://ziyuan.baidu.com/college/documentinfo?id=2988), [low-quality pages](https://ziyuan.baidu.com/college/articleinfo?id=3528),
[quota notice](https://ziyuan.baidu.com/wiki/3531), [StatCounter China](https://gs.statcounter.com/search-engine-market-share/all/china),
[Search Engine Journal on AI Traffic Analysis](https://www.searchenginejournal.com/baidu-now-measures-ai-citations-heres-what-seos-should-and-shouldnt-read-into-it/),
[Alibaba Cloud ICP filing](https://help.aliyun.com/en/dws/icp-filing).
