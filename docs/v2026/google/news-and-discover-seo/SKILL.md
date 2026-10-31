---
name: news-and-discover-seo
description: 'Grows publisher traffic from Google Discover, Top Stories and Google News: how eligibility works without applying, Publisher Center, preferred sources, article pages with dates, bylines and transparency, news sitemaps and NewsArticle markup, Discover images and max-image-preview, titles without clickbait, the February 2026 Discover core update, Discover and News manual actions, and the Discover and News reports. Use for a news site, blog or magazine that wants Discover or Top Stories traffic, when Discover traffic dropped, or when articles do not appear in Google News.'
metadata:
  tags:
  - seo
  - google-discover
  - google-news
  - top-stories
  - publishers
  - news-sitemap
---

# News, Top Stories and Discover SEO

Publishers get Google traffic from three places besides classic results: Top Stories (the news carousel in Search),
Google News (news.google.com and the app) and Discover (the feed on the Google app and Chrome's new tab page, shown
without a query). None needs an application: Google finds eligible content through normal crawling and indexing.
What decides visibility is timeliness, originality, trust and a page that follows Google's content policies.

## Step 0: read what the publication already has

Read the publication's state first, because the reports and sitemaps it already has show which surface sends traffic.
Check whether Search Console shows Performance › Discover and Performance › Google News at all, whether a Publisher
Center entry exists, and how many days a typical story keeps traffic. Then read one article and the files around it:

```bash
curl -s https://www.example.com/robots.txt | grep -iE '^sitemap:|googlebot-news'
curl -sL https://www.example.com/news/latest-story | grep -ioE '"@type": *"[A-Za-z]*Article"|max-image-preview:[a-z]+'
```

No news sitemap, an `Article` type where the page is news, or no `max-image-preview:large` each point to a section
below.

## Choose the surface: Top Stories, Google News or Discover

Top Stories, Google News and Discover reach readers in different ways, so choose which one a piece is written for.

| | Top Stories | Google News | Discover |
|---|---|---|---|
| Where it shows | news carousel in Search | news.google.com and the News app | feed in the Google app and Chrome's new tab page |
| What triggers it | a query about a current story | the reader's topics and sources | the reader's interests, with no query |
| Wins for | timely reporting people are searching for now | a publication with steady original news | a strong image and a clear title; timely stories, unique insight, evergreen explainers |
| Main levers | speed, original facts, clear dates, preferred sources | bylines, dates, publisher information, original reporting | an image 1200 px wide, `max-image-preview:large`, titles without clickbait |
| Report | Performance › Search results (counted under Web) | Performance › Google News | Performance › Discover |
| Loses when | the story is old or the page adds nothing new | transparency details are missing | the title withholds facts or the content is sensational |

Plan on search and direct readers first. Discover swings with interests and updates, so it suits a bonus rather than a
budget line.

## How eligibility works

Eligibility for Top Stories, Google News and Discover is automatic: a page must be indexed, meet Google's content
policies, and for news surfaces be news (timely reporting, analysis, opinion clearly labelled). There is no form to
submit. Google News Publisher Center lets a publisher manage how a publication is shown, but it does not make content
eligible and does not guarantee placement; Google News no longer uses RSS feeds or locations submitted there, it
builds publication pages automatically from crawled content.

## Article pages that news surfaces trust

An article page earns trust with facts a reader can check about who wrote it, when, and for whom. Google's News and
Discover policies list missing dates, bylines and publisher information as "transparency" violations.

- A clear headline in an `<h1>` that says what happened; the same headline in `<title>` and `og:title`.
- A visible byline linking to an author page with the author's role, background and other articles.
- A visible publication date and, when changed, an "Updated" date and time with time zone; the same values in
  `datePublished` and `dateModified`. Change the date only for a real update.
- An "About", "Contact" and editorial policy page that name the organisation, its owners and how corrections work.
- Original reporting or analysis: sources named and linked, quotes attributed, the story's own facts first.
- Labels for opinion, sponsored and AI-assisted content where readers expect them.

## NewsArticle markup and news sitemaps

Structured data and a news sitemap help Google read the facts of each article fast. Neither is required for
eligibility.

