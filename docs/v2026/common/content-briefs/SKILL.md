---
name: content-briefs
description: 'Plans and writes search content that people find useful and search engines trust: SERP and intent analysis, content briefs with outline, questions, entities, proof and internal links, people-first and E-E-A-T checks, AI-assisted content within Google''s policies, topic clusters, product reviews and comparisons, and refreshing or pruning decaying content. Use when asked for a content brief, an SEO article or outline, a content plan or topic cluster, how to make content rank, whether AI-written content is allowed, or what to do with old pages losing traffic.'
metadata:
  tags:
  - seo
  - content
  - content-brief
  - eeat
  - helpful-content
  - topic-clusters
  - content-refresh
---

# Content briefs and search content

Search content ranks when it answers the searcher's question better than what already ranks, from real knowledge,
and shows who stands behind it. A content brief is the one-page plan that makes a writer (person or model) produce
that page on the first try.

## Step 0: read what the site already publishes on the topic

Read the site's own pages before briefing a new one, because a second page on one topic splits its signals. List what
exists, using words from the topic:

```bash
curl -s https://www.example.com/sitemap.xml | grep -oE '<loc>[^<]+' | sed 's/<loc>//' | grep -iE 'waterproof|boots'
```

Add `site:example.com waterproof boots` in Google and the Search Console queries for those pages. A page that already
answers the query gets a refresh, not a new brief (see "Refresh, merge or prune old content"). Then read two published
pages of the same type, the style guide if there is one, the author pages, and the keyword plan's owner page.

## What search engines reward in content

Google's ranking systems aim to reward helpful, reliable content made for people, not content made to rank. Its
self-assessment questions boil down to:

- **Who** made it: is the author or business clear, with visible experience or expertise on the topic?
- **How** was it made: first-hand testing, original data, real examples; if AI or automation helped, is that clear
  where readers would expect it?
- **Why** does it exist: to help a reader who arrived from search leave satisfied, or to attract clicks?

E-E-A-T (experience, expertise, authoritativeness, trust) is the frame Google's quality raters use; trust matters
most, and it weighs heavily on "your money or your life" topics (health, finance, safety, law). It is not a single
ranking factor you can add; it is the result of real authorship, accurate content and a reputation others confirm.

## SERP and intent analysis before writing

The SERP analysis tells you what the page must be before anyone writes. For the main phrase, open the top 10 in a
private window for the target market and record:

| Look at | Tells you |
|---|---|
| page types ranking (guides, lists, product pages, tools, videos, forums) | the format the page must take |
| SERP features (AI Overview, People also ask, video, local pack, shopping) | which extra formats to cover |
| the questions every top page answers | the minimum coverage |
| what none of them has (data, tests, examples, a calculator) | the angle that makes yours better |
| freshness of the top results | whether dates and updates matter |

If the top 10 is all product listings, an article will not rank there; pick another phrase or another page type.

## Write the content brief

The content brief fits on one page; the template with an example is in
[references/brief-template.md](references/brief-template.md). It holds:

1. Main phrase, secondary phrases, intent, page type, target URL (from `keyword-research`).
2. The reader: who they are, what they know, what they need to decide or do.
3. The answer in two sentences: what the lead must say.
4. Outline: H2s from real sub-questions, each with the point it makes and the proof it needs.
5. Proof and sources: data, examples, quotes, tests; who on the team can supply them.
6. Entities and terms the page must explain (products, standards, places, people).
7. Internal links: the hub it links up to, the pages it links to, the pages that will link to it.
8. Title and meta description drafts within the `on-page-seo` limits.
9. Author with credentials, reviewer for YMYL topics, and publication and update dates.
10. Done criteria: the questions a reader must be able to answer after reading.

## Writing rules for search content

The writing rules below keep the page useful for readers and clear for engines and AI answers.

- Answer first: the lead gives the answer (definition, price range, verdict, steps) in its first two sentences.
- One H2 per sub-question; the first sentence under it answers it directly.
- Add what only you have: your numbers, tests, photos, customer cases, expert quotes, a tool or template.
- Name sources with dates and link them; mark estimates as estimates.
- Plain language, short paragraphs, lists for steps, tables for comparisons.
- Show the author with a short bio and a link to an author page; show the update date when the content is
  time-sensitive.
- No filler openers ("In today's fast-paced world..."), no stacked hedges, no keyword repetition for its own sake.

## AI-assisted content and Google's policies

Google's policy on AI-generated content judges the result, not the tool: content made with AI is fine when it is
helpful, accurate and original; using automation to mass-produce pages that add no value is scaled content abuse,
whether a person, a model or a scraper made them. In practice:

- A person with subject knowledge sets the angle, supplies the facts and proof, and edits the result.
- Every factual claim is checked against a source; models invent numbers, studies and quotes.
- Disclose AI involvement where a reader would reasonably expect it (for example, AI-generated images or reviews).
- Never publish hundreds of near-identical pages for query variants; Google's 2026 AI guide names this as a risk.

## Topic clusters

A topic cluster is a hub page that covers a topic broadly and a set of pages that each cover one sub-topic in depth,
all linked to each other. Plan clusters from the keyword map: the hub owns the broad phrase, each spoke owns one
narrower phrase, spokes link to the hub and to the commercial page they support (`internal-linking`). Clusters show
depth on a topic; they do not need to be large, they need to be complete.

## Programmatic pages and reviews

Two content types have their own rules. Pages generated from data at scale (locations, integrations, comparisons)
are legitimate only when each page carries data unique to it; the `programmatic-seo` skill covers them. Product
reviews, "best X" lists and "X vs Y" comparisons are judged by Google's reviews guidance: first-hand testing,
measurements, photos, pros and cons, and a clear verdict. The rules and a review brief are in
[references/reviews-and-comparisons.md](references/reviews-and-comparisons.md).

