# SEO skills library

A library of Claude skills for search engine optimisation. It covers the whole job: technical SEO (crawling,
indexing, JavaScript rendering, canonicals, sitemaps, migrations, Core Web Vitals), page and content work (on-page,
search appearance, briefs, keyword research, structured data, programmatic pages, images and video), markets
(international, local, e-commerce, publishers and Discover), search engines beyond Google (Bing and Copilot, Yandex with
Wordstat and Russian-language text, Naver and Search Advisor), off-site work (links), recovery from updates and penalties, measurement, and visibility in
AI search. Each skill is a standard `SKILL.md`
with references and, where a check is mechanical, a script that needs only Python 3 or Node.

Every skill stands alone: copy one folder and it works without the others. Skills mention each other only as "see
also". Guidance was checked against the search engines' own documentation in October 2026 (for example: Googlebot
reads the first 2 MB of an HTML file; back button hijacking became a spam policy in 2026; site reputation manual
actions no longer apply in the EEA since 30 August 2026; Google retired FAQ rich results in 2026; a Search Console
setting takes a site out of Google's AI features without touching its normal results).

## Use these skills

Skills live in `docs/v2026/<group>/<skill>/`, each with `SKILL.md` at its root and portable front matter (`name`,
`description`, `metadata`). Skill names are unique across groups, so groups can share one skills folder. Take what the
site needs: `common` and `site-types` for most work, plus the group of each engine you target.

| Group | Skills | Use it for |
|---|---|---|
| `common` | 16 | SEO work that stays the same whichever engine you target |
| `site-types` | 4 | international, local, e-commerce and programmatic sites |
| `google` | 6 | Search Console, rich results, AI features, search appearance, news, updates and penalties |
| `bing` | 3 | Bing, Bing Webmaster Tools, Copilot and the AI preferences |
| `yandex` | 3 | Yandex, Wordstat and Russian-language text |
| `naver` | 2 | Naver, Search Advisor and Yeti |

- **Claude Code, for all your projects**: copy one skill with `cp -r docs/v2026/common/seo-audit ~/.claude/skills/`, or a
  whole group with `cp -r docs/v2026/google/* ~/.claude/skills/`. The group's `README.md` comes along and does no harm.
- **Claude Code, for one project**: copy it to the project's `.claude/skills/`.
- **claude.ai and Claude Desktop**: zip the folder so the zip holds the one folder (`seo-audit/SKILL.md` inside),
  then upload it in claude.ai's skills settings (Customize › Skills) and turn it on.

Claude loads a skill when a request matches its description; you can also call one by name, such as `/seo-audit`.
Scripts run with `python3` (3.9 or later) or `node` (18 or later) and need no packages.

## Skills

### common

| Skill | What it does |
|---|---|
| `seo-audit` | Runs a full site audit in a fixed order and ranks findings by reach, severity and ease; `page_check.py`, `sitemap_check.py` |
| `crawling-and-indexing` | robots.txt, noindex, status codes, one URL's diagnosis, crawl budget, server logs and bot verification, removals |
| `javascript-seo` | SSR or static rendering, metadata in server HTML, SPA status codes, the 2 MB limit, framework recipes |
| `xml-sitemaps` | Sitemap format, limits, lastmod, image, video, news and hreflang sitemaps, IndexNow; `sitemap_check.py` |
| `canonical-urls` | Duplicate content, canonical rules, URL normalisation, parameters, pagination |
| `site-migrations` | Domain, HTTPS, URL and platform moves: inventory, redirect map, launch, monitoring; `redirect_check.py` |
| `internal-linking` | Site architecture, hubs, click depth, navigation, anchors, orphan pages, link audits |
| `core-web-vitals` | LCP, INP, CLS thresholds, field and lab data, PSI and CrUX APIs, web-vitals, agent-run traces, fixes with code |
| `structured-data` | JSON-LD rules for any engine, the format choice, templates, validation, Open Graph |
| `image-and-video-seo` | Indexable images, alt text, preferred image, licence metadata, video watch pages, key moments |
| `keyword-research` | Seeds, demand, intent, a reproducible score, clustering, one main phrase per page; `autocomplete.py` |
| `on-page-seo` | The on-page contract, phrase placement by tier, real versus fake fixes, images on the page |
| `content-briefs` | SERP analysis, content briefs, E-E-A-T, AI content policy, reviews and comparisons, refresh and pruning |
| `link-building` | Link policies and attributes, earning links, backlink audits, disavow, manual actions |
| `ai-search-visibility` | ChatGPT, Perplexity, Claude and every other assistant: crawlers, a written policy, AI agents, myths, assistant tests, measurement |
| `seo-measurement` | Data sources, KPIs, GA4 landing pages, control groups, traffic drops |

