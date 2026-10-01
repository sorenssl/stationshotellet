// URL-provet (kritisk provning) — svarar sajten EXAKT som GitHub Pages gjorde?
//
//   node cloudflare/prov.mjs https://stationshotellet.<konto>.workers.dev   (förhand)
//   node cloudflare/prov.mjs https://stationshotellet.com                   (efter flytten)
//
// Facit = GitHub Pages mätt 2026-10-01 10:40 CEST (curl). Innehållet jämförs byte för byte mot dist/.
// Röd rad = utgångskod 1. Kör `node cloudflare/bygg.mjs` först så att dist/ motsvarar det publicerade.

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const DIST = path.join(path.dirname(fileURLToPath(import.meta.url)), 'dist');
const BAS = (process.argv[2] || '').replace(/\/$/, '');
if (!/^https?:\/\//.test(BAS)) { console.error('Användning: node cloudflare/prov.mjs <bas-url>'); process.exit(1); }
const { hostname } = new URL(BAS);
const förhand = hostname.endsWith('.workers.dev') || hostname === 'localhost' || hostname === '127.0.0.1';
const KANON = 'https://stationshotellet.com';

let röda = 0, gröna = 0;
const rad = (ok, text) => { ok ? gröna++ : röda++; if (!ok || process.env.PROV_ALLT) console.log(`${ok ? '✅' : '❌'} ${text}`); };
const hämta = (u, extra = {}) => fetch(u, { redirect: 'manual', headers: { 'user-agent': 'edwin-prov/1' }, ...extra });
const sha = (b) => crypto.createHash('sha256').update(b).digest('hex');
const distFil = (p) => { const f = path.join(DIST, p.endsWith('/') ? `${p}index.html` : p); return fs.existsSync(f) ? fs.readFileSync(f) : null; };

// 1. Facit: [sökväg, status, location-sökväg eller null]
const FACIT = [
  ['/', 200], ['/index.html', 200], ['/sv', 301, '/sv/'], ['/sv/', 200], ['/sv/index.html', 200],
  ['/fr', 301, '/fr/'], ['/fr/', 200], ['/de/', 200], ['/pl/', 200], ['/ro/', 200],
  ['/terms', 200], ['/terms.html', 200], ['/terms/', 404], ['/404-test', 404], ['/images/', 404],
  ['/robots.txt', 200], ['/llms.txt', 200], ['/sitemap.xml', 200], ['/404.html', 200],
  ['/favicon.ico', 200], ['/favicon.svg', 200], ['/apple-touch-icon.png', 200], ['/favicon-32x32.png', 200],
  // De interna filerna — läckan som stängdes 2026-10-01. Får ALDRIG svara 200.
  ['/CLAUDE.md', 404], ['/SEO_NEXT_STEPS.md', 404], ['/ROLLBACK.md', 404], ['/OTA_DISTRIBUTION_ANALYSIS.md', 404],
  ['/seo_tracker/history.csv', 404], ['/seo_tracker/config.json', 404], ['/add_amenities.py', 404],
  ['/_config.yml', 404], ['/cloudflare/worker.mjs', 404], ['/cloudflare/wrangler.jsonc', 404], ['/branding/README.md', 404],
  ['/.gitignore', 404], ['/CNAME', 404],
];
for (const [p, status, plats] of FACIT) {
  const r = await hämta(BAS + p);
  const loc = r.headers.get('location');
  const locVäg = loc ? new URL(loc, BAS).pathname : null;
  rad(r.status === status && (plats ? locVäg === plats : !loc), `${p} → ${r.status}${loc ? ` ${loc}` : ''} (facit ${status}${plats ? ` ${plats}` : ''})`);
  if (r.status === 404 && p !== '/404.html') {
    const t = await r.text();
    rad(sha(Buffer.from(t)) === sha(distFil('/404.html') || ''), `${p} visar sajtens egen 404-sida`);
  }
}

// 2. Varje sida i sitemap + varje resurs sidorna pekar på: 200 och SAMMA BYTE som dist/.
const karta = await (await hämta(`${BAS}/sitemap.xml`)).text();
const sidor = [...karta.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => new URL(m[1]).pathname);
rad(sidor.length >= 7, `sitemap har ${sidor.length} sidor (facit 7)`);
const resurser = new Set();
for (const p of sidor) {
  const r = await hämta(BAS + p);
  const b = Buffer.from(await r.arrayBuffer());
  const d = distFil(p);
  rad(r.status === 200 && d && sha(b) === sha(d), `sida ${p} → ${r.status}, ${d && sha(b) === sha(d) ? 'samma byte som dist/' : 'ANNAT INNEHÅLL'}`);
  for (const m of b.toString('utf8').matchAll(/(?:src|href|srcset|content)="([^"]+)"/g)) {
    for (const del of m[1].split(',')) {
      const u = del.trim().split(/\s+/)[0];
      if (u.startsWith('/') && !u.startsWith('//')) resurser.add(u.split(/[?#]/)[0]);
      else if (u.startsWith(KANON + '/')) resurser.add(new URL(u).pathname);
    }
  }
}
for (const p of [...resurser].sort()) {
  const r = await hämta(BAS + p);
  const b = Buffer.from(await r.arrayBuffer());
  const d = p.endsWith('/') || !p.slice(p.lastIndexOf('/')).includes('.') ? null : distFil(p);
  const ok = r.status === 200 && (d === null || sha(b) === sha(d));
  rad(ok, `resurs ${p} → ${r.status}`);
}
console.log(`(${sidor.length} sidor, ${resurser.size} resurser jämförda)`);

// 3. Rubriker
const start = await hämta(`${BAS}/`);
const h = (n) => start.headers.get(n) || '';
rad(h('x-content-type-options') === 'nosniff', `X-Content-Type-Options: ${h('x-content-type-options') || 'saknas'}`);
rad(h('referrer-policy') === 'strict-origin-when-cross-origin', `Referrer-Policy: ${h('referrer-policy') || 'saknas'}`);
rad(/text\/html/.test(h('content-type')), `Content-Type: ${h('content-type')}`);
if (förhand) {
  rad(/noindex/.test(h('x-robots-tag')), `förhandsskölden X-Robots-Tag: ${h('x-robots-tag') || 'SAKNAS'}`);
} else {
  rad(!/noindex/.test(h('x-robots-tag')), `ingen noindex på riktiga domänen (${h('x-robots-tag') || 'ok'})`);
  rad(/max-age=\d+/.test(h('strict-transport-security')), `HSTS: ${h('strict-transport-security') || 'saknas'}`);
  // 4. Omdirigeringarna, som GitHub: www och http → https://stationshotellet.com, samma sökväg
  for (const [från, till] of [
    ['http://stationshotellet.com/', `${KANON}/`], ['https://www.stationshotellet.com/', `${KANON}/`],
    ['http://www.stationshotellet.com/sv/', `${KANON}/sv/`], ['https://www.stationshotellet.com/terms.html', `${KANON}/terms.html`],
  ]) {
    const r = await hämta(från);
    rad(r.status === 301 && r.headers.get('location') === till, `${från} → ${r.status} ${r.headers.get('location')} (facit 301 ${till})`);
  }
}

console.log(`\n${röda ? '❌ RÖTT' : '✅ GRÖNT'}: ${gröna} gröna, ${röda} röda — ${BAS}`);
process.exit(röda ? 1 : 0);
