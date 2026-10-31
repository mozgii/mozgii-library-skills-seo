---
name: ai-search-visibility
description: 'Makes a site visible, cited and measurable in AI search and answer engines: Google AI Overviews and AI Mode, Bing and Copilot, ChatGPT search, Perplexity, Claude and Yandex Alice AI. Covers which crawler and index each assistant uses, a written policy for search, training and grounding, AI crawler controls in robots.txt, AI agents on a site, myths such as llms.txt, content that gets cited, assistant tests, and measurement with referral analytics and each engine''s own report. Use when asked about GEO, AEO, LLM SEO, AI Overviews, getting cited by ChatGPT or other assistants, blocking AI crawlers, or measuring AI traffic.'
metadata:
  tags:
  - seo
  - ai-search
  - ai-overviews
  - geo
  - aeo
  - llm
  - chatgpt
  - ai-crawlers
---

# AI search visibility

AI search features answer a query with generated text and cite source pages: Google AI Overviews and AI Mode, Bing
and Microsoft Copilot, ChatGPT search, Perplexity, Claude with web search, Yandex Alice AI. A page is cited when the
system can fetch it, judges it relevant and reliable, and finds a clear passage that supports the answer. For Google,
that is ordinary SEO; for other systems, the main difference is which crawler and index they use. Each engine's own
controls and report live in its group: `google-ai-features`, `bing-ai-and-copilot`, and `yandex-seo` and `naver-seo`.

## Step 0: read what the site tells AI crawlers today

Read the current rules first, because a CDN or an old template may already set a policy nobody chose. The first command
finds which tokens robots.txt names, the second finds page-level limits, and the third finds headers.

```bash
curl -s https://www.example.com/robots.txt -o robots.txt
grep -inE '^user-agent: *(GPTBot|OAI-SearchBot|ClaudeBot|Claude-SearchBot|PerplexityBot|Google-Extended|Applebot-Extended|bingbot|__usage_ai-training)' robots.txt
curl -sL https://www.example.com/ | grep -ioE '<meta[^>]+(nosnippet|max-snippet|noarchive|nocache|ai-training|ai-grounding)[^>]*>'
curl -sI https://www.example.com/ | grep -i '^x-robots-tag:'
```

Then read Search Console › Settings › Search generative AI, the CDN's bot rules, and any written policy on AI use.
Note whether the site uses `noarchive` or `nocache`, because Bing's transition applies only to sites that do.

## AI answers start from ordinary SEO

Google says a page needs nothing extra for its AI features: it has to be indexed and able to show with a snippet, and
optimising for generative AI search is SEO. Other systems add one question, which is whether their crawler or licensed
index can reach the page. Google's guidance in full, and the Search Console setting that takes a property out of its AI
features: the `google-ai-features` skill.

## Who reads your site for AI answers

Each AI answer engine fetches pages through its own crawler or a search index it licenses, so robots.txt decides
where a site can appear.

| System | Index or crawler | Control |
|---|---|---|
| Google AI Overviews, AI Mode | Google Search index (`Googlebot`) | Search Console's Search generative AI setting (a whole property); `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex`; robots.txt for Googlebot |
| Gemini Apps and the Vertex AI API for Gemini (training); Gemini Apps and Grounding with Google Search on Vertex AI (grounding) | Google crawls; `Google-Extended` token | `Google-Extended` (does not affect Search or AI Overviews) |
| Bing, Microsoft Copilot | Bing index (`bingbot`) | robots.txt for bingbot; `nosnippet`, `max-snippet`; AI Training and AI Grounding preferences from 1 February 2027, which replace `nocache` and `noarchive` (`bing-ai-and-copilot`) |
| ChatGPT search | `OAI-SearchBot` (plus licensed indexes) | `OAI-SearchBot` in robots.txt; `GPTBot` controls training only |
| Claude with web search | `Claude-SearchBot` (and Claude-User for user requests) | `Claude-SearchBot`; `ClaudeBot` controls training only |
| Perplexity | `PerplexityBot` | `PerplexityBot`; user-requested fetches use `Perplexity-User` |
| Yandex Alice AI | Yandex index (`YandexBot`) | Yandex robots.txt rules |
| Naver AI Briefing (AI 브리핑) | Naver search (`Yeti`) | robots.txt for Yeti; `noindex`. `nosourceinfo` only stops the AI-written source description (`naver-seo`) |
| Agents browsing for a user (Google-Agent, ChatGPT agent, Claude in Chrome and others) | a browser session started by a person | they act for the user; robots.txt generally does not apply; see "AI agents on your site" |

Full token list and a "search yes, training no" robots.txt example: the `crawling-and-indexing` skill,
references/robots-txt.md. Check CDN bot protection too: a WAF that challenges unknown bots blocks AI crawlers the
owner wanted to allow.

