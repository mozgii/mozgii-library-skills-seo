---
title: Core Web Vitals fixes with code
author: MOZGII, Inc.
lang: en
description: Concrete fixes for LCP, INP and CLS with HTML, CSS and JavaScript examples, ordered by how often each one solves the problem.
---

# Core Web Vitals fixes with code

These Core Web Vitals fixes are ordered by how often they solve each metric. Measure first: find the LCP element,
the slow interaction or the shifting element with field attribution or DevTools, then apply the matching fix.

## Contents

1. LCP: find the phase that is slow
2. LCP fixes
3. INP: find the slow interaction
4. INP fixes
5. CLS fixes
6. Third-party scripts

## LCP: find the phase that is slow

LCP splits into four phases, and each has different fixes: time to first byte, resource load delay (time until the
browser starts fetching the LCP resource), resource load duration, and element render delay. The DevTools
Performance panel and PageSpeed Insights show the split. A long load delay means the image is discovered late; a long
render delay means scripts or CSS block painting.

web.dev gives a healthy split, which shows where to look first:

| Phase | Healthy share of LCP |
|---|---|
| Time to first byte | about 40% |
| Resource load delay | under 10% |
| Resource load duration | about 40% |
| Element render delay | under 10% |

The two delays are the usual waste, and they should sit near zero. Fix the phase furthest over its share before
touching the others.

## LCP fixes

The LCP fixes below cover the four phases.

Make the LCP image discoverable and prioritised in the HTML:

```html
<img src="/img/hero-1200.avif" srcset="/img/hero-800.avif 800w, /img/hero-1200.avif 1200w"
     sizes="(max-width: 800px) 100vw, 1200px" width="1200" height="600"
     fetchpriority="high" alt="Runner on a rocky trail at sunrise">
```

Preload it when it comes from CSS or is chosen by JavaScript:

```html
<link rel="preload" as="image" href="/img/hero-1200.avif" fetchpriority="high">
```

- Do not put `loading="lazy"` on the LCP image; do not fade it in with JavaScript.
- Give `fetchpriority="low"` to images hidden at load (later carousel slides, menu promos); leave ordinary images
  without the attribute.
- Serve AVIF or WebP at the displayed size; compress; use a CDN close to users.
- Cut TTFB: cache HTML at the edge, use `stale-while-revalidate`, avoid redirects before the page.
- Inline critical CSS for the first screen and load the rest without blocking; add `defer` to scripts.
- Preconnect to a required third-party origin: `<link rel="preconnect" href="https://cdn.example.com">`.
- Render the main content on the server; client-rendered content waits for JavaScript.

## Speed up the next page with speculation rules

Speculation rules tell Chromium browsers to fetch or render a likely next page early, which cuts its LCP for that
visit. Start with prefetch on links people follow most:

```html
<script type="speculationrules">
{"prefetch": [{"where": {"href_matches": "/shoes/*"}, "eagerness": "moderate"}]}
</script>
```

`eagerness` is `immediate`, `eager`, `moderate` or `conservative`; the last two wait for a hover or the start of a
click. Move to `prerender` only for cheap, cached pages: it runs the page, so analytics, ads and anything with a side
effect must cope with a page nobody has seen yet. Never speculate on URLs that change state, such as a logout link.

## INP: find the slow interaction

INP reports the slowest typical interaction, so first find which one. The `web-vitals/attribution` build gives the
target element, the interaction type and the split into input delay, processing time and presentation delay. Long
input delay means the main thread was busy with other work; long processing means the handler itself is heavy; long
presentation means a large re-render or layout. The same build carries long animation frame data, which names the
script behind the delay:

```js
import { onINP } from "web-vitals/attribution";

onINP(({ value, attribution }) => {
  const { interactionTarget, inputDelay, processingDuration, presentationDelay, longestScript } = attribution;
  const script = longestScript?.entry;
  navigator.sendBeacon("/rum", JSON.stringify({
    inp: value, target: interactionTarget, inputDelay, processingDuration, presentationDelay,
    scriptUrl: script?.sourceURL, scriptFunction: script?.sourceFunctionName,
  }));
});
```

For presentation delay, sum `styleDuration` and `layoutDuration` across `attribution.longAnimationFrameEntries`. High
style time points to broad selectors or wide style invalidation; high layout time points to DOM size and geometry.

## INP fixes

The INP fixes below shorten each part of an interaction.

Yield to the main thread so the browser can paint the response before the heavy work:

```js
async function onFilterChange(event) {
  showSpinner();                                   // visible feedback in the next frame
  await (globalThis.scheduler?.yield?.() ?? new Promise((r) => setTimeout(r, 0)));
  applyFilters(event.target.value);                // heavy work after the paint
}
```

- Split long tasks (over 50 ms) into chunks with `scheduler.yield()` or `setTimeout`.
- Debounce input handlers that run on every keystroke.
- Avoid reading layout (`offsetHeight`, `getBoundingClientRect`) after writing styles in the same handler.
- Keep the DOM small (Lighthouse's DOM size insight flags pages where it slows style and layout); virtualise long lists.
- In React, mark non-urgent updates with `startTransition` so input stays responsive.
- Move heavy computation to a Web Worker.

## CLS fixes

The CLS fixes below reserve space before content arrives.

```html
<img src="/img/card.webp" width="400" height="300" alt="Trail shoe sole close-up">
<div class="ad-slot" style="min-height: 250px"></div>
<iframe src="https://www.youtube-nocookie.com/embed/VIDEO_ID" style="aspect-ratio: 16 / 9; width: 100%"></iframe>
```

Web fonts cause shifts when the fallback has different metrics; match them:

```css
@font-face {
  font-family: "Brand Sans Fallback";
  src: local("Arial");
  size-adjust: 104%;
  ascent-override: 92%;
}
body { font-family: "Brand Sans", "Brand Sans Fallback", sans-serif; }
@font-face { font-family: "Brand Sans"; src: url(/fonts/brand.woff2) format("woff2"); font-display: swap; }
```

- Never insert banners, cookie bars or "app download" bars above existing content after load; overlay them or
  reserve their space.
- Animate with `transform` and `opacity`, not with `top`, `height` or `margin`.
- Pages restored from the back/forward cache do not shift; avoid `unload` handlers and `Cache-Control: no-store` on
  HTML that does not need them.

## Third-party scripts

Third-party scripts (tag managers, chat, analytics, A/B testing, ads) are the most common cause of poor INP and a
frequent cause of slow LCP. Keep an inventory with an owner and a purpose for each; load with `defer` or `async`, or
after user interaction (a chat widget loaded on first click); remove what nobody owns. Test the page with and without
them in DevTools (Network › block request URL) to see their cost.
