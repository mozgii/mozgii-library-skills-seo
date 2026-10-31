---
name: google-ai-features
description: 'Handles a site''s place in Google''s AI features, AI Overviews and AI Mode: what Google says matters (checked October 2026), that they use the normal index and need no special files, chunking or markup, the Search generative AI setting in Search Console that takes a property out without touching normal results, snippet controls, Google-Extended and Gemini, and the Search generative AI report. Use when asked how to appear in AI Overviews or AI Mode, how to leave them, whether opting out hurts rankings, what the generative AI report shows, or whether Google-Extended affects AI Overviews.'
metadata:
  tags:
  - seo
  - google
  - ai-overviews
  - ai-mode
  - gemini
  - google-extended
  - search-console
---

# Google AI features

AI Overviews and AI Mode answer a query with generated text and links, using the same index and core ranking and quality
systems as normal results. So appearing in them is ordinary SEO, and leaving them is one setting in Search Console. This
skill covers what Google says, each control, and the report. Policy across every assistant belongs to
`ai-search-visibility`.

## Step 0: read what the site tells Google today

Read the current signals first, because a template may already limit snippets, and someone may already have set the
property to Exclude.

```bash
curl -s https://www.example.com/robots.txt | grep -inE '^user-agent: *(Googlebot|Google-Extended|__usage_ai-training)'
curl -sL https://www.example.com/ | grep -ioE '<meta[^>]+(nosnippet|max-snippet)[^>]*>|data-nosnippet'
curl -sI https://www.example.com/ | grep -i '^x-robots-tag:'
```

Then read Search Console › Settings › Search generative AI for the property and its parent, and the Search generative AI
report for what the site shows today.

## Choose the control for each goal

Each Google control reaches something different, so pick by what must change and what must stay.

| Goal | Use | Why the others lose here |
|---|---|---|
| Stay in Search, leave its AI features | Search Console › Settings › Search generative AI › Exclude | `nosnippet` also strips normal results |
| One section out, the rest in | a URL-prefix or subdomain property set to Exclude | the setting on the parent would take everything out |
| Part of a page out of answers | `data-nosnippet` on that part | the setting works on a whole property |
| Shorter use of a page's text | `max-snippet` | it shrinks the normal snippet as well |
| No Gemini training, for Gemini Apps or the Vertex AI API for Gemini | `Google-Extended` disallowed | it also ends grounding in Gemini Apps and in Grounding with Google Search on Vertex AI; it does not affect Search or AI Overviews, so it never removes a site from them |
| Out of Search entirely | `noindex` | the setting does not take a page out of Search |
| Stay out of AI Overviews by blocking the crawler | never | it removes the site from Google Search |

## What Google says about AI features

Google's guidance (the "AI features and your website" page and the May 2026 guide "Optimizing your website for
generative AI features on Google Search", updated July 2026) is direct:

- A page needs nothing extra: it has to be indexed and able to show with a snippet. AI features use the same index and
  core ranking and quality systems.
