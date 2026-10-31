---
name: algorithm-updates-and-penalties
description: 'Diagnoses and recovers from Google core updates, spam updates, manual actions and hacked-site security issues: dating a drop against the Search Status Dashboard, telling an algorithmic demotion from a manual action, the spam policies as of October 2026 (scaled content, site reputation, expired domains, back button hijacking), reconsideration requests and cleanup after a hack. Use when traffic fell after a Google update, Search Console shows a manual action or security issue, a client asks about a penalty, or a site was hacked.'
metadata:
  tags:
  - seo
  - core-update
  - manual-action
  - spam-policies
  - penalty-recovery
  - hacked-site
---

# Algorithm updates, penalties and recovery

A site loses Google traffic to an update in one of three ways: a core update re-ranks it against everything else, a
spam system or spam update demotes it for a policy violation, or a person at Google applies a manual action. A hack
is a fourth, and the most urgent. Each has a different test and a different way back, so the first job is always to
say which one it is.

## Step 0: read the drop's date and what changed on the site

Read the exact day clicks moved first, because every test below compares that day with something else. This prints daily
Search Console clicks for a property, and needs a token with the `webmasters.readonly` scope in `GSC_TOKEN`:

```bash
curl -s -X POST "https://searchconsole.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query" \
  -H "Authorization: Bearer $GSC_TOKEN" -H "Content-Type: application/json" \
  -d '{"startDate":"2026-05-01","endDate":"2026-06-15","dimensions":["date"],"rowLimit":100}' \
| python3 -c "import json,sys; [print(r['keys'][0], int(r['clicks'])) for r in json.load(sys.stdin)['rows']]"
```

Then list the site's releases, migrations and tracking changes around that day, and who can read Security and manual
actions in Search Console.

## Which of the four it is

To find out whether a drop is an update, a spam demotion, a manual action or a hack, run these checks in order.

| Check | Where | If yes |
|---|---|---|
| A message or entry in Security issues | Search Console › Security and manual actions › Security issues | hack: "Clean up a hacked site" below, before anything else |
| A manual action listed | Search Console › Security and manual actions › Manual actions | manual action: fix and file a reconsideration request |
| The drop starts during a spam update | Search Status Dashboard (status.search.google.com), Ranking section | spam demotion: find and remove the violation; no request to file |
| The drop starts during a core update | same dashboard | core update: assess quality; recover over months |
| None of the above | — | not an update: the `seo-measurement` traffic-drop steps (tracking, technical, demand) |

A drop on a date with no update and no message is usually technical or seasonal. Rule that out first, because it is
the only kind that can be fixed in a day.

## Google updates in 2025 and 2026

The Search Status Dashboard lists every announced ranking update with start and end dates. The recent ones (US
Pacific dates, checked October 2026):

| Update | Started | Finished |
|---|---|---|
| September 2026 spam update | 24 Sep 2026 | about 7 Oct 2026 |
| August 2026 spam update | 18 Aug 2026 | about 20 Aug 2026 |
| June 2026 spam update | 24 Jun 2026 | about 26 Jun 2026 |
| May 2026 core update | 21 May 2026 | about 1 Jun 2026 |
| March 2026 core update | 27 Mar 2026 | about 8 Apr 2026 |
| March 2026 spam update | 24 Mar 2026 | about 25 Mar 2026 |
| February 2026 Discover core update (Discover only) | 5 Feb 2026 | about 26 Feb 2026 |
| December 2025 core update | 11 Dec 2025 | about 29 Dec 2025 |
| August 2025 spam update | 26 Aug 2025 | about 21 Sep 2025 |
| June 2025 core update | 30 Jun 2025 | about 16 Jul 2025 |
| March 2025 core update | 13 Mar 2025 | about 26 Mar 2025 |

Google also ships smaller core updates it does not announce, so a change between these dates can still be a ranking
change. Read the dashboard again before writing a report: this table ages.

## Read a core update drop correctly

A core update re-weighs how Google judges relevance and quality across all sites; it targets no site and has no
specific fix. Google's own procedure:

1. Wait until at least a week after the update finished.
2. In Search Console › Performance, compare that week with the week before the update started (same weekdays).
3. Split by search type (Web, Image, Video, News) and by page: find which pages and query groups lost.
4. A drop of a few positions on a few queries needs nothing; do not rewrite pages that still perform.
5. For a large, lasting drop, assess the affected pages honestly against people-first content questions (who made
   it, how, why; the `content-briefs` skill has them), and ask someone outside the team to judge them too.

Recovery: some changes show within days, but Google's systems can take months to see that a site improved, and the
next core update is often when it shows. Google guarantees no recovery. Deleting content is a last resort; whole
sections written mainly for search engines are the strongest sign that broad changes are needed.

