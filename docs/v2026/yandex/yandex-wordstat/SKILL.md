---
name: yandex-wordstat
description: 'Measures search demand in Yandex with Wordstat: exact and broad frequency, the operators that fix word form, stop words, word count and order, the Wordstat web tool, the Wordstat API, the Yandex Search API methods GetTop, GetDynamics and GetRegionsDistribution with their prices and quotas, a no-login script for broad and exact frequency with Yandex suggestions, and which numbers to ignore. Use for Вордстат, Wordstat, частотность, точная частотность, сбор семантики, спрос в Яндексе, demand in Russian, comparing word forms, or any Russian-language keyword number.'
metadata:
  tags:
  - seo
  - yandex
  - wordstat
  - keyword-research
  - russian
  - demand
---

# Yandex Wordstat

Wordstat (wordstat.yandex.ru) is the Yandex source of query frequency by region and device, and the number every Russian
keyword decision rests on. Read carelessly it misleads by an order of magnitude, because its default figure counts every
longer query that contains the words. This skill gets the right number from the right source. The general keyword
workflow belongs to `keyword-research`, and ranking in Yandex to `yandex-seo`.

## Step 0: read which Wordstat access the project has

Read the access first, because it decides the source: an API key or token gives regions and dates, and a script without
one gives a snapshot without them. The script needs Node 18 or later and no packages.

```bash
node --version                                                    # expect 18 or later
printenv YANDEX_API_KEY YANDEX_FOLDER_ID | wc -l                  # 2 means the Search API is ready; values stay hidden
node scripts/demand.mjs --help
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

Then note the regions the business sells in, and whether a Yandex ID with Wordstat access exists for checks by hand.

## Choose the Wordstat source

Each source below answers the same question with different limits, and only some carry regions. The table's first row
is the reference number for decisions.

| Source | Use it when | Why the others lose here |
|---|---|---|
| Wordstat web (wordstat.yandex.ru) | a number decides a main phrase, with its region | the free copy has no regions and no date; the APIs need setup |
| Yandex Search API, Wordstat methods | a repeatable pull of tops, dynamics or regions | the Wordstat API needs an application to Direct support |
| Wordstat API (`https://api.wordstat.yandex.net`) | you already hold Direct access and want the same data as the new Wordstat | the Search API is simpler to start with, but billed per 1,000 requests |
| `scripts/demand.mjs` (Bukvarix free copy plus Yandex suggestions) | a first pass over many phrases, with no login | all regions combined, and the snapshot date is not stated |
| Key Collector and paid suites | bulk collection by region as a regular job | paid, with manual setup |

Sources, access and limits in full: [references/wordstat.md](references/wordstat.md).

## Exact and broad frequency in Wordstat

For decisions use **exact** frequency: quotes plus `!` before every word, prepositions included
(`"!ремонт !квартир !под !ключ"`). Broad frequency counts every longer query containing the words and can overstate demand
by an order of magnitude.

| Operator | Fixes | Example |
|---|---|---|
| `!word` | the word form (case, number, tense) | `купить !диван` |
| `+word` | a stop word (preposition, pronoun) | `работа +на дому` |
| `"..."` | the number of words (order may vary) | `"купить диван"` |
| `[...]` | the word order | `билеты [из москвы в казань]` |
| `-word` | excludes a word | `доставка -цветы` |
| `(a\|b)` | alternatives | `заказать (суши\|пиццу)` |

## Official Wordstat APIs

Two official APIs read Wordstat: the Wordstat API (an OAuth token and a connection request through Yandex Direct support),
and the Yandex Search API with its `GetTop`, `GetDynamics` and `GetRegionsDistribution` methods (an API key, billed per
1,000 requests). The Search API needs no application to Direct support:

```bash
curl -s -X POST https://searchapi.api.cloud.yandex.net/v2/wordstat/topRequests \
  -H "Authorization: Api-key $YANDEX_API_KEY" -H 'Content-Type: application/json' \
  -d '{"phrase":"ремонт квартир","numPhrases":100,"regions":["213"],"folderId":"'"$YANDEX_FOLDER_ID"'"}'
```

Roles, every method, prices and quotas: [references/wordstat.md](references/wordstat.md).

## Demand script without a login

The demand script looks up broad and exact frequency through a free Wordstat copy and adds Yandex suggestions, with
caching and backoff. Each request goes over https, and the script refuses a redirect to any other scheme, so a phrase
never crosses the network in the clear. Bukvarix and Yandex still receive every phrase they answer, so leave
unannounced product names out:

```bash
node scripts/demand.mjs "ремонт квартир под ключ" "ремонт квартиры цена"
node scripts/demand.mjs --file phrases.txt --out demand.tsv
node scripts/demand.mjs --expand "ремонт квартир" --expand "дизайн интерьера" --top 30 --out candidates.tsv
```

Columns: `level` (strong, some, weak, none), `exact`, `broad`, `as` (the stored form when the phrase is held in
another word form or order), `position` and `offered` (suggestion evidence), `signal` for expanded candidates. Confirm
by hand in Wordstat every number that decides a main phrase, with the target regions: the free copy has no regions and
no date.

## Worked example: choosing the main phrase for a renovation page

Situation: a Moscow renovation firm must choose a main phrase for its service page, between three wordings.

The first pass needs no login:

