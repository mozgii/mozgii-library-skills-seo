---
title: Reconsideration request template
author: MOZGII, Inc.
lang: en
description: How to write a reconsideration request for a Google manual action, with a template and a filled example for unnatural links.
---

# Reconsideration request template

A reconsideration request asks Google to review a site after a manual action was fixed. A reviewer reads it next to
the site, so it has to show three things with evidence: that you understand what was wrong, that it is fixed on every
affected page, and that it will not come back.

## What a good request contains

A reconsideration request that gets approved on the first try is short, specific and checkable.

1. **The problem in Google's terms**: name the manual action and what caused it on this site.
2. **What you did**: actions with counts and dates, and a link to the evidence (a shared spreadsheet or document).
3. **What remains and why**: links you could not remove and that you disavowed, pages you kept and why they now
   comply.
4. **What prevents a repeat**: the process or rule that changed (who approves sponsored posts, moderation, plugin
   updates).

Leave out blame, pleas and promises without evidence. Never claim a fix that is not live.

## Template for a reconsideration request

The reconsideration request template below follows that order; replace each angle-bracket field.

```text
Manual action: <type, as shown in Search Console>, received <date>.

What was wrong: <one or two sentences, e.g. "From 2023 to 2025 a previous agency bought links on guest-post sites
with exact-match anchors to our service pages.">

What we did:
- <action> (<count>, <dates>). Evidence: <link>
- <action> (<count>, <dates>). Evidence: <link>

What remains: <e.g. "212 links on 140 domains whose owners did not answer two requests; these are in the disavow
file uploaded on <date>.">

What changed so it does not happen again: <rule, owner, process>.
```

## Example: unnatural links to your site

The filled example below is for an "Unnatural links to your site" action.

```text
Manual action: Unnatural links to your site, received 2 September 2026.

What was wrong: From 2023 to early 2025 our former agency placed paid guest posts with exact-match anchors
("trail running shoes", "buy hiking boots") pointing to our category pages.

What we did:
- Audited 3,940 linking domains from Search Console, Bing Webmaster Tools and one third-party index; flagged 318
  domains as paid placements. Evidence: <spreadsheet link>
- Asked all 318 site owners twice (12 and 26 September) to remove the links or add rel="sponsored"; 106 removed,
  72 added sponsored. Evidence: the same spreadsheet, columns F to H.
- Disavowed the remaining 140 domains at domain level on 30 September.

What changed: we ended the agency contract; any sponsored placement now needs approval from the marketing lead and
must carry rel="sponsored". We review new links monthly.
```