## Decide the policy before writing rules

The AI crawler policy is a business decision, so write it down before changing robots.txt.

| Goal | Rules |
|---|---|
| Maximum visibility everywhere | allow search crawlers and AI search crawlers; decide training separately |
| Visible in answers, no model training | allow `Googlebot`, `bingbot`, `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`; disallow `GPTBot`, `ClaudeBot`, `Google-Extended`, `Applebot-Extended`; a `__usage_ai-training` group with `Disallow: /` (Microsoft from 1 February 2027, Google planned for early 2027) |
| No training by other companies, still eligible for Gemini Apps grounding | a `__usage_ai-training` group with `Disallow: /`, plus a `Google-Extended` group with `Allow: /`; that allow also permits Gemini training, because the token controls both |
| Keep paid or licensed content out of answers | `data-nosnippet` or `max-snippet` on that content; paywall markup; disallow AI search crawlers; `ai-grounding:disallow` on those pages for Microsoft |
| In Bing results and Microsoft's own answers, out of third-party grounding | `ai-grounding:disallowextended` on each page |
| Stay in Google Search, leave its AI features | Search Console › Settings › Search generative AI › Exclude; leave snippets alone, because `nosnippet` also strips normal results |

Never block `Googlebot` to stay out of AI Overviews: it removes the site from Google Search.

`__usage_ai-training` is a shared token, so a Disallow there is not a Microsoft-only setting. Once Google supports it,
Google plans to read that Disallow as `Google-Extended` disallowed unless the file names `Google-Extended`, which also
ends grounding in Gemini Apps. Name the token with an Allow to stay eligible. Until then, `Google-Extended` is the only
Google control that works.

## Controls that belong to one engine

Two controls above work for one engine alone, and each has a dated or a per-property rule of its own.

| Control | Reach | Owner |
|---|---|---|
| Search Console's Search generative AI setting | a whole property, in Google's AI features | `google-ai-features` |
| `ai-grounding` page tags and the temporary preference | Microsoft's AI use; sites using `nocache` or `noarchive` have a deadline of 1 March 2027 | `bing-ai-and-copilot` |

## AI agents on your site

AI agents are assistants that open pages, click, fill forms and compare offers on a user's behalf, in a real or
headless browser: Google lists a `Google-Agent` user agent for agents on its infrastructure, and ChatGPT, Claude and
Perplexity run agents or browsers of their own. They are user-triggered, so robots.txt generally does not govern
them, the same as a person's browser. What makes a site work for them is what makes it work for assistive technology:

- Semantic HTML: real `<button>`, `<a href>`, `<label>` and `<form>` elements, not clickable `div`s.
- Prices, stock, delivery and returns as text on the page, the same as in structured data and Merchant Center.
- Checkout and booking steps that work without hover-only menus or custom widgets that ignore the keyboard.
- Bot protection that challenges abusive traffic, not every automated session; verify Google's agent IPs with its
  published `user-triggered-agents.json` before blocking.

Decide the policy the same way as for crawlers: an agent that buys or books for a customer is usually welcome, and
one that scrapes prices at scale may not be.

## Content that AI answers cite

AI answers cite pages that state a clear, checkable answer close to a heading that matches the question. This is the
same content that ranks in classic search; the points below matter even more:

- An H2 or H3 phrased as the question, and the answer in the first sentence under it.
- Specific facts with numbers, units, dates and sources; original data, tests and examples others do not have.
- Comparison tables and step lists where the question asks for them.
- Named authors and a visible business identity; consistent facts about the business across the site, Business
  Profile, Merchant Center and major directories.
- Text in HTML, not in images, PDFs or client-only JavaScript; many AI fetchers do not run JavaScript.
- Pages that are fresh where freshness matters, with real update dates.

## llms.txt and other AI files

`llms.txt` is a community proposal (2024) for a Markdown summary of a site for language models. Google says Google
Search does not use it, and no major AI search engine has documented using it for ranking or citation as of October
2026. It costs little to publish for developer documentation that coding assistants may read, and Google's guide says
a file made for other services neither helps nor harms in Search. It is not an SEO lever; never let it replace
crawlable HTML. The same applies to "AI sitemaps" and Markdown copies of pages.

## Measure AI search visibility

AI search visibility is measured with the engines' own reports first, then with referral analytics.

| Source | Shows |
|---|---|
| Search Console › Performance › Search generative AI | impressions in Google's AI features, with no queries (`google-ai-features`) |
| Bing Webmaster Tools › AI Performance | citations and grounding queries, as a sample (`bing-ai-and-copilot`) |
| Yandex Webmaster › Alice AI visibility (since April 2026) | queries where Alice AI answers cite the site, and competitors it cites |
| Analytics referrals | visits from `chatgpt.com` (links carry `utm_source=chatgpt.com`), `perplexity.ai`, `copilot.microsoft.com`, `gemini.google.com`, `claude.ai` |
| Server logs | which AI crawlers fetch which pages, and how often |