## Worked example: a recipe blog after the May 2026 core update

Situation: a recipe blog lost 45% of clicks between 21 May and 1 June 2026.

Check: no manual action, no security issue; the dates match the May 2026 core update. The week of 8 June against
the week of 11 May shows the loss on 120 "best X" roundup pages that list recipes from other sites with one line
each; the 300 tested recipes with step photos held steady.

Report: core update re-ranking, concentrated on thin roundups. Plan: merge the roundups into 15 pages with tested
picks and own photos; leave the recipes alone; measure again a week after the next core update.

## Spam policies that cause demotions

Google's spam policies (page updated 28 August 2026) list the practices that its spam systems demote and its
reviewers act on. The full list with how to check a site for each is in
[references/spam-policies.md](references/spam-policies.md). The ones that hit ordinary businesses most often:

- **Scaled content abuse**: many pages made mainly to rank, however they are produced (AI, templates, scraping,
  stitching). Fix by removing or `noindex`-ing the set, not by editing a few pages.
- **Site reputation policy** (often called site reputation abuse): third-party pages hosted to borrow the host's ranking signals (coupon, casino, payday
  sections on a news site). Since 30 August 2026 these manual actions no longer apply to results shown in the
  European Economic Area, where such sections are instead ranked separately from the main site; elsewhere the
  policy is enforced as before.
- **Expired domain abuse**: a bought, lapsed domain reused to rank low-value content on its old reputation.
- **Back button hijacking**: scripts that stop the browser's back button returning to the results (history
  manipulation, injected entries). Added in April 2026 under malicious practices, enforced from 15 June 2026; ad and
  "recommended content" scripts are a common source the site owner did not write.
- **Link spam**, **thin affiliation**, **doorways**, **keyword stuffing**, **cloaking and sneaky redirects**,
  **user-generated spam** and **hacked content**.
- **Manipulating AI answers**: the policies' opening definition of spam has included attempts to manipulate generative
  AI responses in Google Search since May 2026. There is no separate policy heading; hidden prompts and generated page
  sets fall under hidden text and scaled content abuse.

A spam demotion lifts automatically once the systems see the violation is gone, which can take months. There is no
request to file unless a manual action was also applied.

## Manual actions and reconsideration requests

A manual action is a penalty a person at Google applied; it is listed in Search Console › Security and manual
actions › Manual actions, with the affected pages or "site-wide". Since April 2026 Google says spam reports sent by
users may lead to one. Types in October 2026 include: back button
hijacking, site abused with third-party spam, user-generated spam, spammy free host, structured data issue,
unnatural links to your site, unnatural links from your site, thin content with little or no added value, cloaking
or sneaky redirects, major spam problems, cloaked images, hidden text or keyword stuffing, AMP content mismatch,
sneaky mobile redirects, News and Discover policy violations, and site reputation policy.

To get a manual action lifted:

1. Expand the action to see which pages and which policy it names.
2. Fix every affected page; a partial fix earns no partial return.
3. Make the fixed pages reachable by Googlebot (no login, no `noindex`, no robots.txt block), checked with URL
   Inspection.
4. Click **Request review** and write the request: what was wrong, what you changed, with examples and numbers,
   and what stops it from happening again. Template:
   [references/reconsideration-request.md](references/reconsideration-request.md).
5. Wait for the email with the result (days to weeks; link actions take longer). Do not resubmit while one is
   pending.

When the action is lifted, rankings return to what the site earns without the violation, not to the inflated level it
had while the violation worked.

## Clean up a hacked site

A hacked site serves spam or malware the owner did not put there, and Google may warn searchers, drop pages or show
the spam in results. Act the same day:

1. Read Search Console › Security issues: the type (hacked content, malware, social engineering, unwanted software)
   and sample URLs.
2. Take the site offline or into maintenance (503) if it serves malware; change every password, revoke old keys and
   sessions, and tell the host.
3. Find the injection: new files and users, modified core files, `.htaccess` and server config rewrites, database
   entries with spam links, cloaked pages that show spam only to Googlebot (fetch with a Googlebot user agent and
   compare). The common patterns are in [references/spam-policies.md](references/spam-policies.md).
4. Restore from a clean backup or remove the code; patch the hole (an outdated plugin, a theme, a leaked password).
5. Let spam URLs return 404 or 410; add a sitemap of the real URLs; use Removals for the worst spam URLs.
6. In Security issues, click **Request review** and describe the cleanup. Malware reviews usually take days; hacked
   spam reviews can take longer.

## Verify the diagnosis and the cleanup

Each claim in the report needs a check someone else can repeat. To match the drop to an update, list what the Search
Status Dashboard recorded around it. Its feed has no documentation and may change, so the dashboard page stays the
reference:

```bash
curl -s https://status.search.google.com/incidents.json | python3 -c '
import json, sys
start, end = "2026-05-01", "2026-06-15"
for i in json.load(sys.stdin):
    if i["begin"][:10] <= end and (i.get("end") or end)[:10] >= start:
        print(i["begin"][:10], (i.get("end") or "ongoing")[:10], i["external_desc"])'
```

To rule out cloaked spam, compare what a crawler user agent and a browser get. Any spam text or link that shows only on
the Googlebot side is a hack:

```bash
GB='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
diff <(curl -sL -A "$GB" https://www.example.com/ | tr '>' '\n') <(curl -sL https://www.example.com/ | tr '>' '\n') | head -40
```

A site that cloaks by IP passes this test, so also read the rendered HTML in URL Inspection. After a cleanup, confirm
every spam URL is gone (`spam-urls.txt` holds one per line):

```bash
while read -r u; do curl -s -o /dev/null -w "%{http_code} $u\n" "$u"; done < spam-urls.txt | grep -vE '^(404|410) '   # expect no output
```

The work is done when Security issues and Manual actions are empty or under review, the fixed pages pass URL Inspection,
and the next core update's week-after comparison has been read against the plan.

## Checklist after an update or a penalty

The checklist below is the minimum before telling a client why traffic fell and what to do.

1. Security issues and Manual actions reports read and recorded, both empty or each item handled.
2. The drop dated from daily Search Console clicks and matched (or not) to a dashboard update.
3. Losing pages and query groups listed, with the week-after comparison.
4. Technical causes ruled out on the losing templates (indexing, canonicals, rendering, status codes).
5. Each spam policy that could apply checked against the site, with evidence for or against.
6. A recovery plan that names what changes, why, and when it will be measured (after the next core update for a core
   drop).

## Gotchas with updates and penalties

The gotchas below are why recovery plans fail.

1. **Calling every drop a penalty.** Symptom: a client asks which penalty hit the site, and no report shows one.
   Cause: most drops are core updates or technical faults; "penalty" means a manual action or a spam demotion, and
   both have evidence. Fix: name the kind only after the four checks at the top of this skill.
2. **Disavowing links after a core update.** Symptom: a disavow file goes in and nothing changes. Cause: a core update
   is not about links you can disavow; the disavow tool is for unnatural-link manual actions. Fix: leave the links
   alone and assess the content.
3. **Rewriting the winning pages too.** Symptom: pages that held their rankings start to slip after a site-wide
   rewrite. Cause: the plan changed everything instead of what lost; pages that held are evidence of what works. Fix:
   change the losing pages and the reason they lost.
4. **Judging recovery a week later.** Symptom: a team calls the work a failure after seven flat days. Cause: core
   changes show over months. Fix: measure after the next core update.
5. **Missing the third-party script.** Symptom: the site's own code is clean, yet users hit a back button trap, a
   mobile redirect or injected links. Cause: back button hijacking, sneaky mobile redirects and injected links often
   come from an ad network, a "related content" widget or a plugin. Fix: test the live page on a phone and turn
   scripts off one at a time.
6. **Moving the spam to a subdomain.** Symptom: the action follows the content to its new home. Cause: Google's policy
   circumvention rule extends the action to the new place. Fix: remove the violation rather than relocate it.
7. **Cleaning the hack but not the hole.** Symptom: the site is reinfected within days. Cause: the entry point is
   still open. Fix: find and patch the entry point before asking for review.

## Anti-patterns in updates and penalties

Anti-patterns after a traffic loss are reactions that feel decisive and make recovery slower.

| Do not | Do this instead |
|---|---|
| Filing a reconsideration request for an algorithmic drop | file one only when the Manual actions report lists an action; a spam or core demotion has no request |
| Deleting content in bulk straight after an update | assess it first; deletion is a last resort and pages that held should stay |
| Sending a request after a partial fix | fix every affected page first, because a partial fix earns no partial return |
| Promising a date for recovery | give the measurement date instead; Google guarantees no recovery |
| Trusting third-party "penalty checker" scores | use Search Console's two reports and the dashboard dates, which are the evidence |

## References for updates and penalties

The reference files below hold the detail for this skill; open one only when the task needs it.

- [references/spam-policies.md](references/spam-policies.md): every Google spam policy with how to check a site for
  it, and the common hack patterns.
- [references/reconsideration-request.md](references/reconsideration-request.md): a reconsideration request template
  with a filled example.

## See also for updates and penalties

- `seo-measurement`: the traffic-drop steps for a drop that matches no update
- `search-console`: daily exports and Page indexing reasons
- `link-building`: unnatural-link manual actions and disavow
- `content-briefs`: the people-first questions for assessing affected pages
- `crawling-and-indexing`: removals, status codes and fetching as Googlebot
- `programmatic-seo`: cleaning up scaled pages