```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "City marathon publishes 2026 route with new river crossing",
  "image": ["https://www.example.com/img/marathon-route-16x9.jpg"],
  "datePublished": "2026-10-27T07:15:00+01:00",
  "dateModified": "2026-10-27T11:40:00+01:00",
  "author": [{"@type": "Person", "name": "Sam Lee", "url": "https://www.example.com/authors/sam-lee"}],
  "publisher": {"@id": "https://www.example.com/#organization"}
}
```

A news sitemap lists only articles published in the last two days, at most 1,000 per file, with `news:publication`
(name and language), `news:publication_date` and `news:title`; older articles stay in the normal sitemap. Generate it
from the CMS on publish, not on a schedule.

## Preferred sources in Top Stories and AI answers

Preferred sources let a reader pick sites they want to see more often in Top Stories; picked sites get a "preferred"
label and appear more often there and in a "From your sources" section. In October 2026 it works in every language
where Google Search runs. Since May 2026 the badge also shows in AI Overviews and AI Mode, for sites included in
Search generative AI features in Search Console. Only domains and subdomains can be chosen, not subfolders. It raises
the chance of appearing; it does not replace fresh, relevant coverage of the story the reader searched for.

Readers can be sent straight to your entry, though nothing requires it. Link to
`https://www.google.com/preferences/source?q=example.com` from an article, a newsletter or a social post, or add
Google's JavaScript button: load its library, then place a `div` with the `google-add-preferred-source-btn` attribute
(`data-theme` and `data-lang` are optional).

A Search profile gathers a publisher's site and social posts, and its followers are more likely to see them in
Discover; the `search-appearance` skill has the badge.

## Discover: images, titles and large previews

Discover chooses content for a person's interests and shows it as a large card, so the image and the title do most
of the work.

- **Image**: large, relevant and high quality; at least 1200 px wide, at least 300,000 pixels in total (1280×720
  works), 16:9 preferred. Not a logo, not a picture of text.
- **Large previews**: allow them with `<meta name="robots" content="max-image-preview:large">`; without it Discover
  can only show a small thumbnail.
- **Preferred image**: the main entity's `image` in markup or `og:image`; keep key details inside a landscape crop.
- **Title**: says what the article is about. No clickbait, no withheld key facts ("You won't believe..."), no outrage
  or morbid-curiosity hooks.
- **Freshness and depth**: timely stories, unique insight, well-told explainers; older evergreen pages can appear when
  still relevant.

Discover does not recommend some content at all: job applications, petitions, forms, code repositories, satire
without context, and content SafeSearch filters.

## The February 2026 Discover core update

The February 2026 Discover core update (5 to about 26 February 2026) was Google's first core update for Discover only;
classic Search ranking did not change with it. Google said it aimed to show more locally relevant content from sites
based in the reader's country and less sensational content and clickbait, and to favour original, in-depth and expert
content. Sites that lived on viral headlines or on foreign audiences lost the most. Recovery is the same as for any
core update: improve the content and titles, then judge over months.

## Discover and News policy violations

Google's content policies for News and Discover cover dangerous, deceptive, hateful, harassing, violent, sexually
explicit, manipulated-media and medically misleading content, misleading content, vulgar language, and transparency
(missing dates, bylines, publisher or contact information). A violation can bring a manual action shown in Search
Console › Manual actions as "News and Discover policy violation", which removes content from these surfaces but not
necessarily from Search. Fix it like any manual action and request a review.

## Measure Discover and News

Discover and News are measured in their own Search Console Performance reports, separate from Web search.

| Report | Shows | Note |
|---|---|---|
| Performance › Discover | impressions, clicks, CTR by page, country, device, date; includes Chrome | appears once the site passes a minimum of Discover impressions; 16 months |
| Performance › Google News | traffic from news.google.com and the News app | Top Stories inside Search count under Web |
| Performance › Search results, search appearance | Web results with features | AI features counted in Web totals |

Discover traffic swings with readers' interests and with updates even when nothing on the site changed. Treat it as a
bonus on top of search and direct readers, not as the base of a business plan.

## Worked example: Discover clicks fell 70% in February 2026

Situation: a UK site of celebrity and TV news lost 70% of Discover clicks between 5 and 26 February 2026; Web search
clicks were flat.