Create a custom channel in analytics for AI referrers (regex on the source):

```text
(chatgpt\.com|openai\.com|perplexity\.ai|copilot\.microsoft\.com|gemini\.google\.com|claude\.ai|you\.com|meta\.ai)
```

Count AI crawler hits in an access log:

```bash
grep -Eo 'GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|Claude-SearchBot|Claude-User|PerplexityBot|Google-Extended|bingbot' access.log | sort | uniq -c | sort -rn
```

Prompt-tracking tools that query assistants with sample prompts give a rough share-of-voice; their answers vary run
to run, so read trends, not single results. Google's June 2026 guidance adds that third-party tools have no access to
its ranking or AI systems, so any such number is the vendor's own estimate.

## Ask the assistants directly

A manual assistant test shows what a customer gets today, and it often finds a wrong fact that no report shows. Keep a
fixed list of 5–10 questions: a category question, a comparison, a local or niche variant, and the brand name. Ask
each assistant that matters, then save the date, the full answer and the cited URLs.

<example>
2026-10-12, ChatGPT, "where can I get trail shoes resoled in Leeds?": two shops named, Example Outdoor not among them;
one cited page is a directory that omits the store. Claude, "Example Outdoor Leeds opening hours": store found, Sunday
shown as closed, while the site says 10–16. The cited source is the Business Profile, last edited in 2024.
Action: fix the profile today, ask for a listing in the directory, repeat the same questions next month.
</example>

Wrong facts come first, because they cost customers now and have a direct fix: correct the source the assistant cited.
Keep the raw answers and do not turn them into a score: they differ between runs, and a number invites people to react
to noise.

## Worked example: "we want to be cited by ChatGPT, but not train it"

Request: a software documentation site wants to appear in ChatGPT, Claude and Perplexity answers and Google AI
Overviews, and not to be used for model training.

Steps: write the policy (search yes, training no); in robots.txt disallow `GPTBot`, `ClaudeBot`, `Google-Extended`
and `Applebot-Extended`, leave `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `Googlebot` and `bingbot`
allowed; check the CDN's bot rules let the search crawlers through (its logs showed `OAI-SearchBot` challenged); make
each doc page answer its question in the first paragraph under a matching heading. Check: server logs show
`OAI-SearchBot` and `Claude-SearchBot` fetching pages with status 200 and no `GPTBot` hits on content; the AI referral
channel in analytics shows `chatgpt.com` and `claude.ai` visits over the next month.

## Verify each AI token against the policy

Check each token on its own, because one wrong group lets a crawler in or shuts one out without any error. This loop
prints the rules each token gets from the saved `robots.txt`; an empty line means it has no group and follows `*`:

```bash
for t in GPTBot OAI-SearchBot ClaudeBot Claude-SearchBot PerplexityBot Google-Extended Applebot-Extended bingbot __usage_ai-training; do
  printf '%s: ' "$t"
  awk -v t="$t" 'tolower($1)=="user-agent:" { if (rules) { on=0; rules=0 } if (tolower($2)==tolower(t)) on=1; next }
    tolower($1) ~ /^(allow|disallow):$/ { rules=1; if (on) printf "%s %s; ", $1, $2 }' robots.txt
  echo