## Refresh, merge or prune old content

Content decay is the slow loss of traffic as pages age and competitors improve. Review pages that lost more than
about 30% of clicks over 6–12 months (Search Console, compare periods by page):

| Situation | Action |
|---|---|
| still the right topic, outdated facts | update facts, examples, screenshots; change `dateModified` only for real updates |
| intent changed (the SERP now shows another page type) | rewrite to the new format |
| two or more pages on the same topic | merge into the strongest URL and 301 the others |
| no traffic, no links, no business value | delete (404 or 410) or `noindex`; keep if it serves users who arrive other ways |

Changing only the date to look fresh is not an update; engines and readers notice.

## Worked example: a brief for "how to waterproof hiking boots"

Request: an outdoor shop wants an article for "how to waterproof hiking boots" (2,400 searches a month in the US).

SERP: the top 10 are step-by-step guides and two videos; People also ask covers wax against spray, Gore-Tex boots and
how often. None shows a test. Brief: intent informational, page type guide, H2s from those four questions plus
"leather, suede and fabric need different products"; the angle is the shop's own spray-and-wax soak test with
photos; the lead answers "clean, dry, apply wax to leather or spray to fabric, cure 24 hours"; the author is the
store's boot fitter; links up to the hiking boots category and to the care products. Done when a reader can pick the
right product for their boot material and knows how often to reapply.

## Verify a page against its brief

A brief is proven on the published page, not in the document. Fetch the page and compare what is served with the
brief:

```bash
curl -sL https://www.example.com/guides/waterproof-hiking-boots > page.html
python3 - page.html <<'EOF'
import re, sys
html = open(sys.argv[1], encoding="utf-8", errors="replace").read()
strip = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()
print("title:", strip("".join(re.findall(r"<title[^>]*>(.*?)</title>", html, re.S | re.I))))
print("h1:", [strip(h) for h in re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)])
print("h2:", [strip(h) for h in re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S | re.I)])
first = re.search(r"<p[^>]*>(.*?)</p>", html, re.S | re.I)
print("lead:", strip(first.group(1))[:300] if first else "NO PARAGRAPH")
print("dates in markup:", re.findall(r'"date(?:Published|Modified)"\s*:\s*"([^"]+)"', html))
EOF
```

Expect one H1, the brief's H2s, a lead that gives the answer in two sentences, and a `dateModified` that matches the
visible date. Then read it as the brief's reader: every done criterion can be answered from the page, each number has
a source, and at least one thing is on the page that the top 10 lacks. Six to eight weeks later, Search Console ›
Performance filtered to the page shows impressions for the main phrase. When the page is missing from the results,
check it is indexed before judging the content.

## Checklist for a search content page

The content checklist is run before publishing.

1. SERP checked; the page type matches what ranks.
2. Brief complete: phrase, reader, answer, outline, proof, links, author.
3. Lead answers the query in two sentences.
4. Every H2 answers a real sub-question, starting with the answer.
5. At least one thing the top 10 lacks: data, test, example, tool.
6. Every fact sourced or checked; no invented numbers or quotes.
7. Author named with credentials; YMYL pages reviewed by a qualified person.
8. On-page contract met (`on-page-seo`); internal links in and out added.

## Gotchas in search content

The gotchas below are why well-written content still does not rank.

1. **Wrong format for the intent.** Symptom: a long guide stalls on page two while Google shows product listings for
   the query. Cause: the page type does not match what the SERP rewards. Fix: build the page type that ranks, or pick
   another phrase.
2. **Rewriting the top 10.** Symptom: the page is indexed and gets no traction. Cause: a summary of what already ranks
   adds nothing; Google calls this out as unhelpful. Fix: add data, a test or an example the others lack.
3. **Unverified AI drafts.** Symptom: a reader or a reviewer finds a study that does not exist. Cause: models invent
   statistics and quotes; fabricated ones destroy trust and can trigger spam reports. Fix: check every claim against a
   source before publishing.
4. **Author pages with no substance.** Symptom: the byline is there, yet the page reads as anonymous. Cause: a name
   without credentials or other work does not show expertise. Fix: add a real bio, credentials and the author's other
   work.
5. **Publishing without internal links.** Symptom: a new article stays unindexed or ranks weakly for weeks. Cause:
   content no page links to is found late. Fix: link it from its hub and related pages on publication day.
6. **Fake freshness.** Symptom: the date moves and rankings do not, or readers complain the page is stale. Cause: the
   date was updated without changing the content. Fix: change the date only with a real update.

## Anti-patterns in search content

Anti-patterns in search content are habits that fill a page without giving a reader a reason to stay.

| Do not | Do this instead |
|---|---|
| Writing to a word count | write until the sub-questions are answered, then stop |
| Briefing with a keyword list alone | give the writer the reader, the answer, the proof and the links |
| Publishing hundreds of near-identical AI pages | use a person with subject knowledge on each page, or build real programmatic pages with unique data |
| Hiding AI involvement where readers expect to be told | disclose it for AI-generated images, reviews and similar content |
| Deleting old posts by age alone | decide by traffic, links and business value, using the refresh table |

## References for content briefs

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/brief-template.md](references/brief-template.md): the brief template with a filled example.
- [references/reviews-and-comparisons.md](references/reviews-and-comparisons.md): product reviews, "best" lists and
  comparison pages that meet Google's reviews guidance, with a review brief.

## See also for search content

- `keyword-research`: the phrase, intent and owner page a brief starts from
- `on-page-seo`: title, description and heading limits
- `internal-linking`: hubs and links on publication day
- `programmatic-seo`: pages generated from data
- `algorithm-updates-and-penalties`: what to do when a core update hits content
