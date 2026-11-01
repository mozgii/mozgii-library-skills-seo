#!/usr/bin/env node
// SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
// Copyright 2026 MOZGII, Inc. (https://mozgii.com/)
// Search demand for Russian phrases without accounts: Wordstat frequencies through the Bukvarix free copy
// (broad and exact «!», all regions) plus Yandex suggestions (what people type, by popularity).
//
//   node demand.mjs "ремонт квартир под ключ" "ремонт квартиры цена"   # look up phrases
//   node demand.mjs --file phrases.txt --out demand.tsv         # one phrase per line
//   node demand.mjs --expand "ремонт квартир" --expand "дизайн интерьера"   # seeds → candidates with suggest Signal
//   options: --top N (expanded candidates to look up, default 20), --cache <path> (default .seo-cache/demand.json), --json, --no-bukvarix, --no-suggest
//
// Levels with frequency data: strong = exact ≥ 20 (or exact ≥ 5 and a top-3 suggestion); some = exact ≥ 5, or exact ≥ 1
// and suggested; weak = broad only, or suggested with exact 0; none. Without frequency data (--no-bukvarix or an
// error) suggestions alone decide: top-3 = some, suggested = weak. A suggestion is wording evidence, not volume.
// Every request uses https, and a redirect to anything else is refused before it is followed, so a phrase never
// crosses the network in the clear. Bukvarix returns 429 after ~30 fast requests; the script waits and retries,
// sleeps between calls, and caches answers for 30 days so reruns do not hit the service again.
import fs from "node:fs";
import path from "node:path";

const USAGE = 'usage: node demand.mjs "phrase" … | --file list.txt | --expand "seed" [--top N] [--out file.tsv] [--json] [--cache path] [--no-bukvarix] [--no-suggest]';
const argv = process.argv.slice(2);
const wantsHelp = argv.some((a) => a === "--help" || a === "-h");
if (wantsHelp) {
  console.log(USAGE);
  process.exit(0);
}
const opts = { expand: [], top: 20, file: undefined, out: undefined, cache: ".seo-cache/demand.json", json: false, bukvarix: true, suggest: true };
const phrases = [];
const argCount = argv.length;
const required = (name, value) => {
  if (value === undefined || value.startsWith("--")) {
    console.error(`${name} needs a value\n${USAGE}`);
    process.exit(2);
  }
  return value;
};
for (let i = 0; i < argCount; i++) {
  const a = argv[i];
  if (a === "--expand") opts.expand.push(required(a, argv[++i]));
  else if (a === "--top") opts.top = Number(argv[++i]);
  else if (a === "--file") opts.file = required(a, argv[++i]);
  else if (a === "--out") opts.out = argv[++i];
  else if (a === "--cache") opts.cache = argv[++i];
  else if (a === "--json") opts.json = true;
  else if (a === "--no-bukvarix") opts.bukvarix = false;
  else if (a === "--no-suggest") opts.suggest = false;
  else if (a.startsWith("--")) {
    console.error(`unknown option ${a}`);
    process.exit(2);
  } else phrases.push(a);
}
if (opts.file) {
  try {
    phrases.push(...fs.readFileSync(opts.file, "utf8").split("\n").map((s) => s.trim()).filter((s) => s && !s.startsWith("#")));
  } catch (e) {
    console.error(`cannot read ${opts.file}: ${e.message}`);
    process.exit(2);
  }
}
if (!phrases.length && !opts.expand.length) {
  console.error(USAGE);
  process.exit(2);
}

const sleep = (ms) => new Promise((done) => setTimeout(done, ms));
const norm = (s) => s.toLowerCase().replace(/ё/gu, "е").replace(/-/gu, " ").replace(/\s+/gu, " ").trim();
const STOP = new Set(["в", "во", "на", "за", "по", "до", "от", "из", "для", "с", "со", "к", "ко", "о", "об", "у", "и", "а", "или", "при", "про", "без", "под", "над"]);
const terms = (s) => norm(s).split(" ").filter((w) => w && !STOP.has(w));
// Same word in another form: shared prefix with at most 2 differing trailing letters (диван / диваны / диванов).
const same = (a, b) => {
  let k = 0;
  while (k < a.length && k < b.length && a[k] === b[k]) k++;
  return k >= Math.min(a.length, b.length) - 2 && k >= 3;
};

let cache = {};
try {
  cache = JSON.parse(fs.readFileSync(opts.cache, "utf8"));
} catch {
  cache = {};
}
const saveCache = () => {
  fs.mkdirSync(path.dirname(opts.cache), { recursive: true });
  fs.writeFileSync(opts.cache, JSON.stringify(cache, null, 1));
};

const MAX_REDIRECTS = 5;
const REFUSED = -1; // Not 0: a refusal is final, and callers retry a 0.

async function get(url) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 45000);
  try {
    let target = new URL(url);
    for (let hop = 0; hop <= MAX_REDIRECTS; hop++) {
      if (target.protocol !== "https:") return { status: REFUSED, error: `refused a non-https address: ${target.protocol}//${target.host}` };
      // Redirects are followed by hand: fetch's own "follow" would send the phrase before the address could be checked.
      const res = await fetch(target, { signal: ctrl.signal, redirect: "manual", headers: { "user-agent": "Mozilla/5.0 (seo demand check)" } });
      const location = res.headers.get("location");
      if (res.status < 300 || res.status >= 400 || !location) return { status: res.status, body: await res.text() };
      await res.body?.cancel();
      target = new URL(location, target);
    }
    return { status: REFUSED, error: "too many redirects" };
  } catch (e) {
    return { status: 0, error: e.name === "AbortError" ? "timeout" : e.message };
  } finally {
    clearTimeout(timer);
  }
}

