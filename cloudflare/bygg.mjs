// Bygger cloudflare/dist/ — det ENDA som publiceras på Cloudflare.
//
//   node cloudflare/bygg.mjs
//
// Läser ur git (HEAD), inte ur disken: okommitterat arbete kommer aldrig med (TAVLAN 2026-09-21).
// Vitlista på filtyper + svartlista på mappar: CLAUDE.md, *.py, seo_tracker/ m.fl. kan inte följa med
// (de låg publikt på domänen fram till 2026-10-01, se ROLLBACK.md). Stoppar med utgångskod 1 om något
// internt ändå skulle hamna i dist/.

import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HÄR = path.dirname(fileURLToPath(import.meta.url));
const ROT = path.resolve(HÄR, '..');
const DIST = path.join(HÄR, 'dist');
const stopp = (varför) => { console.error(`⛔ STOPP: ${varför}`); process.exit(1); };

const TILLÅTNA = /\.(html|xml|txt|ico|svg|png|jpe?g|webp|avif|gif|css|js|webmanifest|woff2?)$/i;
const ALDRIG_MAPP = /^(seo_tracker|branding|cloudflare|\.github|node_modules)\//;
const ALDRIG_NAMN = /(^|\/)(CLAUDE|ROLLBACK|SEO_NEXT_STEPS|README)[^/]*$|\.(md|py|ps1|bat|json|jsonc|csv|mjs)$/i;

const git = (args, opt = {}) => execFileSync('git', args, { cwd: ROT, maxBuffer: 64 << 20, ...opt });
const alla = git(['ls-tree', '-r', '--name-only', 'HEAD'], { encoding: 'utf8' }).split('\n').filter(Boolean);
const valda = alla.filter((f) => TILLÅTNA.test(f) && !ALDRIG_MAPP.test(f) && !f.startsWith('.'));

const fel = valda.filter((f) => ALDRIG_NAMN.test(f));
if (fel.length) stopp(`interna filer på väg in i dist/:\n${fel.join('\n')}`);
for (const måste of ['index.html', '404.html', 'robots.txt', 'sitemap.xml']) {
  if (!valda.includes(måste)) stopp(`${måste} saknas i bygget`);
}

// Tömmer i stället för att radera mappen (wrangler dev kan hålla den öppen på Windows — Visions lärdom 2026-09-26).
fs.mkdirSync(DIST, { recursive: true });
for (const f of fs.readdirSync(DIST)) fs.rmSync(path.join(DIST, f), { recursive: true, force: true });

for (const f of valda) {
  const mål = path.join(DIST, f);
  fs.mkdirSync(path.dirname(mål), { recursive: true });
  fs.writeFileSync(mål, git(['show', `HEAD:${f}`]));
}

const rev = git(['rev-parse', '--short', 'HEAD'], { encoding: 'utf8' }).trim();
console.log(`dist/ byggd ur ${rev}: ${valda.length} filer (av ${alla.length} i repot).`);