```bash
node scripts/demand.mjs "ремонт квартир под ключ" "ремонт квартиры под ключ" "отделка квартир под ключ" --out demand.tsv
```

The broad column looks strong for all three, so it is ignored. The `exact` and `level` columns put two wordings on top, and
the suggestion columns show people typing the first form. That is a candidate, not a decision: the file has no regions.
So the two leaders go into Wordstat by hand, as `"!ремонт !квартир !под !ключ"` and `"!ремонт !квартиры !под !ключ"`, with
the region set to Moscow, and the winner is recorded with its source, region and month.

Check: the plan row reads phrase, exact frequency, region 213, month, source; a second person repeats the search and gets
the same figure within the month.

## Verify a Wordstat number

A number counts once it has its operators, its region and its date. These commands confirm the script and the Search API
answer as expected:

```bash
node scripts/demand.mjs "ремонт квартир под ключ" --json | head -20                 # exact and broad both present
curl -s -X POST https://searchapi.api.cloud.yandex.net/v2/wordstat/topRequests \
  -H "Authorization: Api-key $YANDEX_API_KEY" -H 'Content-Type: application/json' \
  -d '{"phrase":"ремонт квартир","numPhrases":5,"regions":["213"],"folderId":"'"$YANDEX_FOLDER_ID"'"}' \
| python3 -c "import json,sys; r=json.load(sys.stdin); print(r['totalCount'], len(r['results']))"
```

A fake `fetch` proves the demand script's redirect refusal with no network: it answers every request with a redirect to
each address below. It needs Node 20.6 or later for `--import`. Expect `refused` in the `error` column, exit code 1, and
no `LEAK` line:

```bash
fake='data:text/javascript,globalThis.fetch=async(u)=>{if(new URL(u).protocol!=="https:")console.log("LEAK",String(u));return new Response(null,{status:302,headers:{location:process.env.TO}})}'
for TO in http://example.com/ ftp://example.com/ HTTP://example.com/; do
  TO="$TO" node --import "$fake" scripts/demand.mjs "проверка" --no-suggest --cache "$(mktemp -d)/c.json"
done
```

1. Each number in the plan names its source, region and month.
2. Exact frequency is below broad for the same phrase.
3. The figure that decides a main phrase was read in Wordstat itself.

## Checklist for Wordstat numbers

The checklist runs before a phrase list goes to writers.

1. Every main phrase has exact frequency, in the target regions.
2. Operators written in full, prepositions included.
3. Word forms and Cyrillic and Latin spellings compared.
4. Script output confirmed by hand for each number that decides a page.
5. Sources and dates recorded next to the numbers.
6. No API key in the repository, logs or tickets.

## Gotchas in Wordstat

The gotchas below produce numbers that look right and are not.

1. **Planning on broad Wordstat frequency.** Symptom: thousands of "searches" bring tens of visits. Cause: broad
   frequency counts every longer query containing the words. Fix: use exact frequency.
2. **Free Wordstat copy rate limit.** Symptom: HTTP 429 after about 30 fast requests. Cause: the free service limits
   bursts; the script waits 30 s, retries and caches. Fix: do not run it in parallel.
3. **Latin spelling of a term.** Symptom: a page misses demand that a rival takes. Cause: the Cyrillic form has the
   demand («AI агент» against «ИИ-агент»). Fix: compare exact frequency of both forms.
4. **Quotes without `!`.** Symptom: a "precise" number is still high. Cause: quotes fix the number of words, and Yandex
   still matches all word forms. Fix: add `!` to every word.
5. **A dropped preposition.** Symptom: the exact figure counts a different query. Cause: stop words were left out of the
   operators. Fix: put `!` on prepositions too.
6. **`refused a non-https address` in the error column.** Symptom: the phrase has no numbers and the script exits 1. Cause: the
   service redirected to an address without https, and the script stops rather than send the phrase in the clear. Fix:
   rerun later, or take the number from Wordstat web or the Search API; never change the script to follow it.
7. **A zero in the script for a real phrase.** Symptom: the phrase shows no demand, and the `as` column holds another form.
   Cause: the copy stores it in another word form or order. Fix: read the `as` column before reporting zero.
8. **Weekly dynamics refuse an operator.** Symptom: `GetDynamics` rejects a phrase or gives odd weekly data. Cause: weekly
   and monthly data accept only `+`, and every operator works only for daily data. Fix: use daily data for exact phrases.

## Anti-patterns in Wordstat

Anti-patterns here treat any number from a tool as demand.

| Do not | Do this instead |
|---|---|
| Choosing a main phrase on the free copy alone | confirm it in Wordstat with the target regions |
| Quoting a number without its operators | write the full operator string next to it |
| Scraping Wordstat or the results page | use the APIs, or the script's free copy |
| Trusting keyword difficulty from tools built on Google data | read Yandex's own results; such scores are weak for Yandex |
| Chasing positions for zero-demand phrases | they rank because nobody competes, and bring nothing |

## References for Wordstat

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/wordstat.md](references/wordstat.md): Wordstat operators, demand and position sources for Yandex,
  what to ignore.
- `scripts/demand.mjs`: demand lookup and seed expansion without a login (cache in `.seo-cache/`).

## See also for Wordstat

- `keyword-research`: the general keyword workflow
- `yandex-seo`: Yandex Webmaster, regions and filters
- `russian-language-seo`: writing the text around the phrase
- `seo-measurement`: whether the chosen phrase later brought traffic