async function suggestList(part) {
  const key = `suggest ${norm(part)}`;
  const hit = cache[key];
  if (hit && Date.now() - Date.parse(hit.date) < 30 * 864e5) return hit.list;
  const r = await get(`https://suggest.yandex.ru/suggest-ff.cgi?part=${encodeURIComponent(part)}&uil=ru&v=3&sn=10`);
  if (r.status !== 200) throw new Error(`suggest: ${r.error ?? `HTTP ${r.status}`}`);
  let list;
  try {
    list = JSON.parse(r.body)[1] ?? [];
  } catch {
    throw new Error("suggest: unexpected response shape");
  }
  cache[key] = { list, date: new Date().toISOString() };
  saveCache();
  await sleep(700);
  return list;
}

async function frequency(phrase) {
  const key = `bukvarix ${norm(phrase)}`;
  const hit = cache[key];
  if (hit && Date.now() - Date.parse(hit.date) < 30 * 864e5) return hit;
  for (let attempt = 0; ; attempt++) {
    const r = await get(`https://api.bukvarix.com/v1/keywords/?q=${encodeURIComponent(phrase)}&api_key=free&format=tsv&num=100`);
    // 429 = burst limit (clears within a minute); 0 = timeout or network error on a heavy phrase.
    if ((r.status === 429 || r.status === 0) && attempt < 3) {
      await sleep(r.status === 429 ? 30000 : 5000);
      continue;
    }
    if (r.status !== 200) throw new Error(`bukvarix: ${r.error ?? `HTTP ${r.status}`}`);
    const rows = r.body.split("\n").slice(1).map((l) => l.split("\t")).filter((c) => c.length > 4);
    // Wordstat may hold the phrase in another form or order («доставка цветов москва» for «доставка цветов по москве»).
    const want = terms(phrase);
    const sameForm = (c) => {
      const got = terms(c[0]);
      return got.length === want.length && want.every((w) => got.some((g) => same(w, g)));
    };
    const row = rows.find((c) => norm(c[0]) === norm(phrase)) ?? rows.filter(sameForm).sort((a, b) => Number(b[4]) - Number(a[4]))[0];
    cache[key] = { broad: row ? Number(row[3]) : 0, exact: row ? Number(row[4]) : 0, as: row && norm(row[0]) !== norm(phrase) ? row[0] : "", date: new Date().toISOString() };
    saveCache();
    await sleep(3000);
    return cache[key];
  }
}

async function lookup(phrase) {
  const out = { phrase, broad: "", exact: "", as: "", position: "", offered: "", level: "", suggestions: "", error: "" };
  try {
    if (opts.bukvarix) Object.assign(out, await frequency(phrase));
    if (opts.suggest) {
      const own = await suggestList(phrase);
      const lead = norm(phrase).split(" ").slice(0, -1).join(" ");
      const typed = lead.includes(" ") || lead.length >= 3 ? await suggestList(lead) : [];
      out.position = typed.findIndex((s) => norm(s) === norm(phrase)) + 1 || "";
      out.offered = own.some((s) => norm(s) === norm(phrase)) ? "yes" : "";
      out.suggestions = own.slice(0, 5).join("; ");
    }
    const exact = Number(out.exact || 0);
    const pos = Number(out.position || 0);
    const suggested = Boolean(pos || out.offered);
    if (opts.bukvarix) out.level = exact >= 20 || (exact >= 5 && pos && pos <= 3) ? "strong" : exact >= 5 || (exact >= 1 && suggested) ? "some" : Number(out.broad || 0) || suggested ? "weak" : "none";
    else if (opts.suggest) out.level = pos && pos <= 3 ? "some" : suggested ? "weak" : "none";
  } catch (e) {
    out.error = e.message;
  }
  delete out.date;
  return out;
}

// Seed expansion: each seed bare and with commercial modifiers; Signal = Σ 1/position over every list the
// phrase appears in. It ranks candidates against each other; it is not a volume.
async function expand(seed) {
  const signal = new Map();
  for (const mod of ["", " цена", " стоимость", " под ключ", " заказать", " для бизнеса", " что это"]) {
    let list = [];
    try {
      list = await suggestList(seed + mod);
    } catch (e) {
      console.error(`expand «${seed + mod}»: ${e.message}`);
    }
    list.forEach((s, i) => signal.set(norm(s), (signal.get(norm(s)) ?? 0) + 1 / (i + 1)));
  }
  const ranked = [...signal.entries()].map(([phrase, score]) => ({ phrase, score }));
  ranked.sort((x, y) => y.score - x.score);
  return ranked.map(({ phrase, score }) => ({ phrase, signal: score.toFixed(2) }));
}

const rows = [];
for (const seed of opts.expand) {
  const candidates = await expand(seed);
  console.error(`seed «${seed}»: ${candidates.length} candidates`);
  for (const c of candidates.slice(0, opts.top)) rows.push({ seed, ...(await lookup(c.phrase)), signal: c.signal });
}
for (const p of phrases) rows.push(await lookup(p));

const cols = ["phrase", "level", "exact", "broad", "as", "position", "offered", "signal", "seed", "suggestions", "error"].filter((c) => rows.some((r) => r[c] !== undefined && r[c] !== ""));
const text = opts.json ? JSON.stringify(rows, null, 1) : [cols.join("\t"), ...rows.map((r) => cols.map((c) => String(r[c] ?? "").replace(/\t/gu, " ")).join("\t"))].join("\n");
if (opts.out) fs.writeFileSync(opts.out, text + "\n");
console.log(text);
process.exit(rows.some((r) => r.error) ? 1 : 0);
