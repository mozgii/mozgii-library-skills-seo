---
name: core-web-vitals
description: 'Measures and improves Core Web Vitals and page experience for search: LCP, INP (which replaced FID in March 2024) and CLS thresholds at the 75th percentile, field data from CrUX, PageSpeed Insights and Search Console, lab data from Lighthouse and DevTools, real-user monitoring with the web-vitals library, agent-run traces with Chrome DevTools MCP, and the fixes that move each metric. Use when Search Console shows Poor or Need improvement URLs, when a page is slow, when asked about page speed and rankings, or before shipping a heavy template.'
metadata:
  tags:
  - seo
  - core-web-vitals
  - lcp
  - inp
  - cls
  - page-speed
  - performance
---

# Core Web Vitals and page experience

Core Web Vitals are three metrics of real users' experience that Google uses as part of its page experience signals:
loading (LCP), responsiveness (INP) and visual stability (CLS). They matter for rankings mainly as a tie-breaker
between pages of similar relevance, and much more for conversions. Content relevance always comes first.

## Step 0: read what the project runs

Read the installed versions first, because attribution fields and soft-navigation support depend on them. The code
here targets `web-vitals` 6 and Lighthouse 13.

```bash
npm ls web-vitals lighthouse chrome-devtools-mcp 2>/dev/null
```

Upgrading `web-vitals` from 5 to 6: import types with `import type`; `includeProcessedEventEntries` on `onINP` now
defaults to false; reports can arrive more often with `reportAllChanges`, since idle callbacks are capped at 1 second.

## Metrics and thresholds

Core Web Vitals thresholds apply at the 75th percentile of page loads, separately for mobile and desktop. A URL group
passes when all three metrics are good.

| Metric | Measures | Good | Needs improvement | Poor |
|---|---|---|---|---|
| Largest Contentful Paint (LCP) | when the biggest image or text block in the viewport finishes painting | ≤ 2.5 s | 2.5–4.0 s | > 4.0 s |
| Interaction to Next Paint (INP) | the slowest typical delay from a tap, click or key press to the next frame | ≤ 200 ms | 200–500 ms | > 500 ms |
| Cumulative Layout Shift (CLS) | how much visible content moves unexpectedly | `≤ 0.1` | `0.1–0.25` | `> 0.25` |

FID is gone: INP replaced First Input Delay (FID) as a Core Web Vital on 12 March 2024. It is no longer reported, and
any guide or tool still optimising FID is out of date. Supporting metrics: TTFB (server response; good at 0.8 s or less, poor above
1.8 s) and FCP.

## Field data first, lab data second

Field data is what real Chrome users experienced over the last 28 days; it is what Google uses. Lab data is one
simulated load; it explains causes but is not the score.

| Source | Type | Use |
|---|---|---|
| Search Console › Core Web Vitals | field, grouped by similar URLs | which templates fail, and validation after a fix |
| PageSpeed Insights (pagespeed.web.dev) | field for URL and origin, plus a Lighthouse lab run | one URL's numbers and diagnostics |
| CrUX API and CrUX History API | field, per URL or origin; the History API returns up to 40 weekly periods (about 10 months), 25 by default, set with `collectionPeriodCount` | monitoring and reports |
| CrUX on BigQuery | field, monthly, per origin | market comparisons |
| Lighthouse, DevTools Performance panel | lab | finding the cause; both report insights such as LCP breakdown and CLS culprits; Lighthouse cannot measure INP (it reports TBT instead) |
| `web-vitals` library in your analytics | field, every user and browser that supports the metric | debugging real interactions with attribution |

CrUX only includes pages and origins with enough Chrome traffic; small sites may have no field data, in which case
monitor with your own real-user data.

## Read field data from the command line

The PageSpeed Insights API returns field and lab data for one URL. It works without a key at a low quota; add
`&key=$PSI_KEY` for regular use.

```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://www.example.com/&strategy=mobile&category=performance" \
| python3 -c "import json,sys; d=json.load(sys.stdin); m=d.get('loadingExperience',{}).get('metrics',{});
print({k: (v['percentile'], v['category']) for k,v in m.items()})"
```

`CUMULATIVE_LAYOUT_SHIFT_SCORE` is reported × 100 (`8` means 0.08). The CrUX API takes an origin or URL and a form
factor:

```bash
curl -s -X POST "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"origin": "https://www.example.com", "formFactor": "PHONE", "metrics": ["largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift"]}'
```

## Lab runs with Lighthouse

A Lighthouse lab run explains what slows one load; run it several times and take the median.

```bash
npx lighthouse https://www.example.com/ --only-categories=performance --form-factor=mobile \
  --output=json --output-path=./lh-home.json --chrome-flags="--headless=new"
```

