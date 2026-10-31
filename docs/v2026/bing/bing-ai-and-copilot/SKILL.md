---
name: bing-ai-and-copilot
description: 'Handles a site''s place in Microsoft Copilot and Bing''s AI answers: reading the AI Performance report (citations, grounding queries, Citation Share), the AI Training and AI Grounding preferences announced on 30 October 2026, the ai-training and ai-grounding tags, DisallowExtended, the shared __usage_ai-training token and how Google will read it, and the deadlines for sites using noarchive or nocache, with 1 March 2027 as the last date. Use for Copilot citations, grounding queries, a site that never appears in Copilot, ai-training or ai-grounding tags, noarchive or nocache in Bing, stopping Microsoft training on content, or planning for the 2027 transition.'
metadata:
  tags:
  - seo
  - bing
  - copilot
  - grounding
  - ai-performance
  - ai-training
  - noarchive
---

# Bing AI and Copilot

Copilot and Bing's AI summaries draw on the Bing index, and Microsoft gives site owners two things Google does not: a
report that names the phrases behind citations, and separate preferences for training and grounding. The old tags that
controlled this stop counting in 2027, so a site that uses them has a date to meet. This skill reads the report, sets the
preferences and walks the transition. Bing Webmaster Tools setup belongs to `bing-webmaster-tools`.

Facts here were read on Microsoft's own pages on 31 October 2026. Bing's help pages render only with JavaScript, so a
plain fetch of them returns a title and no text: open them in a browser.

## Step 0: read what the site tells Microsoft today

Read the tags first, because a site that serves `noarchive` or `nocache` is in the transition whether anyone chose that or
not, and those tags decide what Copilot may do today.

```bash
curl -sL https://www.example.com/ | grep -ioE '<meta[^>]+(noarchive|nocache|nosnippet|ai-training|ai-grounding)[^>]*>'
curl -sI https://www.example.com/ | grep -i '^x-robots-tag:'
curl -s https://www.example.com/robots.txt | grep -inE '^user-agent: *(bingbot|__usage_ai-training|Google-Extended)'
```

Then read AI Performance in Bing Webmaster Tools, and any written policy on AI use.

## Choose the preference for each goal

Training and grounding are independent, so set each for its own reason. Both default to Allow, and neither changes
eligibility for normal Bing results.

| Goal | Set |
|---|---|
| No training anywhere on the site | robots.txt: `User-Agent: __usage_ai-training` then `Disallow: /` (shared with other companies: see below) |
| No training on one section | the same group with `Disallow: /section/` |
| Train nothing on one page, allow the rest | `<meta name="Bingbot" content="ai-training:disallow">` |
| Grounding only in Microsoft's own products | `<meta name="Bingbot" content="ai-grounding:disallowextended">` |
| No grounding at all | `<meta name="Bingbot" content="ai-grounding:disallow">` |

Grounding has no robots.txt form, so it goes on each page or into a header: `X-Robots-Tag: Bingbot: ai-grounding:disallow`.
A page setting overrides robots.txt for training. Until the new preferences apply, `noarchive` keeps a page out of Copilot
and `nocache` limits Copilot to URL, title and snippet.

## Bing's AI Training and AI Grounding preferences

Bing is replacing `nocache` and `noarchive` with two independent preferences, announced on 30 October 2026 in the post
"Your content, your choice". Neither sets up licensing or payment. Training means changing a generative model's learned
parameters; grounding means using content as input to a generated response.