Diagnosis: no manual action; the dates match the Discover core update; Discover's page export shows the losses on
"you won't believe" headlines and on stories about US shows read mostly by US readers. Plan: rewrite headline
guidelines (say what happened, name the person, no withheld facts); cover more UK stories with original quotes; add
`max-image-preview:large` to the template (it was missing); add bylines with author pages. Check: Discover CTR and
clicks per article for six to eight weeks, compared with the same weeks before the update.

## Verify the article template and news sitemap

Publisher rules can be read from one live article and the news sitemap. The first command shows the preview setting
and the dates in markup; the script lists sitemap entries older than two days:

```bash
curl -sL https://www.example.com/news/marathon-route | grep -ioE 'max-image-preview:[a-z]+|"date(Published|Modified)"[^,}]*'
curl -sL https://www.example.com/news-sitemap.xml | python3 -c '
import datetime as dt, re, sys
xml = sys.stdin.read()
dates = re.findall(r"<news:publication_date>([^<]+)<", xml)
now = dt.datetime.now(dt.timezone.utc)
def age(d):
    when = dt.datetime.fromisoformat(d.strip().replace("Z", "+00:00"))
    return now - (when if when.tzinfo else when.replace(tzinfo=dt.timezone.utc))
print(len(dates), "entries;", sum(age(d) > dt.timedelta(days=2) for d in dates), "older than two days; limit 1,000")'
```

Expect `max-image-preview:large`, both dates with a time zone, and no old entries. Then open the article: byline,
publisher and date are visible and match the markup, and the preferred image is at least 1200 px wide. Search Console
› Manual actions stays empty, and Discover, News and Web are read separately for six to eight weeks after a change.

## Checklist for publishers

The checklist runs on the article template and the site's trust pages.

1. Article pages indexed; headline, byline, dates and publisher visible and in `NewsArticle` markup.
2. `max-image-preview:large` on articles; a 1200 px wide or larger preferred image on every article.
3. News sitemap generated on publish with the last two days only.
4. About, contact, editorial and corrections policies published and linked from every article.
5. Headline guidelines that forbid clickbait; opinion and sponsored labels in place.
6. Discover, News and Web performance read separately every week.

## Gotchas for news and Discover

The gotchas below cost publishers the most traffic.

1. **No `max-image-preview:large`.** Symptom: Discover clicks are low while impressions look normal. Cause: Discover
   can only show a small image, so CTR collapses. Fix: add it to the article template.
2. **Clickbait titles.** Symptom: a spike of clicks, then less Discover reach and possible policy action. Cause: the
   headline withholds the facts or oversells them. Fix: say what happened and name the subject.
3. **Fake freshness.** Symptom: articles keep a new date and lose trust. Cause: `dateModified` changes without an
   update, and readers and Google notice. Fix: change the date only for a real update.
4. **Logo as the article image.** Symptom: the card shows a logo, or the article never appears. Cause: Discover shows
   the logo or skips the article. Fix: set a large, relevant image for each story.
5. **Treating Publisher Center as an application.** Symptom: a publisher waits for approval that never arrives. Cause:
   Publisher Center manages display; eligibility comes from crawling and policy. Fix: work on the article pages and
   policies.
6. **Planning on Discover.** Symptom: a good month sets a budget and the next month misses it. Cause: Discover is
   volatile by design. Fix: keep search, newsletters and direct readers as the base.
7. **Republishing wire copy as your own.** Symptom: agency text never ranks, or the original outranks it. Cause:
   syndicated text competes with the original. Fix: add reporting, or block indexing of your copy with `noindex`.

## Anti-patterns in news and Discover

Anti-patterns in publishing chase a spike and pay for it in trust.

| Do not | Do this instead |
|---|---|
| Submitting an RSS feed to Google News | rely on crawling, since Google News no longer uses feeds submitted there |
| Leaving old stories in the news sitemap | keep the last two days only and move older ones to the normal sitemap |
| Generating the news sitemap on a schedule | generate it on publish |
| Hiding who runs the site | publish about, contact and corrections pages and link them from articles |
| Expecting a preferred source button to replace coverage | use it as a small extra; fresh, relevant coverage still decides |

## See also for news and Discover

- `structured-data`: `NewsArticle` and the wider markup rules
- `google-rich-results`: what Google shows for it
- `xml-sitemaps`: news sitemap format
- `search-appearance`: titles, dates and the Search profile badge
- `image-and-video-seo`: preferred images
- `algorithm-updates-and-penalties`: core updates and manual actions