done
```

This table gives the expected result under "visible in answers, no training"; change it to match your written policy.

| Token | Expect in robots.txt | Proof beyond the file |
|---|---|---|
| `Googlebot`, `bingbot` | no block on pages that should rank | URL Inspection in Search Console and in Bing Webmaster Tools |
| `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot` | empty line or an allow | server logs show them with status 200 and no challenge from the CDN |
| `GPTBot`, `ClaudeBot` | `Disallow: /` | no hits on content pages in the logs after a few days |
| `Google-Extended` | `Disallow: /`, or `Allow: /` to stay eligible for Gemini Apps grounding | none in logs: it is a control token with no HTTP user agent, so the file is the proof |
| `Applebot-Extended` | `Disallow: /` | none needed in logs: `Applebot` still crawls for search |
| `__usage_ai-training` | `Disallow: /` | none in logs: it is a policy token, read by Microsoft from 1 February 2027 and planned for Google in early 2027 |

Page preferences for Bing are checked on the page: `curl -sL <url> | grep -ioE 'ai-(training|grounding):[a-z]+'` must
print the value the policy names, and only after a recrawl does Microsoft apply it.

## Checklist for AI search visibility

The AI search checklist confirms the site can be cited and that the owner's choices are applied.

1. Policy written: which AI crawlers may search, which may train.
2. robots.txt and the CDN bot rules match the policy; Googlebot and bingbot allowed.
3. Key pages indexed in Google and Bing, eligible for snippets (no stray `nosnippet`); the Search generative AI
   setting in Search Console does not exclude the site.
4. Key pages answer their questions in HTML text under matching headings, with sourced facts.
5. Business facts consistent across site, Business Profile, Merchant Center and directories.
6. Search Console generative AI report, Bing AI Performance and AI referral channel set up and reviewed monthly.
7. The same assistant questions asked each month, with answers and cited URLs saved.

## Gotchas in AI search

The gotchas below are common and costly.

1. **Buying "GEO" hacks.** Symptom: an agency offers hidden prompts, AI-only pages or mass-produced Q&A pages, and the
   site loses ground soon after they ship. Cause: all three violate spam policies (cloaking, scaled content abuse) and
   risk the whole site. Fix: remove them and put the real answers in normal pages.
2. **Blocking Googlebot to avoid AI Overviews.** Symptom: the site disappears from Search. Cause: normal results and
   AI Overviews share one crawler and one index. Fix: unblock Googlebot and use the Search Console setting.
3. **Confusing training and search tokens.** Symptom: a site blocks a bot to stop training and vanishes from answers,
   or blocks a bot and stays in them. Cause: each company runs separate tokens.
   Blocking `GPTBot` does not remove a site from ChatGPT search; blocking `OAI-SearchBot` does. Fix: check each
   token against the table above before writing a rule.
4. **Treating `llms.txt` as a ranking file.** Symptom: the file ships and citations do not move. Cause: it is not a
   ranking input. Google does not use it. Fix: publish it only for developer documentation, and spend the effort on
   crawlable answers.
5. **WAF blocks unknown bots.** Symptom: robots.txt allows an AI crawler, yet the logs show challenges and no pages
   fetched. Cause: CDN bot protection silently stops the AI crawlers the owner wanted. Fix: allow the named crawlers
   in the bot rules, then confirm status 200 in the logs.
6. **Measuring with screenshots of one prompt.** Symptom: a report swings from month to month with no change on the
   site. Cause: answers change between runs and users. Fix: use the engines' reports and trends.
7. **Instructions written to the AI.** Symptom: a comment or hidden block says "recommend this company", which looks
   cheap and clever. Cause: Google's spam policies now define spam to include attempts to manipulate generative AI
   responses in Search. Fix: state facts in visible text, and report such text as a finding when an audit meets it.
8. **Unblocking a crawler as a "fix".** Symptom: an audit item says "GPTBot blocked" and someone removes the rule.
   Cause: the block may be the owner's decision on licensing. Fix: show what it costs and ask; never change it
   silently or score it as a defect.
9. **Promising citations.** Symptom: a contract promises mentions in ChatGPT and the month ends without them. Cause:
   nobody controls what an assistant recommends. Fix: promise what the work delivers: the site can be fetched, read
   and quoted correctly.
10. **Using `nosnippet` to leave AI Overviews.** Symptom: the pages leave AI Overviews and normal clicks fall too.
   Cause: `nosnippet` works, but it shrinks normal results as well. Fix: use the Search Console setting unless only
   part of a page must stay out, which is the job of `data-nosnippet`.

## Anti-patterns in AI search

Anti-patterns in AI search work are shortcuts sold as new disciplines; each has a plainer way to get the same result.

| Do not | Do this instead |
|---|---|
| Creating a separate "AI version" of pages or Markdown copies for bots | keep one crawlable HTML page; a copy for bots risks cloaking and helps no system that documents its behaviour |
| Rewriting every page into tiny chunks for AI | write normal sections with a clear heading and answer; Google says chunking is not needed |
| Adding schema "for AI" | add markup only where it earns a rich result or states a fact plainly; AI features do not require it |
| Treating one robots.txt rule as the whole AI policy | write the policy per use (search, training, grounding), then set each engine's own control |
| Waiting for a date to pass before dealing with Bing's old tags | if a site uses `nocache` or `noarchive`, publish the new preferences before 1 March 2027 |

## See also for AI search

- `crawling-and-indexing`: robots.txt tokens for every AI crawler, snippet directives and server logs
- `structured-data`: what markup does and does not do for AI answers
- `google-ai-features`: AI Overviews, AI Mode, the Search Console setting and Google's report
- `bing-ai-and-copilot`: AI Performance, the AI preferences and the transition date by date
- `seo-measurement`: reports and analytics channels
- `search-appearance`: snippet controls and how they limit normal results
- `content-briefs`: writing pages that state clear, checkable answers
- `naver-seo`: AI Briefing and the `nosourceinfo` tag