| Preference | Where it is set | Values |
|---|---|---|
| AI Training (changing a generative model's learned parameters) | robots.txt for a site or path, or a page tag or header, which overrides robots.txt for that page | Allow, Disallow |
| AI Grounding (content used as input to a generated response) | one page at a time; there is no robots.txt form | Allow; DisallowExtended (Microsoft's own products such as Copilot, Microsoft 365, AI Mode and AI Overview, not third-party services such as Web IQ or grounding through the Foundry API); Disallow |

```text
# robots.txt: no training on one path; use Disallow: / for the whole site (Allow is the default)
User-Agent: __usage_ai-training
Disallow: /example-path/
```

```html
<meta name="Bingbot" content="ai-training:disallow">
<meta name="Bingbot" content="ai-grounding:disallowextended">
```

These settings govern use and not crawl access: an Allow does not undo a robots.txt rule that blocks `bingbot`, and a
page's setting counts only once Microsoft recrawls it, so publishing a page tag alone does not take effect before that
recrawl. IndexNow can prompt a recrawl but guarantees no date. Bing warns that Disallow and DisallowExtended cut
visibility in AI answers. Once it finds a new preference on a site, it disregards any `nocache` or `noarchive` left there,
and those tags go back to their original meaning for cached pages in traditional search. The Bing search syndication API
returns links for traditional search, so grounding preferences do not touch it.

## The training token is shared with Google

The robots.txt token belongs to no single company: Microsoft reads it from 1 February 2027, and Google intends to support
it in early 2027. The page tags above are Microsoft's alone. A Disallow written for Bing will therefore reach Google too,
and Google will read it as `Google-Extended` disallowed unless the file names `Google-Extended`. A site that wants to stay
eligible for grounding in Gemini Apps must allow that token explicitly:

```text
User-Agent: __usage_ai-training
Disallow: /

User-Agent: Google-Extended
Allow: /
```

The allow covers Gemini training as well, because `Google-Extended` controls training and grounding together.

## Deadlines for sites that use noarchive or nocache

A site that uses `nocache` or `noarchive` has a deadline, because the old tags stop counting and pages then fall back to
Allow. Sites that never used the old tags need no transition step.

| Date | What happens |
|---|---|
| 15 December 2026 | temporary grounding preferences open in Bing Webmaster Tools, only for sites using `nocache` or `noarchive` on that date |
| 1 February 2027 | Microsoft starts honouring the new preferences as it crawls |
| 1 March 2027 | deadline: publish the training preference, publish the page grounding preference and record the temporary one; after this date the old tags are not read for training or grounding |
| 30 September 2027 | temporary preferences expire, or earlier for a page once a recrawl finds its new preference |

There is no temporary setting for training. Without a temporary grounding preference by 1 March, pages using the old
tags default to Allow for grounding until a recrawl finds the new one. Rulings and syntax in full:
[references/ai-preferences.md](references/ai-preferences.md). Sources: the
[post](https://blogs.bing.com/search/2026/10/your-content-your-choice-clearer-preferences-for-training-and-grounding/)
and [Bing's FAQ](https://www.bing.com/webmasters/help/new-ai-pref-2t1cc16d).

## Read the AI Performance report

AI Performance shows how often a site is cited in generated answers across Copilot, AI summaries in Bing and selected
partners. It has been in public preview since February 2026, with Intents, Topics, Citation Share and Compare in preview
since June 2026, and it names the phrases behind citations, which Google's report does not.

| Metric | Reads as |
|---|---|
| Total citations | how often the site was shown as a source in the period |
| Average cited pages | unique pages cited per day |
| Grounding queries | short phrases the AI used to retrieve the content; grouped, not real user prompts |
| Pages | citations per URL |
| Citation Share (preview) | the site's percentage of citations for one grounding query; competitors are not named |
| Intents, Topics, Compare (preview) | classified queries, themed clusters, and a period overlaid on the chart |

Read it as a trend. The data is sampled, refreshed daily, not a full log, and totals differ between views. A citation is
not a click, and Microsoft says the report does not measure ranking, authority or importance. Sparse sites may see no
grounding queries at all, which Microsoft says is no penalty.

Work the report in this order: pick grounding queries that matter commercially, open their cited pages, find the
queries where the site should appear and has low share, then fix the page that ought to answer (a clear fact near the
top, one topic, current data). Export before and after, and treat a change as an observation: Compare shows what moved,
never why.

## Worked example: a publisher keeps paid guides out of Copilot

Situation: a trade publisher serves `noarchive` on 2,000 paid guides so that Copilot cannot use them. It wants that to
continue after the old tag stops counting, and it wants free articles cited.

The site uses the old tag, so it is in the transition. The team writes the policy: no training anywhere, no grounding on
guides, grounding allowed on articles. On 15 December 2026 it records the temporary grounding preference in Webmaster
Tools. It adds to the guide template:

```html
<meta name="Bingbot" content="ai-grounding:disallow">
```

robots.txt gains a `__usage_ai-training` group with `Disallow: /`. The owner has no interest in Gemini Apps grounding,
so `Google-Extended` stays unnamed, and the team records that Google will read this as a refusal. The `noarchive` tag
comes off the free articles, which removes the block on Copilot there. All of it is done before 1 March 2027.

Check: the guide template serves the tag and the robots.txt group answers, by the commands below. AI Performance shows
cited article pages and no guide pages over the months after Microsoft recrawls. Nothing here promises citations, so the
report states what changed and what the numbers then did.

## Verify the preferences and the report

Verify from outside what the site serves, because a preference counts only after Microsoft recrawls.

```bash
curl -sL https://www.example.com/guides/one | grep -ioE 'ai-(training|grounding):[a-z]+'     # the value the policy names
curl -sI https://www.example.com/guides/one | grep -i '^x-robots-tag:'
curl -s https://www.example.com/robots.txt | grep -iA1 '^user-agent: *__usage_ai-training'   # the Disallow the policy names
curl -sL https://www.example.com/guides/one | grep -icE 'noarchive|nocache'                  # 0 unless kept on purpose
```

1. The temporary preference shows in Webmaster Tools, when the site needs one.
2. robots.txt still allows `bingbot`: a preference does not reopen a blocked crawl.
3. AI Performance's Pages view matches the policy, read as a trend.
4. A citation column and a clicks column stay apart in every report.

## Checklist for Bing AI and Copilot

The checklist covers a change that touches templates, robots rules or AI policy.

1. A written policy states training and grounding separately.
2. AI preferences match the policy, on pages and in robots.txt.
3. A `__usage_ai-training` Disallow was weighed for Google, with `Google-Extended` named or left out on purpose.
4. Sites using `noarchive` or `nocache` have met each date, or plan to before 1 March 2027.
5. No new `noarchive`, `nocache` or `nosnippet` without an owner's decision.
6. `bingbot` is allowed, in robots.txt and in the WAF.
7. AI Performance is reviewed monthly as a trend.

## Gotchas in Bing AI and Copilot

The gotchas below are the costly ones, and several carry a date.

1. **Copilot never cites the site.** Symptom: citations stay at zero and rankings look fine. Cause: `noarchive` or
   `nocache` on the template. Fix: remove them unless the owner chose them.
2. **The old tags stop protecting content.** Symptom: pages the owner kept out of AI answers start appearing in spring
   2027. Cause: after 1 March 2027 the old tags are not read for grounding or training, and pages fall back to Allow.
   Fix: publish the preferences and record the temporary one in Webmaster Tools.
3. **Reports disagree.** Symptom: citations for one query and page differ by filter. Cause: AI Performance samples
   queries and pages over slightly different windows. Fix: compare like with like and read trends.
4. **A citation counted as a visit.** Symptom: a report treats citations as traffic. Cause: AI Performance shows a sample
   of citations, and a citation is neither a click nor traffic. Fix: report citations and visits apart.
5. **A Bing rule reaches Google.** Symptom: a site loses Gemini Apps grounding in 2027 after a robots.txt edit for Bing.
   Cause: `__usage_ai-training` is shared. Fix: name `Google-Extended` with an Allow if the owner wants that grounding.
6. **Copying the FAQ's Allow sample.** Symptom: a training Allow tag does nothing. Cause: the FAQ's sample shows
   `ai-grounding:allow` under a training heading, which looks like a typo. Fix: add no tag, since Allow is the default.
7. **A tag that does nothing yet.** Symptom: the tag is live and the page is still used. Cause: it counts only after a
   recrawl. Fix: record the temporary preference, and use IndexNow to prompt a recrawl, which guarantees no date.

## Anti-patterns in Bing AI and Copilot

Anti-patterns here use the wrong control, or wait for a date.

| Do not | Do this instead |
|---|---|
| Using `nosnippet` to manage AI use | use the AI preferences, because `nosnippet` also strips captions |
| Waiting for a date to pass before dealing with the old tags | if a site uses `nocache` or `noarchive`, publish the new preferences before 1 March 2027 |
| Reading a citation as a visit | keep citations and clicks in separate columns |
| Writing pages for grounding with engineered phrasing | write for readers; prompt injection and keyword stuffing are named abuses |
| Treating a grounding query as a user's prompt | read it as a short, grouped retrieval phrase |
| Claiming a change caused a citation rise | report it as an observation: Compare shows what moved, never why |

## References for Bing AI and Copilot

The reference files below hold the detail for this skill; open one only when the task needs it.

- [references/ai-preferences.md](references/ai-preferences.md): the transition from `noarchive` and `nocache`, date by
  date, with the syntax and the FAQ's rulings.

## See also for Bing AI and Copilot

- `ai-search-visibility`: AI crawlers, policy and citations across every assistant
- `bing-seo`: the Webmaster Guidelines and what makes content groundable
- `bing-webmaster-tools`: where the report and the temporary preference live
- `google-ai-features`: the same questions for Google
- `seo-measurement`: reporting citations beside clicks
