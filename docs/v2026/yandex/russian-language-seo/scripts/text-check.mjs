#!/usr/bin/env node
// SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
// Copyright 2026 MOZGII, Inc. (https://mozgii.com/)
// Lints Russian search-facing text: anti-AI vocabulary, 168-ФЗ words, typography traps,
// heading case, metadata length, and the main phrase counted by lemma across the SEO zones.
// Usage: node text-check.mjs <file.md|file.txt> [--phrase "ремонт квартир под ключ"] [--max N]
// Exit: 0 pass (WARN lines allowed), 1 at least one FAIL, 2 usage error.
import { readFileSync } from "node:fs";

const USAGE = 'usage: node text-check.mjs <file> [--phrase "main phrase"] [--max N]';
const args = process.argv.slice(2);
const wantsHelp = args.some((a) => a === "--help" || a === "-h");
if (wantsHelp) {
  console.log(USAGE);
  process.exit(0);
}
const opts = {};
const positional = [];
const argCount = args.length;
for (let i = 0; i < argCount; i++) {
  if (args[i].startsWith("--")) opts[args[i]] = args[++i];
  else positional.push(args[i]);
}
const file = positional[0];
const opt = (name) => opts[name];
if (!file) {
  console.error(USAGE);
  process.exit(2);
}

let raw;
try {
  raw = readFileSync(file, "utf8");
} catch (e) {
  console.error(`cannot read ${file}: ${e.message}`);
  process.exit(2);
}