### site-types

| Skill | What it does |
|---|---|
| `international-seo` | URL structures, hreflang rules and codes, localisation, locale redirects, a China and Baidu reference, Seznam; `hreflang_check.py` |
| `local-seo` | Google Business Profile, reviews, NAP and citations, location pages, other map platforms |
| `ecommerce-seo` | Categories, faceted navigation, products, variants, stock changes, shipping and returns, Merchant Center |
| `programmatic-seo` | Pages generated from data at scale without scaled content abuse: page sets, quality gates, batch launch |

### google

| Skill | What it does |
|---|---|
| `search-console` | Properties, Page indexing reasons, the Indexing API, metrics, exports, new reports, reconciling totals; `gsc_export.py` |
| `google-rich-results` | The features Google supports, the 2026 properties, retired features, enhancement reports |
| `google-ai-features` | AI Overviews and AI Mode: Google's guidance, the Search Console opt-out, snippet controls, `Google-Extended`, the generative AI report |
| `search-appearance` | Title links Google rewrites, snippets, site names, favicons, dates, sitelinks, snippet controls |
| `news-and-discover-seo` | Google News, Top Stories, preferred sources, Discover images and titles, the 2026 Discover update |
| `algorithm-updates-and-penalties` | Core and spam updates, spam policies, manual actions, reconsideration, hacked-site cleanup |

### bing

| Skill | What it does |
|---|---|
| `bing-seo` | Where Bing's share justifies the work, what differs from Google, the 2026 guidelines, IndexNow, bingbot; `bing_check.py` |
| `bing-webmaster-tools` | Setup, verification, every report, quotas, the REST API, keys and OAuth; `bing_api.py` |
| `bing-ai-and-copilot` | AI Performance, AI Training and AI Grounding preferences, the `noarchive` and `nocache` deadlines |

### yandex

| Skill | What it does |
|---|---|
| `yandex-seo` | Yandex Webmaster, regions, commercial and behavioural factors, filters, Alice AI |
| `yandex-wordstat` | Exact frequency, operators, the Wordstat and Search APIs, prices and quotas; `demand.mjs` |
| `russian-language-seo` | Russian SEO text for Yandex and Google: morphology, zones, lemma counts, typography, natural Russian, translation; `text-check.mjs` |

### naver

| Skill | What it does |
|---|---|
| `naver-seo` | Where content lives, titles, descriptions, favicons, sublinks, structured data, C-Rank, Blog, AI Briefing |
| `naver-search-advisor` | Ownership, Yeti, robots rules, sitemaps and RSS, indexing fixes, IndexNow, the crawl API, moves; `naver_check.py` |

## Layout

- `docs/v2026/<group>/<skill>/SKILL.md`: the skill; `references/*.md` for detail opened only when needed; `scripts/` for
  checks.
- `docs/v2026/<group>/README.md`: what the group holds and when to use it.
- `library.json`: name `seo`, title, version, the self-test minimum.
- `questions.json`: the self-test; each question names a phrase its answering passage holds.
- `versions.json`: every package and tool the library names, with the version and the date it was checked.
- `sources.json`, `NOTICE`: the vendor skills and community collections read as context, each at a commit, with its
  licence.

The built pack lands in `dist/` (not in git).

## What changed from the source skills

Three skills came from an earlier private collection and were rewritten for general use: keyword research (now
Google, Bing and Yandex, not Yandex only), on-page SEO (no longer tied to Russian-language sites), and Russian SEO
text (kept as a general Russian-language skill). Project-specific examples were replaced with neutral ones. Dropped:
a drift-check script that compared the Russian skill with two base skills not shipped here, and references to skills
that did not exist in the source. The Wordstat demand script moved to `yandex-seo`.