Read the LCP element and its phases (TTFB, resource load delay, load time, render delay), render-blocking resources,
the main-thread long tasks, and the layout shift culprits.

## Let an agent read a trace with Chrome DevTools MCP

The `chrome-devtools-mcp` server gives a coding agent a real Chrome, so it can record a trace and read the insights a
person sees in the Performance panel. Add it to the agent's MCP settings:

```json
{"mcpServers": {"chrome-devtools": {"command": "npx", "args": ["-y", "chrome-devtools-mcp@latest"]}}}
```

| Step | Tool | What to read |
|---|---|---|
| Record a cold load | `performance_start_trace` with `reload: true`, `autoStop: true` | LCP, CLS and the insight set id |
| Explain it | `performance_analyze_insight` with `LCPBreakdown`, `LCPDiscovery`, `DocumentLatency`, `RenderBlocking` or `CLSCulprits` | the slow phase and the resource behind it |
| Find late files | `list_network_requests`, then `get_network_request` | start time and size of the LCP resource |
| Test a slow phone | `emulate` with `networkConditions: "Fast 3G"`, `cpuThrottlingRate: 4` | problems a fast laptop hides |

Insight names change between Chrome versions, so take them from the trace output. A trace is lab data: it finds causes,
and the field numbers still decide. Report only what was measured. A render-blocking warning with 0 ms of estimated
saving is a note and not a task; confirm a file is unused before removing it; name the file and its size ("hero.png,
450 KB"), not "optimise images"; and when LCP is 1.2 s and CLS is 0, say the page is fine.

## Real-user monitoring with web-vitals

The `web-vitals` library reports each metric from real users to your analytics, with attribution that names the
slow element or interaction.

```js
import { onLCP, onINP, onCLS } from "web-vitals/attribution";

function send(metric) {
  const body = JSON.stringify({ name: metric.name, value: metric.value, rating: metric.rating,
    id: metric.id, page: location.pathname, target: metric.attribution?.interactionTarget
      ?? metric.attribution?.target ?? metric.attribution?.largestShiftTarget });
  navigator.sendBeacon?.("/rum", body) || fetch("/rum", { body, method: "POST", keepalive: true });
}
onLCP(send); onINP(send); onCLS(send);
```

## Fixes that move each metric

The fixes below are ordered by how often they solve the problem. Full detail with code is in
[references/cwv-fixes.md](references/cwv-fixes.md).

**LCP.** Make the LCP image discoverable in the HTML (no lazy loading on it, `fetchpriority="high"`), serve it in a
modern format at the right size from a CDN, cut TTFB (caching, CDN, faster backend), remove render-blocking CSS and
synchronous scripts, and avoid client-side rendering of the main content.

**INP.** Break long tasks (over 50 ms) so input is handled quickly, yield to the main thread in heavy handlers, cut and
defer third-party scripts, keep the DOM small, and avoid layout thrashing in event handlers.

**CLS.** Set `width` and `height` (or `aspect-ratio`) on images, video and embeds; reserve space for ads and banners;
avoid inserting content above existing content; use `font-display` with metric-matched fallback fonts.

## Single-page apps and soft navigations

Single-page apps change views without a full page load ("soft navigations"), and Core Web Vitals in CrUX and Search
Console have counted only full loads. Chrome's Soft Navigations API (Chrome 151) let CrUX publish experimental
soft-navigation versions of LCP, INP and CLS in 2026, in BigQuery and the CrUX APIs. Use them to diagnose SPA views;
Search Console still reports the standard metrics.

`web-vitals` 6 reports the same views from your own users, in browsers that support the API:

```js
import { onLCP, onINP, onCLS } from "web-vitals/attribution";

onLCP(send, { reportSoftNavs: true });
onINP(send, { reportSoftNavs: true });
onCLS(send, { reportSoftNavs: true });
```

On a soft navigation TTFB reads 0, INP restarts for the new view, and elements that stay on screen between views are
not counted as paints, so LCP can differ from a full load of the same URL. Keep these values apart from full loads in
your reports.

## Page experience beyond Core Web Vitals

Page experience also covers HTTPS, a mobile-friendly layout, no intrusive interstitials (pop-ups covering the content
on arrival from search) and a clear main content area. Google retired the separate page experience report and the
Mobile-Friendly Test; these remain good practice and are checked in a normal audit.

## Worked example: product pages fail LCP on mobile

Situation: Search Console shows 6,200 product URLs "Poor" for LCP on mobile; field p75 is 4.6 s.

Lab run: the LCP element is the main product image; it is `loading="lazy"`, set by a gallery script after hydration,
from a 2,400 px JPEG; TTFB is 1.3 s because product HTML is not cached. Fix: render the first image as a plain `<img>`
in the server HTML with `fetchpriority="high"`, no lazy loading, AVIF at 800 and 1200 widths with `srcset`; cache
product HTML at the CDN for 5 minutes. Lab LCP falls to 1.9 s. Check: Validate fix in Search Console, and CrUX p75 for
the template after 28 days.

## Verify a Core Web Vitals fix

A fix is proven in two steps: the lab shows the change now, and field data confirms it for real users about 28 days
later. Run Lighthouse on the same URL and settings before and after, three times each, and compare the medians:

```bash
python3 -c "
import json
a = json.load(open('lh-home.json'))['audits']
print({k: round(a[k]['numericValue'], 3) for k in ('largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift')})"
```

LCP and total blocking time are in milliseconds. A lab run has no INP, so read total blocking time as the nearest
signal, then confirm INP in the field. After release, read field data for the URL:

```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://www.example.com/p/runner-x&strategy=mobile&category=performance" \
| python3 -c "import json,sys; m=json.load(sys.stdin).get('loadingExperience',{}).get('metrics',{});
print({k: (v['percentile'], v['category']) for k,v in m.items()})"
```

| Field metric at p75 | Passes when |
|---|---|
| `LARGEST_CONTENTFUL_PAINT_MS` | ≤ 2500 |
| `INTERACTION_TO_NEXT_PAINT` | ≤ 200 |
| `CUMULATIVE_LAYOUT_SHIFT_SCORE` | ≤ 10 (reported × 100) |

An empty result means the URL has too little traffic for field data: use the origin in the CrUX API, or Search Console's
group for that template. Then start Validate fix in the Search Console report, which watches the group for 28 days.

## Checklist for Core Web Vitals

The Core Web Vitals checklist confirms field data is read, causes are found and fixes are proven.

1. Search Console Core Web Vitals report read for mobile and desktop; failing groups mapped to templates.
2. Field numbers per template recorded (PSI or CrUX API), not only lab scores.
3. LCP element identified per template; it is in the HTML, not lazy loaded, sized and prioritised; the slowest LCP
   phase named.
4. INP: the slowest interactions found with web-vitals attribution or DevTools; long tasks split.
5. CLS: every image, embed and ad slot has reserved space.
6. After release, Search Console › Validate fix started; field data checked again after 28 days.

## Gotchas with Core Web Vitals

The gotchas below are why "we fixed it" often does not show in the report.

1. **Chasing the Lighthouse score.** Symptom: the score is 100 and Search Console still reports failures. Cause: a lab
   run is one simulated load, and Lighthouse does not measure INP. Fix: decide with field data.
2. **Expecting instant change.** Symptom: a shipped fix shows nothing in the report for days. Cause: field data is a
   28-day rolling window, so the report moves weeks after a fix. Fix: start Validate fix and read the numbers again
   after 28 days.
3. **Lazy loading the hero image.** Symptom: LCP is slow although the image file is small. Cause: `loading="lazy"` on
   the LCP image delays it. Fix: lazy load only below the fold.
4. **Fixing desktop while mobile fails.** Symptom: desktop turns green and the mobile group stays Poor. Cause: mobile
   is usually the failing form factor and the one Google indexes. Fix: read and fix the mobile group first.
5. **Third-party tags added after the fix.** Symptom: INP was good at release and regressed a month later. Cause: tag
   managers, chat widgets and A/B testing scripts are the most common INP regressions. Fix: budget them and review
   each new tag.
6. **Speed as the ranking fix.** Symptom: the pages pass and rankings stay flat. Cause: a fast page that does not
   answer the query still does not rank. Fix: treat speed as a tie-breaker and a conversion gain.
7. **Compressing the image when the delay is elsewhere.** Symptom: LCP does not move after a smaller hero ships.
   Cause: render delay was the slow phase, and the saved time just waits there. Fix: read the four phases first.

## Anti-patterns in Core Web Vitals

Anti-patterns in performance work optimise a number that no one in the field experiences.

| Do not | Do this instead |
|---|---|
| Reporting one lab run as the page's speed | run Lighthouse several times, take the median and report field numbers beside it |
| Optimising FID or reading old guides that do | work on INP and check the guide's date |
| Adding `fetchpriority="high"` to many images | give it to the one LCP image |
| Removing a file flagged as render-blocking without proof | confirm it is unused and that the estimated saving is above 0 ms |
| Mixing soft-navigation values with full loads in one report | keep them in separate series |

## References for Core Web Vitals

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/cwv-fixes.md](references/cwv-fixes.md): LCP, INP and CLS fixes with code.

## See also for Core Web Vitals

- `image-and-video-seo`: the LCP image in markup, formats and sizes
- `javascript-seo`: rendering choices and client-side content
- `seo-audit`: where page experience sits in a full audit
- `seo-measurement`: reporting Core Web Vitals pass rate as a health KPI