// ---------- Russian Snowball stemmer (lemma proxy) ----------
const PERFECTIVE = /((ив|ивши|ившись|ыв|ывши|ывшись)|((?<=[ая])(в|вши|вшись)))$/u;
const REFLEXIVE = /(с[яь])$/u;
const ADJECTIVE = /(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$/u;
const PARTICIPLE = /((ивш|ывш|ующ)|((?<=[ая])(ем|нн|вш|ющ|щ)))$/u;
const VERB = /((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю)|((?<=[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$/u;
const NOUN = /(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$/u;
const RV = /^(.*?[аеиоуыэюя])(.*)$/u;
const DERIVATIONAL = /[^аеиоуыэюя][аеиоуыэюя]+[^аеиоуыэюя]+[аеиоуыэюя].*(?<=о)сть?$/u;

export function stem(input) {
  const word = input.toLowerCase().replace(/ё/gu, "е");
  if (!/[а-я]/u.test(word)) return word;
  const m = word.match(RV);
  if (!m || !m[2]) return word;
  const pre = m[1];
  let rv = m[2];
  let tmp = rv.replace(PERFECTIVE, "");
  if (tmp === rv) {
    rv = rv.replace(REFLEXIVE, "");
    tmp = rv.replace(ADJECTIVE, "");
    if (tmp !== rv) rv = tmp.replace(PARTICIPLE, "");
    else {
      tmp = rv.replace(VERB, "");
      rv = tmp === rv ? rv.replace(NOUN, "") : tmp;
    }
  } else rv = tmp;
  rv = rv.replace(/и$/u, "");
  if (DERIVATIONAL.test(rv)) rv = rv.replace(/ость?$/u, "");
  tmp = rv.replace(/ь$/u, "");
  rv = tmp === rv ? rv.replace(/ейше?/u, "").replace(/нн$/u, "н") : tmp;
  return pre + rv;
}

// ---------- parsing ----------
let title;
let description;
let body = raw;
const fm = raw.match(/^---\n([\s\S]*?)\n---\n?/u);
if (fm) {
  body = raw.slice(fm[0].length);
  const field = (k) => {
    const line = fm[1].match(new RegExp(`^${k}:\\s*(.+)$`, "mu"));
    return line ? line[1].trim().replace(/^["']|["']$/gu, "") : undefined;
  };
  title = field("title");
  description = field("description");
}
const prose = body
  .replace(/```[\s\S]*?```/gu, " ")
  .replace(/`[^`]*`/gu, " ")
  .replace(/\]\([^)]*\)/gu, "]")
  .replace(/https?:\/\/\S+/gu, " ")
  .replace(/<[^>]+>/gu, " ");
const lines = prose.split("\n");
const headings = lines.filter((l) => /^#{1,6}\s/u.test(l)).map((l) => ({ level: l.match(/^#+/u)[0].length, text: l.replace(/^#+\s*/u, "").trim() }));
const h1 = headings.find((h) => h.level === 1)?.text;
const textOnly = lines.filter((l) => !/^#{1,6}\s/u.test(l)).join("\n");
const words = (s) => s.match(/[\p{L}\d]+(?:-[\p{L}\d]+)*/gu) ?? [];
const wordCount = words(textOnly).length;

const fails = [];
const warns = [];
const lineOf = (re) => {
  const out = [];
  raw.split("\n").forEach((l, i) => {
    if (re.test(l)) out.push(i + 1);
    re.lastIndex = 0;
  });
  return out.slice(0, 5).join(",");
};
const W = (s) => new RegExp(`(?<![\\p{L}])(?:${s})(?![\\p{L}])`, "giu");

function scan(list, sink, label) {
  for (const [pattern, hint] of list) {
    const re = W(pattern);
    const hits = prose.match(re);
    if (hits) sink.push(`${label}: «${hits[0]}» ×${hits.length} (lines ${lineOf(re)}) → ${hint}`);
  }
}

// ---------- anti-AI vocabulary (editing-passes.md) ----------
scan(
  [
    ["данн(?:ый|ая|ое|ого|ому|ом|ой|ую)", "этот / эта / это («данные, данных» = data are fine)"],
    ["явля(?:ется|ются|лся|лась|лось|лись|ющийся|ющаяся|ющиеся)", "restructure without the copula"],
    ["осуществл\\p{L}*", "the direct verb"],
    ["в рамках", "в / по / за"],
    ["ввиду того", "потому что / так как"],
    ["следует отметить", "state the fact"],
    ["необходимо (?:отметить|подчеркнуть)", "state the fact"],
    ["на сегодняшний день", "сейчас"],
    ["представляется возможным", "можно"],
    ["имплементир\\p{L}*", "внедрять"],
    ["верифицир\\p{L}*", "проверять"],
  ],
  fails,
  "FAIL chancellery",
);
scan(
  [
    ["функционир\\p{L}*", "работать"],
    ["таким образом", "итак / значит (as an opener)"],
    ["вместе с тем", "но / при этом"],
    ["целый ряд", "несколько / a number"],
    ["немаловажн\\p{L}*", "важный"],
    ["колоссальн\\p{L}*", "огромный"],
    ["в современном мире", "delete the opener; answer first"],
    ["не секрет, что", "delete the opener"],
    ["в этой статье мы", "delete; answer the query in the lead"],
    ["давайте разбер\\p{L}*", "delete the opener"],
  ],
  warns,
  "WARN AI phrasing",
);

// ---------- 168-ФЗ vocabulary (typography-and-register.md) ----------
scan(
  [
    ["софт\\p{L}*", "программа / ПО"],
    ["фикс-прайс\\p{L}*", "фиксированная цена"],
    ["дедлайн\\p{L}*", "срок"],
    ["фидб[эе]к\\p{L}*", "отзыв / обратная связь"],
    ["саппорт\\p{L}*", "поддержка"],
    ["лендинг\\p{L}*", "страница / сайт"],
    ["онбординг\\p{L}*", "запуск / ввод в работу"],
    ["дашборд\\p{L}*", "панель"],
    ["воркфлоу", "процесс"],
    ["апдейт\\p{L}*", "обновление"],
    ["митинг\\p{L}*", "встреча"],
    ["юзкейс\\p{L}*", "сценарий"],
  ],
  fails,
  "FAIL 168-ФЗ",
);

// ---------- 38-ФЗ claims ----------
scan(
  [["лучш(?:ий|ая|ее|ие|его|ей|их)", "a provable number"], ["уникальн\\p{L}*", "what exactly differs"], ["инновационн\\p{L}*", "what it does"], ["лидер рынка", "a sourced number"], ["№\\s?1", "a sourced number"]],
  warns,
  "WARN 38-ФЗ claim",
);

// ---------- orthography and typography ----------
// ё stays only in names (Фёдор, Артём). A capitalized word is a name unless its lower-case
// form is a known common ё-word («Ещё» opening a sentence).
const COMMON_YO = new Set(["всё", "ещё", "её", "неё", "моё", "твоё", "своё", "чьё", "шёл", "пришёл", "нашёл", "прошёл", "учёт", "отчёт", "расчёт", "счёт", "объём", "приём", "подъём", "съёмка", "лёгкий", "тяжёлый", "чёрный", "зелёный", "жёлтый", "тёмный", "твёрдый", "дешёвый", "самолёт", "полёт", "учёный", "зачёт"]);
const yoCommon = [];
const yoNames = [];
for (const m of prose.matchAll(/\p{L}*ё\p{L}*/gu)) {
  const word = m[0];
  if (word[0] === word[0].toLowerCase() || COMMON_YO.has(word.toLowerCase())) yoCommon.push(word);
  else yoNames.push(word);
}
if (yoCommon.length) fails.push(`FAIL ё in common words: ${[...new Set(yoCommon)].slice(0, 8).join(", ")} → е`);
if (yoNames.length) warns.push(`WARN ё in capitalized words (keep only in names like Фёдор, Артём): ${[...new Set(yoNames)].slice(0, 8).join(", ")}`);
if (/\u2011/u.test(raw)) fails.push(`FAIL non-breaking hyphen U+2011 (lines ${lineOf(/\u2011/u)}) → plain hyphen; prevent wrapping in markup`);
if (/\.\.\./u.test(prose)) warns.push(`WARN three dots (lines ${lineOf(/\.\.\./u)}) → …`);
if (/(?<![=\w])"[^"\n]{2,}"/u.test(textOnly)) warns.push(`WARN straight quotes in prose → «ёлочки»`);
if (/[^.!?…\n]\s+Вы(?![\p{L}])/u.test(textOnly)) warns.push("WARN capital «Вы» mid-sentence → «вы»");
const dashes = (textOnly.match(/\s—\s/gu) ?? []).length;
if (wordCount && dashes / wordCount > 1 / 150) warns.push(`WARN em dash ×${dashes} in ${wordCount} words → keep only «подлежащее — сказуемое», split the rest`);
const multiDash = textOnly.split("\n").filter((l) => (l.match(/\s—\s/gu) ?? []).length >= 2).length;
if (multiDash) warns.push(`WARN ${multiDash} line(s) with 2+ em dashes`);

// ---------- headings ----------
const ACRONYM = /^[\p{Lu}\d-]{2,}$/u;
// Title Case: most words after the first start with a capital, including capitalized
// one-letter prepositions («В», «К»); acronyms (ИИ, CRM) and «Я» do not count.
const titleCase = (text) => {
  const ws = text.split(/\s+/u).slice(1).filter((w) => /^\p{L}/u.test(w));
  const caps = ws.filter((w) => (/^\p{Lu}\p{Ll}/u.test(w) && !ACRONYM.test(w)) || (/^\p{Lu}$/u.test(w) && w !== "Я"));
  return ws.length >= 3 && caps.length >= 2 && caps.length / ws.length >= 0.5;
};
for (const h of headings) if (titleCase(h.text)) fails.push(`FAIL Title Case heading «${h.text}» → sentence case`);
if (title !== undefined && titleCase(title.split(/\s[—|:]\s/u)[0])) fails.push(`FAIL Title Case title «${title}» → sentence case`);
const h1s = headings.filter((h) => h.level === 1).length;
if (h1s > 1) fails.push(`FAIL ${h1s} H1 headings → exactly one`);
headings.slice(1).forEach((h, at) => {
  const before = headings[at];
  if (h.level > before.level + 1) warns.push(`WARN heading level jumps H${before.level}→H${h.level} at «${h.text}»`);
});

// ---------- metadata length ----------
if (title !== undefined) {
  if (title.length > 70) fails.push(`FAIL title ${title.length} chars > 70`);
  else if (title.length > 60) warns.push(`WARN title ${title.length} chars > 60 (may be truncated)`);
}
if (description !== undefined) {
  if (description.length > 170) fails.push(`FAIL description ${description.length} chars > 170`);
  else if (description.length < 120 || description.length > 160) warns.push(`WARN description ${description.length} chars, target 120–160`);
}

// ---------- main phrase by lemma ----------
const STOP = new Set(["в", "во", "на", "за", "по", "до", "от", "из", "для", "с", "со", "к", "ко", "о", "об", "у", "и", "а", "но", "или", "не", "что", "как", "это", "при", "про", "без", "под", "над"]);
const phrase = opt("--phrase");
const report = [];
if (phrase) {
  const norm = (s) => s.toLowerCase().replace(/ё/gu, "е").replace(/-/gu, " ");
  const target = words(norm(phrase)).filter((w) => !STOP.has(w)).map(stem);
  const tokens = (s) => words(norm(s)).filter((w) => !STOP.has(w)).map(stem);
  const exactRe = new RegExp(`(?<![\\p{L}])${norm(phrase).replace(/[.*+?^${}()|[\]\\]/gu, "\\$&").replace(/\s+/gu, "[\\s\\u00a0-]+")}(?![\\p{L}])`, "gu");
  // The stemmer splits some forms of one word (диван→дива, диванов→диван), so stems also match on
  // their first 4 letters.
  const sameLemma = (a, b) => a === b || (a.length >= 4 && a.slice(0, 4) === b.slice(0, 4));
  const lemmaCount = (s) => {
    const t = tokens(s);
    let n = 0;
    const span = target.length + 2;
    const end = t.length;
    for (let i = 0; i < end; i++) {
      if (!target.some((x) => sameLemma(x, t[i]))) continue;
      const win = t.slice(i, i + span);
      const hits = target.map((x) => win.findIndex((w) => sameLemma(x, w)));
      if (hits.every((at) => at >= 0)) {
        n++;
        i += Math.max(...hits);
      }
    }
    return n;
  };
  const exact = (norm(textOnly).match(exactRe) ?? []).length;
  const lemma = lemmaCount(textOnly);
  const per1000 = wordCount ? ((lemma * 1000) / wordCount).toFixed(1) : "0";
  report.push(`phrase «${phrase}»: exact ${exact}, by lemma ${lemma}, per 1000 words ${per1000}, words ${wordCount}`);
  const lead = words(textOnly).slice(0, 120).join(" ");
  const zones = { title, h1, description, lead };
  for (const [zone, value] of Object.entries(zones)) {
    if (value === undefined) continue;
    const hit = lemmaCount(value) > 0;
    report.push(`  ${zone}: ${hit ? "yes" : "no"}`);
    if (!hit && (zone === "description" || zone === "lead")) warns.push(`WARN main phrase missing in ${zone}`);
  }
  const inTitle = title !== undefined && lemmaCount(title) > 0;
  const inH1 = h1 !== undefined && lemmaCount(h1) > 0;
  if ((title !== undefined || h1 !== undefined) && !inTitle && !inH1) fails.push("FAIL main phrase in neither title nor H1");
  const max = opt("--max") !== undefined ? Number(opt("--max")) : undefined;
  if (max !== undefined && lemma > max) fails.push(`FAIL main phrase by lemma ${lemma} > --max ${max}`);
  else if (max === undefined && wordCount >= 150 && lemma / wordCount > 1 / 150) warns.push(`WARN main phrase ${lemma}× by lemma in ${wordCount} words (> 1 per 150) → reread for stuffing`);
  const sentences = textOnly.split(/(?<=[.!?…])\s+/u);
  let streak = 0;
  for (const s of sentences) {
    streak = lemmaCount(s) > 0 ? streak + 1 : 0;
    if (streak === 3) warns.push("WARN main phrase in 3 consecutive sentences → pronoun or synonym");
  }
}

for (const l of report) console.log(l);
for (const l of fails) console.log(l);
for (const l of warns) console.log(l);
console.log(`${fails.length ? "FAIL" : "PASS"}: ${fails.length} fail, ${warns.length} warn`);
process.exit(fails.length ? 1 : 0);
