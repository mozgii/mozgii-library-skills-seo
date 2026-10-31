---
name: image-and-video-seo
description: 'Gets images and videos found and shown in Google Images, Lens, video results, Discover and AI answers: img markup Google indexes, formats, file names, alt text, preferred image, image sitemaps and CDNs, image licence metadata, video watch pages, thumbnails, VideoObject, key moments, the Video indexing report, YouTube against self-hosting. Use when images or videos do not show in search, Search Console says no video indexed or Video is not the main content, when writing alt text, or when planning video for SEO.'
metadata:
  tags:
  - seo
  - image-seo
  - video-seo
  - alt-text
  - google-images
  - videoobject
---

# Image and video SEO

Images and videos rank in their own results (Google Images, Lens, the Videos tab and video results), appear as
thumbnails in Search, Discover and AI answers, and make the page they sit on more useful. Search engines understand
them from the HTML around them, the file and the markup, so most of the work is plain markup done every time.

## Step 0: read how the site serves images and video

Read one page of each template first, because lazy-loading scripts, CDN hosts and video players decide most of what
search engines can reach.

```bash
curl -sL https://www.example.com/guides/waterproofing/ | grep -ioE '<img [^>]*>' | head -5
curl -sL https://www.example.com/guides/waterproofing/ | grep -ioE '<video[^>]*>|youtube\.com/embed/[^"]*|"@type": *"VideoObject"'
curl -s https://cdn.example.com/robots.txt | grep -iE '^(user-agent|disallow):'
curl -s https://www.example.com/sitemap.xml | grep -o '<image:image>' | wc -l
```

Images on a CDN host follow that host's robots.txt, not the main site's. Then read Search Console: Performance with the
Image and Video search types, and the Video indexing report if it shows. Note who controls the CDN and the player.

## Images Google can index

To make an image indexable, put it in an `<img>` element with a real `src`; Google does not index CSS background
images.

```html
<figure>
  <img src="https://cdn.example.com/img/trail-shoe-rock-plate-cutaway.avif"
       srcset="https://cdn.example.com/img/trail-shoe-rock-plate-cutaway-800.avif 800w,
               https://cdn.example.com/img/trail-shoe-rock-plate-cutaway-1600.avif 1600w"
       sizes="(max-width: 800px) 100vw, 800px"
       width="1600" height="900" loading="lazy"
       alt="Cutaway of a trail shoe showing the rock plate between midsole and outsole">
  <figcaption>The rock plate spreads the load of sharp stones.</figcaption>
</figure>
```

- `<picture>` and `srcset` are fine; always keep a fallback `src` on the `<img>`.
- Formats Google indexes: BMP, GIF, JPEG, PNG, WebP, SVG and AVIF; the file extension must match the real type.
- Short descriptive file names with hyphens (`trail-shoe-rock-plate-cutaway.avif`, never `IMG_4021.jpg`); translate
  them on localised pages.
- Keep one URL per image across pages so it is fetched and cached once.
- `loading="lazy"` below the fold only; the main (LCP) image loads eagerly with `fetchpriority="high"`.
- Place the image next to the text that discusses it; a caption is read by people and engines.
- Blocking `Googlebot-Image` in robots.txt removes images from Google Images and from image features in Search.

## Alt text that works

Alt text is the most important image attribute for search and the only one screen readers use. Write what the image
shows and why it is on this page, in about 5–15 words.

| Image | Alt |
|---|---|
| product photo | `alt="Runner X trail shoe in blue, side view"` |
| diagram | `alt="Diagram: the three lacing methods for downhill running"` |
| image used as a link | the link's destination: `alt="Trail running shoes"` |
| decorative divider or background | `alt=""` (empty, so screen readers skip it) |

Use the page's phrase only when the image shows it; a keyword list in `alt` is keyword stuffing. Text inside an image
(a price, a chart value) must also be in the HTML. For inline SVG, put a `<title>` element inside it.

## Choose the image Google shows for a page