Version 1.1 added six skills (JavaScript SEO, search appearance, images and video, news and Discover, programmatic
SEO, algorithm updates and penalties), moved the JavaScript and image material out of two larger skills into their
own, removed every dependency of one skill on another skill's scripts, and added a worked example to every skill.

The October 2026 pass compared the library with every official vendor skill we could find, then with Google's
documentation and the current framework majors. It corrected the Google AI opt-out, favicon rules, FAQ and practice
problem dates, and the React Router 8 and Nuxt 4 recipes. It added the Indexing API limits, Search profile, preferred
sources in AI answers, 2026 markup properties, DevTools MCP traces, `web-vitals` 6 soft navigations, evidence labels for
audit findings, an assistant test, GA4 landing page reports and approved catalogue batches.

The late October 2026 pass added one skill per engine that earns it: `bing-seo` and `naver-seo`, beside `yandex-seo`. It
added a China reference to `international-seo`, and fixed crashes in `sitemap_check.py` and `gsc_export.py`.

The 31 October 2026 audit pass covered the shared `__usage_ai-training` token at Google, the Wordstat methods in the
Yandex Search API, and the `kr` and `se` language codes. It gave every skill its missing Step 0, decision table, worked
example or Verify section, and fixed false passes and crashes in six scripts. Packs stay: a skill that runs a script now
tells the reader to read that script from the library and save it first when the file is not on disk.

The grouping pass, also on 31 October 2026, took the library from 27 to 34 skills and put each one in a group under
`docs/v2026/`. The test: change the engine and ask whether the advice changes. If it stays, the skill stays in `common`;
each engine's group owns its console, crawler, policies and AI controls. New skills: `search-console`,
`google-rich-results`, `google-ai-features`, `bing-webmaster-tools`, `bing-ai-and-copilot`, `yandex-wordstat` and
`naver-search-advisor`. `sitemap_check.py` no longer loses a repeated `X-Robots-Tag` header.

## Sources

Every text here is written in our own words. Official documentation was read and is linked, not copied. Third-party
skill collections were reviewed for coverage only; no text was taken from them.