- The 2026 guide adds one condition: the property has to stay included under Search generative AI features in Search
  Console. Inclusion is the default, so check that nobody set the property to Exclude (see "Leave Google's AI
  features with the Search Console setting").
- Optimising for generative AI search is SEO. Google does not treat "GEO" or "AEO" as separate disciplines.
- You do not need new machine-readable files, AI text files, special markup or Markdown versions. Google Search does
  not use `llms.txt`.
- There is no need to break content into small chunks, no ideal page length, and no special writing style for AI.
- Structured data is not required for AI features (it still helps rich results and understanding).
- Seeking inauthentic "mentions" across the web is not as helpful as it seems; spam systems handle manipulation.
- What helps: unique, non-commodity content from first-hand experience, clear structure with headings, good images and
  video, crawlable pages, semantic HTML, a good page experience, current Merchant Center and Business Profile data.

## Leave Google's AI features with the Search Console setting

The Search generative AI setting takes a property out of Google's AI features and leaves its normal results alone. It
sits in Search Console › Settings › Search generative AI and reached every site by 31 August 2026.

| Option | What happens |
|---|---|
| Include (the default) | links and content can appear in the features and ground their answers |
| Exclude | nothing from the property appears there, so no impressions or traffic from them |
| Inherit from parent | follows the closest parent property with a manual choice; the default on a child property |

- Its reach is AI Overviews, AI Mode and Discover's generative AI features. Google says that list may change.
- It works per property and its subpages. A URL-prefix or subdomain property can differ from its parent, so one
  section can leave while the rest stays; owners of the top-level domain property see a notice on the control page.
- A change takes a few days. Content usually drops out 1–2 days after the change goes live, though caches can hold
  some for longer.
- It is not a ranking signal for the rest of Search, and Google may still use the content for Search overall (for
  example to understand query language).
- It does not cover model training: that is `Google-Extended`. It does not override Merchant Center or Google Ads
  participation, and `noindex` is still the way out of Search entirely.
- An excluded site loses the "preferred" badge in AI Overviews and AI Mode, and the generative AI report has nothing
  to show.

Read the report before changing the setting: what it shows is what the site gives up.

## Google-Extended, Gemini and the shared training token

`Google-Extended` is a robots.txt token with no HTTP user agent: Google crawls, and the token decides use in training
the Gemini models behind Gemini Apps and the Vertex AI API for Gemini, and in grounding for Gemini Apps and for Grounding
with Google Search on Vertex AI. It does not affect Search or AI Overviews. Until Google supports the shared
`__usage_ai-training` token, planned for early 2027, `Google-Extended` is the only Google control that works for training.

Once Google supports it, a `__usage_ai-training` Disallow reads as `Google-Extended` disallowed unless the file names
`Google-Extended`, which also ends grounding in Gemini Apps. Name the token with an Allow to stay eligible. That allow
also permits Gemini training, because the token controls both. The rule set is in `ai-search-visibility`.

## Measure Google's AI features with the generative AI report

Search Console counts AI features in two places, and neither gives queries for AI alone.

| Source | Shows |
|---|---|
| Search Console › Performance › Search generative AI (Google calls it the Generative AI performance report; all sites by 31 August 2026) | impressions of your URLs in Google's AI features in Search and Discover, by page, country, device (Search only) and date; no query data; empty for an excluded property |
| Search Console Performance (Web) | AI Overviews and AI Mode clicks and impressions are counted inside the normal Web totals |

Google's June 2026 guidance adds that third-party tools have no access to its ranking or AI systems, so any such number
is the vendor's own estimate.

## Worked example: a publisher takes one section out of AI Overviews

Request: a subscription publisher wants `/research/` out of Google's AI features, and everything else left alone.

The generative AI report shows 40,000 impressions a month on `/research/` pages, and the owner accepts losing them. Blocking
Googlebot would drop the section from Search, and `nosnippet` would shrink its normal results, so neither is used. The
team verifies a URL-prefix property at `https://www.example.com/research/`, and sets it to Exclude. The domain property stays
on Include, and if it is the top-level domain property, its owners see a notice on the control page.

Check: after a few days the generative AI report for the new property has nothing to show; URL Inspection still shows the
pages indexed. Web clicks to `/research/` may fall by what AI features brought, because those clicks sit inside Web
totals; a wider fall has another cause. The rest of the site's generative AI impressions do not move.

## Verify a Google AI setting

The file and the headers are checked from outside; the setting and the report only inside Search Console.

```bash
curl -sL https://www.example.com/research/report | grep -ioE '<meta[^>]+nosnippet[^>]*>'     # expect nothing unless chosen
curl -s https://www.example.com/robots.txt | grep -iA2 '^user-agent: *googlebot'             # expect no Disallow on pages that should rank
```

1. Settings › Search generative AI shows the choice on the right property, and each child's Inherit or override.
2. URL Inspection shows the page indexed with a snippet allowed.
3. The generative AI report matches the choice: impressions for Include, nothing for Exclude.
4. Web totals lost at most what AI features brought, read a week after the change.

## Checklist for Google AI features

The checklist confirms the site can appear, or has left on purpose.

1. Key pages indexed and able to show with a snippet.
2. The property is on Include, or the owner chose Exclude in writing.
3. Child properties checked for an override.
4. Googlebot is allowed; no stray `nosnippet` on templates.
5. The training decision is made separately, with `Google-Extended`.
6. The generative AI report is read monthly.
7. Business facts current in Merchant Center and Business Profile.

## Gotchas with Google's AI features

The gotchas below are the ones that cost traffic or a wrong report.

1. **Blocking Googlebot to avoid AI Overviews.** Symptom: the site disappears from Search. Cause: normal results and
   AI Overviews share one crawler and one index. Fix: unblock Googlebot and use the Search Console setting.
2. **Using `nosnippet` to leave AI Overviews.** Symptom: the pages leave AI Overviews and normal clicks fall too.
   Cause: `nosnippet` works, but it shrinks normal results as well. Fix: use the Search Console setting unless only
   part of a page must stay out, which is the job of `data-nosnippet`.
3. **An empty generative AI report.** Symptom: the report shows nothing. Cause: the property may be set to Exclude, or it
   may have no AI impressions yet. Fix: check the setting before reporting zero visibility.
4. **`Google-Extended` expected to remove AI Overviews.** Symptom: the token is disallowed and the site still shows in
   AI Overviews. Cause: it controls Gemini training and app grounding, not Search. Fix: use the Search Console setting.
5. **A section stays included after the parent changes.** Symptom: pages still appear after Exclude on the domain
   property. Cause: a child property holds its own manual choice, or caches keep some content for longer. Fix: read each
   child's setting, and wait a few days.
6. **A shared token ends Gemini grounding.** Symptom: from early 2027, a site loses grounding in Gemini Apps after a
   robots.txt edit made for Bing. Cause: Google plans to read a `__usage_ai-training` Disallow as `Google-Extended`
   disallowed unless the file names that token. Fix: add a `Google-Extended` group with `Allow: /` if the owner wants it.

## Anti-patterns with Google's AI features

Anti-patterns here buy a special treatment that Google says does not exist.

| Do not | Do this instead |
|---|---|
| Rewriting every page into tiny chunks | write normal sections; Google says chunking is not needed |
| Publishing Markdown copies for Google | keep one crawlable HTML page; Google needs no special files |
| Adding schema "for AI Overviews" | add markup only where it earns a rich result or states a fact |
| Reporting AI clicks from Web totals as a separate number | say they sit inside Web, and use the generative AI report for impressions |
| Excluding the site without reading the report | read what it shows first: that is what the site gives up |

## See also for Google's AI features

- `ai-search-visibility`: AI crawlers, policy across assistants, agents and assistant tests
- `search-console`: reports, properties and exports
- `search-appearance`: snippet controls and how they limit normal results
- `crawling-and-indexing`: `noindex` and robots.txt
- `google-rich-results`: what markup earns in Google
- `bing-ai-and-copilot`: the same questions for Microsoft
