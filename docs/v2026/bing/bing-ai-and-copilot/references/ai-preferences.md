---
title: Bing AI Training and AI Grounding preferences
author: MOZGII, Inc.
lang: en
tags: [bing, copilot, grounding, ai-training, noarchive, nocache]
description: The transition from noarchive and nocache to the AI Training and AI Grounding preferences, with dates, syntax and the FAQ's rulings.
---

# Bing AI Training and AI Grounding preferences

Microsoft announced two separate preferences on 30 October 2026 in the post "Your content, your choice" and in a Webmaster
Tools FAQ. This page holds the dates and rulings a site owner needs. The FAQ page renders only with JavaScript.

## What each preference controls

The AI Training preference covers changing the learned parameters of a generative model; models used only for
non-generative tasks fall outside it, under the IETF working definition. The AI Grounding preference covers using content
as input to a generated response. Ordinary indexing and ranking are not grounding, and allowing grounding guarantees
no inclusion, traffic or payment.

| Preference | robots.txt | Page tag or header | Values |
|---|---|---|---|
| AI Training | yes, a site or a path | yes, overrides robots.txt for that page | Allow, Disallow |
| AI Grounding | no | yes | Allow, DisallowExtended, Disallow |

DisallowExtended allows grounding in Microsoft-operated experiences (AI Mode, AI Overviews, Copilot, Microsoft 365) and
refuses grounding services sold to third parties (Web IQ, grounding through Microsoft Foundry APIs). The two preferences
are independent: Disallow on training and DisallowExtended on grounding is a valid pair.

## Syntax for each preference

The robots.txt token is shared across the industry and built on IETF work in progress. Each participating company says
how it honours it, and Microsoft says it will give notice of any syntax change. The page tags and grounding apply only
to Microsoft; the robots.txt token does not (see "How Google will read the shared training token").

```text
User-Agent: __usage_ai-training
Disallow: /
```

```html
<meta name="Bingbot" content="ai-training:disallow">
<meta name="Bingbot" content="ai-grounding:disallowextended">
<meta name="Bingbot" content="ai-grounding:disallow">
```

```text
X-Robots-Tag: Bingbot: ai-training:disallow
X-Robots-Tag: Bingbot: ai-grounding:disallowextended
X-Robots-Tag: Bingbot: ai-grounding:disallow
```

Do not copy the FAQ's page-level training "Allow" sample: it shows `ai-grounding:allow` under a training heading, which
looks like a typo. Allow is the default, so no tag is needed.

## How Google will read the shared training token

`__usage_ai-training` is not a Microsoft-only token. Google said on 30 October 2026 that it plans to support the same
control, and its crawler documentation gives early 2027 (the post itself says 2027). Google does not act on the token
yet, so until then `Google-Extended` remains the way to refuse Gemini training.

| robots.txt holds | How Google plans to read it |
|---|---|
| `__usage_ai-training` with Disallow, `Google-Extended` not named | as if `Google-Extended` were disallowed: no Gemini training and no grounding in Gemini Apps |
| `__usage_ai-training` with Disallow, `Google-Extended` with Allow | the named token decides: eligible for grounding in Gemini Apps |
| `__usage_ai-training` with Disallow, `Google-Extended` with Disallow | the named token decides: no Gemini training or grounding |

A site that refuses training everywhere and still wants to appear through grounding in Gemini Apps has to allow
`Google-Extended` explicitly. The token controls Gemini training and grounding together, so that allow gives up the
training refusal for Gemini. Other companies can handle the shared token in their own way.

```text
User-Agent: __usage_ai-training
Disallow: /

User-Agent: Google-Extended
Allow: /
```

## Timeline for sites that use noarchive or nocache

The transition applies only to sites using `noarchive` or `nocache` on 15 December 2026. Every other site does nothing.

| Date | Event | Action |
|---|---|---|
| 30 October 2026 | announcement; nothing changes yet | write the policy |
| 15 December 2026 | temporary grounding preferences open in Webmaster Tools | record one, per site |
| 1 February 2027 | Microsoft starts honouring the new preferences as it crawls | publish them on pages |
| 1 March 2027 | deadline; the old tags are no longer read for training or grounding | both steps done |
| 30 September 2027 | temporary preferences expire, or earlier per page once a recrawl finds the new one | all pages recrawled |

A site that wants to keep withholding content from grounding has to do two things before 1 March 2027: publish the
page preference, and record the temporary preference in Webmaster Tools. Publishing alone is not enough, because the page
tag takes effect only when Microsoft recrawls the page, and a recrawl may not happen before the deadline.

There is no temporary setting for training. Publish it in robots.txt or on pages by 1 March 2027.

## Rulings from the FAQ

These answers settle the questions that come up in an audit.

- **No temporary preference by 1 March 2027:** pages using the old tags default to Allow for grounding until a recrawl
  finds the new preference.
- **Published after 1 March 2027:** training preferences still take effect when crawled. Grounding ones take effect on
  recrawl, with no promise that this happens before the temporary preferences expire.
- **Old tags afterwards:** Microsoft disregards them for training and grounding and goes back to their original meaning
  in traditional search, the cached page.
- **An Allow does not reopen crawling:** it does not override a robots.txt rule that blocks Bingbot.
- **Bing results:** limiting either preference does not change eligibility for traditional results.
- **Disagreement between levels:** for training, the page wins; a page with no setting follows robots.txt.
- **Syndication:** the post says the Bing search syndication API returns links for traditional search, so grounding
  preferences do not touch it.
- **Visibility:** the post warns that Disallow and DisallowExtended cut visibility in AI answers.

Sources: [Your content, your choice](https://blogs.bing.com/search/2026/10/your-content-your-choice-clearer-preferences-for-training-and-grounding/),
[FAQ: New AI Preferences](https://www.bing.com/webmasters/help/new-ai-pref-2t1cc16d),
[IETF draft on the training signal](https://datatracker.ietf.org/doc/draft-kelley-aipref-training-preference-signal/),
[Google's October 2026 post on the shared token](https://developers.google.com/search/blog/2026/10/ai-training-control),
[Google's common crawlers](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers).
