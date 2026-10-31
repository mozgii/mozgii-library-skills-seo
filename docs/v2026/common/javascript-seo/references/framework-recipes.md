---
title: JavaScript framework recipes for SEO
author: MOZGII, Inc.
lang: en
description: Where metadata, canonical tags, sitemaps, robots.txt and 404 status codes go in Next.js, Nuxt, SvelteKit, Astro, React Router and client-only apps, and how single-page apps are measured for Core Web Vitals.
---

# JavaScript framework recipes for SEO

Each framework below has a server-side way to set the title, description, canonical and status code of a page. Use
it instead of setting them in the browser. Read the installed version first (`npm ls next nuxt @sveltejs/kit astro
react-router`), because the shapes below match the current majors in October 2026: Next.js 16, Nuxt 4, SvelteKit 3,
Astro 7 and React Router 8.

## Contents

1. Next.js App Router
2. Nuxt
3. SvelteKit
4. Astro
5. React Router framework mode
6. Client-only apps
7. Single-page apps and Core Web Vitals

## Next.js App Router metadata, sitemap and 404

Next.js App Router renders on the server by default; metadata comes from `generateMetadata`, sitemaps and robots.txt
from route files. Set `metadataBase` once in the root layout so relative canonicals become absolute.

```tsx
// app/layout.tsx
export const metadata = { metadataBase: new URL("https://www.example.com") };

// app/shoes/[slug]/page.tsx
import type { Metadata } from "next";
import { notFound } from "next/navigation";

type Props = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const product = await getProduct(slug);
  if (!product) return {};
  return {
    title: `${product.name} trail shoe`,
    description: product.summary,
    alternates: { canonical: `/shoes/${slug}` },
  };
}

export default async function Page({ params }: Props) {
  const { slug } = await params;
  const product = await getProduct(slug);
  if (!product) notFound();          // 404 status when called before streaming starts
  return <ProductView product={product} />;
}
```

When `notFound()` runs after the response has started streaming, the status is already 200; Next.js then adds a
`noindex` robots tag instead. Call it at the top of the page, before any `Suspense` boundary that streams.

Next.js can also stream metadata: when `generateMetadata` depends on request data, the tags arrive in `<body>` after
the first HTML. Googlebot reads them, and crawlers on the `htmlLimitedBots` list get them in `<head>`. A crawler outside
that list that runs no JavaScript gets the page with no metadata in the head, so check the raw HTML with its user agent,
or set `htmlLimitedBots: /.*/` to turn streaming off at the cost of a slower first byte.

```ts
// app/sitemap.ts
import type { MetadataRoute } from "next";
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const products = await listPublishedProducts();
  return products.map((p) => ({ url: `https://www.example.com/shoes/${p.slug}`, lastModified: p.updatedAt }));
}

// app/robots.ts
import type { MetadataRoute } from "next";
export default function robots(): MetadataRoute.Robots {
  return { rules: { userAgent: "*", disallow: ["/cart/"] }, sitemap: "https://www.example.com/sitemap.xml" };
}
```

Pages Router equivalents: `next/head` for tags, `getServerSideProps` or `getStaticProps` returning `{ notFound: true }`
for a 404.

## Nuxt metadata and 404

Nuxt renders on the server by default (`ssr: true`); keep it on for indexable routes and use `routeRules` for
prerendering or regeneration per path.

```ts
// pages/shoes/[slug].vue, inside <script setup lang="ts">
const route = useRoute();
const { data: product } = await useFetch(`/api/products/${route.params.slug}`);
if (!product.value) {
  throw createError({ status: 404, statusText: "Product not found", fatal: true });
}
useSeoMeta({ title: `${product.value.name} trail shoe`, description: product.value.summary });
useHead({ link: [{ rel: "canonical", href: `https://www.example.com/shoes/${product.value.slug}` }] });
```

## SvelteKit metadata and 404

SvelteKit renders on the server unless a route sets `export const ssr = false`; never set that on an indexable route.

```ts
// src/routes/shoes/[slug]/+page.server.ts
import { error } from "@sveltejs/kit";
export async function load({ params }) {
  const product = await getProduct(params.slug);
  if (!product) error(404, "Product not found");
  return { product };
}
```

```svelte
<!-- src/routes/shoes/[slug]/+page.svelte -->
<script lang="ts">
  let { data } = $props();
</script>

<svelte:head>
  <title>{data.product.name} trail shoe</title>
  <meta name="description" content={data.product.summary} />
  <link rel="canonical" href={`https://www.example.com/shoes/${data.product.slug}`} />
</svelte:head>
```

## Astro metadata and 404

Astro builds static HTML by default and ships JavaScript only for interactive islands, so content is in the HTML
without extra work. Put title, description and canonical in a shared layout fed by page props; `src/pages/404.astro`
becomes the not-found page that hosts serve with status 404; the `@astrojs/sitemap` integration builds the sitemap
once `site` is set in `astro.config`.

## React Router framework mode metadata and 404

React Router 8 in framework mode (the former Remix) renders on the server; loaders can throw a status. Its `meta`
function receives `loaderData`; the older `data` argument is gone.

```ts
// app/routes/shoe.tsx
import { data } from "react-router";
import type { Route } from "./+types/shoe";

export async function loader({ params }: Route.LoaderArgs) {
  const product = await getProduct(params.slug);
  if (!product) throw data(null, { status: 404 });
  return { product };
}

export function meta({ loaderData }: Route.MetaArgs) {
  if (!loaderData) return [{ title: "Not found" }];
  return [
    { title: `${loaderData.product.name} trail shoe` },
    { name: "description", content: loaderData.product.summary },
    { tagName: "link", rel: "canonical", href: `https://www.example.com/shoes/${loaderData.product.slug}` },
  ];
}
```

## Client-only apps

A client-only app (Create React App style, a Vite SPA, an Angular app without SSR) has three options, best first:

1. Move indexable routes to a framework with server rendering (Next.js, Nuxt, SvelteKit, React Router framework mode,
   Angular SSR).
2. Prerender indexable routes to static HTML at build time, so each route has its own HTML file.
3. Keep the app client-only and accept that Google may index it late and other engines poorly; keep marketing and
   content pages on a static site beside it.

## Single-page apps and Core Web Vitals

A single-page app changes views without full page loads ("soft navigations"). Core Web Vitals in CrUX and Search
Console have counted only full page loads, so LCP and CLS of later views were missing and INP of a long session was
attributed to the first URL. Chrome's Soft Navigations API (Chrome 151) let CrUX publish experimental soft-navigation
versions of LCP, INP and CLS in 2026, in BigQuery and the CrUX APIs, and `web-vitals` 6 reports them from your own
users with `reportSoftNavs: true`. They are experimental: read them for SPA diagnosis, not as the numbers Search
Console reports. Most origins have few soft navigations, so most sites see little change.