The preferred image is the one Google uses as the page's thumbnail in Search, Discover and AI answers. Declare it in
markup (`primaryImageOfPage`, or the `image` of the page's main entity) and in `og:image`, and use the same image in
both. Choose a large, relevant image with a normal aspect ratio; not a logo, not a picture of text. For Discover and
large previews, it should be at least 1200 px wide and the page should allow `max-image-preview:large`.

## Image sitemaps and CDNs

An image sitemap lists images Google might not find otherwise, such as images loaded by JavaScript. It may list image
URLs on another host (a CDN); verify the CDN host in Search Console when you can. Only `image:loc` is used.

```xml
<url>
  <loc>https://www.example.com/shoes/runner-x</loc>
  <image:image><image:loc>https://cdn.example.com/img/runner-x-side.avif</image:loc></image:image>
</url>
```

## Image licence and credit metadata

Image metadata tells Google Images who made an image and how to licence it, and can show a "Licensable" badge. Use
`ImageObject` structured data with `contentUrl`, `license`, `acquireLicensePage`, `creator`, `creditText` and
`copyrightNotice`, or embed the same facts as IPTC photo metadata in the file. Details and a template:
[references/image-and-video-details.md](references/image-and-video-details.md).

## Video watch pages

A video is indexed for video features only on a watch page: a page whose main purpose is that one video. The watch
page must be indexed itself first. A video in a sidebar, under a long article or in a gallery of ten is "not the main
content" and is usually skipped.

- One watch page per video: the player near the top, a title, a description and a transcript in the HTML.
- The video loads without a click on a JavaScript cover, a login or a consent wall the crawler cannot pass.
- `VideoObject` structured data with `name`, `thumbnailUrl`, `uploadDate`, and `contentUrl` (the file) or
  `embedUrl` (the player); `duration` and `description` when known.
- Google must be able to fetch the video file to show previews and key moments: stable file URLs, not blocked by
  robots.txt or `noindex`, and enough server capacity.
- Remove a video by returning 404 for the watch page, `noindex`, or an accurate `expires` date.

## Thumbnails and key moments

Video features need a thumbnail and, for key moments, chapter data.

- Thumbnail: a stable URL Googlebot can fetch, at least 60×30 px (larger is better), mostly opaque, in BMP, GIF,
  JPEG, PNG, WebP, SVG or AVIF; use the same URL in `poster`, the sitemap, structured data and `og:image`.
- Key moments: `Clip` structured data with start and end times and labels (all languages), or `SeekToAction` to tell
  Google how your timestamp URLs work (a limited set of languages). On YouTube, timestamps and labels in the
  description do the same.
- Live streams: `BroadcastEvent` marks a video as live for the LIVE badge.
- `nosnippet` opts the page out of key moments and video previews.

## YouTube or self-hosted video

YouTube videos rank on YouTube's watch page; the same video embedded on your page can also be indexed for your page.
Both are fine. Choose by goal:

| Goal | Default |
|---|---|
| reach and discovery | YouTube, with chapters, a full description and a link to your page; embed it on a watch page of your site |
| traffic and conversions on your site | your own watch pages with `VideoObject`, transcript and your own player or a host that lets Google fetch the file |
| product and how-to pages | embed the video on the product or guide page anyway; it helps the page even if the video is not indexed there |

## Measure image and video search

Image and video results are measured in Search Console's Performance report: search type Image and search type
Video, plus the Video appearance filter under Web. Since September 2026 the Web report also has a Multimodal filter
for visits from Google Lens, Circle to Search and image uploads; it reports pages, not queries. The Video indexing
report (Indexing › Videos) lists watch pages with an indexed video and the reasons other videos were skipped.

## Worked example: "No video indexed" on 300 guide pages

Situation: a cookware brand embeds a 90-second video at the bottom of each of 300 recipe guides; the Video indexing
report says "Video isn't on a watch page" for 290 of them.

Diagnosis: each guide is a 2,000-word article with the video as an extra; that is not a watch page by Google's
definition. Fix, in order: keep the videos on the guides for readers; add `/videos/<slug>/` watch pages for the 40
videos with search demand ("how to season a carbon steel pan"), each with the player first, a transcript and
`VideoObject` with `Clip` chapters; link each guide to its watch page; add the watch pages to a video sitemap. Check:
the Video indexing report counts indexed watch pages over the next weeks; the Video search type gains impressions.

## Verify images and video on a template

Image rules can be checked from the served HTML, one page per template. This reports what a crawler that does not run
scripts can see:

```bash
curl -sL https://www.example.com/shoes/runner-x > page.html
python3 - page.html <<'EOF'
import sys
from html.parser import HTMLParser
class Media(HTMLParser):
    imgs = []
    other = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "img":
            self.imgs.append(a)
        elif tag in ("video", "iframe") or (tag == "meta" and a.get("property") == "og:image"):
            self.other.append((tag, a.get("src") or a.get("content") or a.get("poster")))
page = Media()
page.feed(open(sys.argv[1], encoding="utf-8", errors="replace").read())
for i, a in enumerate(page.imgs):
    src = a.get("src")
    flags = [name for name, bad in (("NO_SRC", not src), ("NO_ALT", "alt" not in a), ("NO_SIZE", not (a.get("width") and a.get("height"))),
                                    ("FIRST_IMAGE_LAZY", i == 0 and a.get("loading") == "lazy")) if bad]
    print(flags or "ok", src or a.get("data-src"))
print(page.other)
EOF
```

`NO_SRC` means a script must fill the image in, and crawlers may never see it; `FIRST_IMAGE_LAZY` needs a look when
that image is the LCP element. For video, the watch page must show a player in the rendered HTML: run URL Inspection ›
Test live URL and the Rich Results Test for `VideoObject`. Afterwards the Video indexing report shows the page as
indexed, and Search Console's Image and Video search types gain impressions over the following weeks.

## Checklist for images and video

The checklist runs per template.

1. Content images are `<img>` with `src`, width and height, a descriptive file name and alt text.
2. The LCP image loads eagerly; others lazy.
3. Each page declares one preferred image in markup and `og:image`, at least 1200 px wide where Discover matters.
4. Images and video files are not blocked by robots.txt; CDN image hosts listed in an image sitemap if needed.
5. Each video that should rank has a watch page with the video as main content, a transcript and `VideoObject`.
6. Thumbnails stable and identical across poster, markup and sitemap; key moments marked where videos are long.
7. Image, Video and Multimodal performance and the Video indexing report checked monthly.

## Gotchas with images and video

The gotchas below are why media does not show in search.

1. **CSS background images.** Symptom: product photos never appear in Google Images. Cause: Google does not index CSS
   background images. Fix: use an `<img>` element with a real `src`.
2. **Lazy loading by a script that swaps `data-src`.** Symptom: images are missing from the raw HTML and from image
   results. Cause: there is no `src` in the HTML, so crawlers may never see the image. Fix: keep a real `src`, or use
   native `loading="lazy"`.
3. **Video at the bottom of an article.** Symptom: the Video indexing report says the video is not on a watch page.
   Cause: a video under a long article is not a watch page, so there is no video result. Fix: give it a watch page of
   its own when it has demand.
4. **A click-to-load player.** Symptom: the page has a video for people and none in the report. Cause: the player is
   built from an image and JavaScript, and the crawler never sees a video. Fix: load the player in the page without a
   click.
5. **Changing image URLs on every deploy.** Symptom: images drop in image search after each release. Cause: a cache
   buster in the path means images are re-crawled and lose their history. Fix: use stable URLs.
6. **Alt text stuffed with keywords.** Symptom: alt text reads as a list of phrases. Cause: it is worse for
   accessibility and a spam signal. Fix: write what the image shows, in about 5–15 words.
7. **Stock photos as the preferred image.** Symptom: the thumbnail appears on hundreds of other results. Cause: the
   same image appears on hundreds of sites and says nothing. Fix: use an original, relevant image.

## Anti-patterns in image and video SEO

Anti-patterns with media treat the file as the whole job and forget the markup around it.

| Do not | Do this instead |
|---|---|
| Putting prices or chart values only inside an image | repeat that text in the HTML |
| Exporting every image at full size | serve modern formats through `srcset` at the sizes the layout uses |
| Showing ten videos on one page and expecting each to rank | give each video that should rank its own watch page |
| Mixing thumbnail URLs across poster, sitemap and markup | use one stable URL in all of them |
| Blocking `Googlebot-Image` to save crawl | keep it allowed, because blocking removes images from Google Images and image features |

## References for images and video

The reference files below hold the detail for this skill; open one only when the task needs it.

- [references/image-and-video-details.md](references/image-and-video-details.md): image licence metadata, the
  `ImageObject` and `VideoObject` templates with `Clip`, a video sitemap entry and the Video indexing report reasons.

## See also for image and video SEO

- `core-web-vitals`: the LCP image and layout shift from media
- `structured-data`: `VideoObject`, `ImageObject` and the wider markup rules
- `google-rich-results`: video features and the 2026 `VideoObject` properties
- `xml-sitemaps`: image and video sitemaps
- `news-and-discover-seo`: Discover image requirements
- `ecommerce-seo`: product photos and galleries