| Source | Licence | Used for |
|---|---|---|
| [Google Search Central documentation](https://developers.google.com/search/docs) | CC BY 4.0 text, Apache 2.0 code samples | crawling, indexing, robots, sitemaps, canonicals, hreflang, site moves, faceted navigation, JavaScript SEO, title links, site names, favicons, images, video, Discover, structured data gallery (checked 2026-10) |
| [Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies), [core updates guide](https://developers.google.com/search/updates/core-updates) and [Search Status Dashboard](https://status.search.google.com/) | CC BY 4.0 (docs); dashboard linked | spam policies, update dates, recovery guidance |
| [Google Search Central blog](https://developers.google.com/search/blog), 2025–2026 posts | CC BY 4.0 | back button hijacking, site reputation policy update, Googlebot fetch limits, Discover core update, Search Console features |
| [Google's post on the shared training token](https://developers.google.com/search/blog/2026/10/ai-training-control) (Oct 2026) | CC BY 4.0 | `__usage_ai-training` at Google, and how it meets `Google-Extended` and Gemini Apps grounding |
| [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) and [Optimizing for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | CC BY 4.0 | AI search guidance and myths |
| [Google crawlers and fetchers](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers), [verifying Google requests](https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests) | CC BY 4.0 | crawler tokens, Google-Extended, Google-Agent, IP range files |
| [Search Console Help](https://support.google.com/webmasters/) (Manual actions, Video indexing report) | Google terms (linked, not copied) | manual action types, reconsideration, video report reasons |
| [Google preferred sources](https://developers.google.com/search/docs/appearance/preferred-sources) and [Google News Publisher Center help](https://support.google.com/news/publisher-center/) | CC BY 4.0 (docs); help linked | Top Stories and Google News |
| [web.dev Core Web Vitals](https://web.dev/articles/vitals) and [CrUX soft navigation metrics](https://web.dev/blog/crux-experimental-soft-navs/) | CC BY 4.0 | metrics, thresholds, tools, single-page apps |
| [schema.org](https://schema.org) | CC BY-SA 3.0 | type and property names |
| [sitemaps.org protocol](https://www.sitemaps.org/protocol.html) | CC BY-SA 2.5 | sitemap format |
| [RFC 9309 Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309) | IETF Trust | robots.txt rules |
| [IndexNow documentation](https://www.indexnow.org/documentation) | public protocol | request formats and response codes |
| [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmasters-guidelines-30fba23a), [Introducing AI Performance](https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/) (Feb 2026), [AI Performance help](https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c), [Your content, your choice](https://blogs.bing.com/search/2026/10/your-content-your-choice-clearer-preferences-for-training-and-grounding/) (Oct 2026), [FAQ: New AI Preferences](https://www.bing.com/webmasters/help/new-ai-pref-2t1cc16d), [URL Submission](https://www.bing.com/webmasters/help/url-submission-62f2860b), [SOAP and POX retirement](https://www.bing.com/webmasters/help/soap-pox-api-retirement-s0appox01) and the [Webmaster Tools help centre](https://www.bing.com/webmasters/help/help-center-661b2d18) | Microsoft terms (linked, not copied) | `bing-seo`, `bing-webmaster-tools`, `bing-ai-and-copilot`, Bing behaviour, AI Performance, AI Training and AI Grounding preferences |
| [Bing Webmaster API](https://learn.microsoft.com/en-us/bingwebmaster/) | Microsoft Learn terms (linked, not copied) | `bing-webmaster-tools`, `bing_api.py` |
| [DuckDuckGo result sources](https://duckduckgo.com/duckduckgo-help-pages/results/sources) | DuckDuckGo terms (linked, not copied) | where its links come from |
| [Naver Search Advisor guides](https://searchadvisor.naver.com/guide), all 54 pages in its [sitemap](https://searchadvisor.naver.com/sitemap.xml), and the [C-Rank post](https://m.blog.naver.com/naver_search/220774795442) | Naver terms (linked, not copied) | `naver-seo`, `naver-search-advisor`, read in Korean, written in English |
| [Wordstat in the Yandex Search API](https://aistudio.yandex.ru/docs/en/search-api/concepts/wordstat) and the [Wordstat API](https://yandex.com/support2/wordstat/en/content/api-wordstat) | Yandex terms (linked, not copied) | `yandex-wordstat`: Wordstat access, methods, prices and quotas |
| [Business Profile service areas](https://support.google.com/business/answer/9157481) and [guidelines](https://support.google.com/business/answer/3038177) | Google terms (linked, not copied) | storefront, service-area and hybrid businesses |
| [ISO 639-2 code list](https://www.loc.gov/standards/iso639-2/php/code_list.php) (Library of Congress) | public standard list | hreflang language codes |
| [Baidu Search Resource Platform](https://ziyuan.baidu.com/): tool handbook, algorithm rules, low-quality pages, notices | Baidu terms (linked, not copied) | the China reference in `international-seo` |
| [StatCounter](https://gs.statcounter.com/search-engine-market-share) and [InternetTrend](http://www.internettrend.co.kr/trendForward.tsp) | their terms (figures quoted with dates, linked) | market share, shown as third-party estimates |
| [Search Engine Journal](https://www.searchenginejournal.com/bing-adds-geo-to-official-guidelines-expands-ai-abuse-definitions/568442), [Search Engine Roundtable](https://www.seroundtable.com/bing-webmaster-guidelines-updated-41002.html), [Baidu AI Traffic Analysis report](https://www.searchenginejournal.com/baidu-now-measures-ai-citations-heres-what-seos-should-and-shouldnt-read-into-it/) | publisher terms (linked, not copied) | dates and facts marked as secondary |
| [Alibaba Cloud ICP filing](https://help.aliyun.com/en/dws/icp-filing) and consultancy articles on ICP | their terms (linked, not copied) | third-party views on ICP, marked as conflicting |
| [Yandex Webmaster help](https://yandex.ru/support/webmaster/) and [Wordstat operators](https://yandex.ru/support2/wordstat/ru/content/operators) | Yandex terms (linked, not copied) | Yandex robots.txt, Webmaster, Wordstat, Alice AI visibility (April 2026) |
| [OpenAI crawlers](https://developers.openai.com/api/docs/bots), [Anthropic crawler help](https://support.claude.com/en/articles/8896518), Perplexity crawler docs | vendor terms (linked, not copied) | AI crawler tokens and IP lists |
| Framework documentation: [Next.js](https://nextjs.org/docs), [Nuxt](https://nuxt.com/docs), [SvelteKit](https://svelte.dev/docs/kit), [Astro](https://docs.astro.build), [React Router](https://reactrouter.com) | MIT (docs and code) | metadata, sitemap and 404 APIs named in the framework recipes |
| [google/robotstxt](https://github.com/google/robotstxt) | Apache 2.0 | named as a test tool |
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | MIT | reviewed for topic coverage only |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT | reviewed for topic coverage only |
| [rampstackco/claude-skills](https://github.com/rampstackco/claude-skills) | MIT | reviewed for topic coverage only |
| [seo-skills/seo-audit-skill](https://github.com/seo-skills/seo-audit-skill) | MIT | reviewed for audit categories only |
| Bukvarix free API, Yandex, Bing and Google suggestion endpoints | unofficial public endpoints | used by `demand.mjs` and `autocomplete.py` (Bing by default; `--engine google` runs at your own risk, because Google's spam policies forbid automated queries); may change without notice |

### Official vendor skills

We looked for official skills from every vendor these skills name, on 30 October 2026, and from Microsoft, Naver and Baidu again on 31 October. Those we read were read at a
commit as context for facts and coverage; `sources.json` and `NOTICE` list the commits. Nothing was copied.

| Vendor | Official skill on this subject | Licence | What it informed |
|---|---|---|---|
| Google Search, Search Console | none: [google/skills](https://github.com/google/skills) has about 180 skills for Cloud, Ads, Analytics and identity, none on Search, Search Console or structured data | Apache 2.0 | its Analytics Data API skill informed the GA4 report in `seo-measurement` |
| Google Chrome | [modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) and [debug-optimize-lcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Apache 2.0 | `core-web-vitals` |
| Microsoft, Bing | none for Bing or Bing Webmaster Tools; [add-seo](https://github.com/microsoft/power-platform-skills) covers Power Pages sites only | MIT | read, nothing used |
| Naver | none found in its GitHub organisation; the 54 official guides are the source for `naver-seo` and `naver-search-advisor` | | |
| Baidu | a skill for [Search Mini Tools](https://ziyuan.baidu.com/aitoolset/index) only, behind a Baidu login | | not read |
| Schema.org | none | | |
| Yandex | none for Search, Webmaster or Wordstat; [kit-skills](https://github.com/yandex/kit-skills) covers Yandex Kit stores only | MIT | read, nothing used |
| Anthropic | [seo-audit](https://github.com/anthropics/knowledge-work-plugins) and seo-ai-visibility | Apache 2.0 | `seo-audit`, `ai-search-visibility`, `google-ai-features`, `ecommerce-seo`; its advice to publish `llms.txt` and FAQ markup was not followed, because Google's documentation says otherwise |
| Semrush | [semrush/skills](https://github.com/semrush/skills), eight skills on its MCP server | Apache 2.0 | `seo-audit`, `structured-data`, `google-rich-results`, `keyword-research`, `link-building` |
| Ahrefs | [ahrefs-api-skills](https://github.com/ahrefs/ahrefs-api-skills), its Python SDK only | Apache 2.0 | read, nothing used |
| Cloudflare | [web-perf](https://github.com/cloudflare/skills) | Apache 2.0 | `core-web-vitals` |
| OpenAI, Perplexity | none on this subject | | |
| WordPress | [wp-performance](https://github.com/WordPress/agent-skills) is about server performance, none on SEO | GPL | not read |
| Vercel, Next.js | none on SEO: [vercel/next.js](https://github.com/vercel/next.js/tree/canary/skills) holds workflow skills, and metadata knowledge now ships in the docs bundled with Next.js | | |
| Nuxt, SvelteKit, Astro, Shopify | none on SEO; their skills cover building with each product | | |
