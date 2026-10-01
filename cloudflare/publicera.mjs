// Publicerar stationshotellet.com på Cloudflare. Enda vägen ut — kör aldrig `wrangler deploy` för hand.
//
//   node cloudflare/publicera.mjs            förhandsadressen (*.workers.dev, noindex)
//   node cloudflare/publicera.mjs --skarpt   riktiga domänen (Tonys ja 2026-10-01 10:34 gäller flytten)
//
// Spärrarna (var och en stoppar med utgångskod 1) — samma mönster som Visions mall/publicera.mjs:
//  1. cloudflare/ är committad: Workern och inställningarna läses från disken.
//  2. Förhand: inga "routes" i wrangler.jsonc. Skarpt: routes MÅSTE finnas.
//  3. Bygget (ur git HEAD) → deploy från cloudflare/ → svaret ska nämna Workern "stationshotellet".
//  4. URL-provet körs direkt efteråt mot rätt adress. Rött = utgångskod 1.

import { execFileSync, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HÄR = path.dirname(fileURLToPath(import.meta.url));
const ROT = path.resolve(HÄR, '..');
const skarpt = process.argv.includes('--skarpt');
const stopp = (varför) => { console.error(`⛔ STOPP: ${varför}`); process.exit(1); };

let smuts;
try {
  smuts = execFileSync('git', ['status', '--porcelain', '--untracked-files=all', '--', 'cloudflare'], { cwd: ROT, encoding: 'utf8' })
    .split('\n').filter(Boolean).filter((r) => !/cloudflare\/(dist|node_modules)\//.test(r));
} catch (e) { stopp(`kunde inte fråga git (${e.message}) — okänt räknas som smutsigt`); }
if (smuts.length) stopp(`okommitterat i cloudflare/, committa först:\n${smuts.join('\n')}`);

const cfg = fs.readFileSync(path.join(HÄR, 'wrangler.jsonc'), 'utf8').replace(/\/\/.*$/gm, '');
const namn = (cfg.match(/"name":\s*"([^"]+)"/) || [])[1];
if (namn !== 'stationshotellet') stopp(`Worker-namnet är "${namn}", väntat "stationshotellet"`);
const harDomän = /"routes"\s*:/.test(cfg);
if (!skarpt && harDomän) stopp('wrangler.jsonc har routes men --skarpt saknas');
if (skarpt && !harDomän) stopp('--skarpt men wrangler.jsonc har ingen route till stationshotellet.com');

if (spawnSync(process.execPath, [path.join(HÄR, 'bygg.mjs')], { stdio: 'inherit' }).status !== 0) stopp('bygget misslyckades');

console.log(`\n${skarpt ? '🔴 SKARP publicering' : 'Förhandsversion'} → Worker "${namn}" …`);
const wrangler = path.join(HÄR, 'node_modules', 'wrangler', 'bin', 'wrangler.js');
if (!fs.existsSync(wrangler)) stopp('wrangler saknas — kör `npm install` i cloudflare/');
const ut = spawnSync(process.execPath, [wrangler, 'deploy'], { cwd: HÄR, encoding: 'utf8' });
const text = `${ut.stdout || ''}${ut.stderr || ''}`;
console.log(text.split('\n').filter((r) => /Uploaded|Deployed|https:\/\/|Version ID|ERROR|✘/.test(r)).join('\n'));
if (ut.status !== 0) stopp('wrangler deploy misslyckades (se ovan)');
if (!/Uploaded stationshotellet\b/.test(text)) stopp('svaret nämner inte Workern "stationshotellet" — kontrollera i Cloudflare');

const bas = skarpt ? 'https://stationshotellet.com' : (text.match(/https:\/\/[\w.-]+\.workers\.dev/) || [])[0];
if (!bas) stopp('hittade ingen workers.dev-adress i svaret — kör prov.mjs för hand');
console.log(`\nURL-provet mot ${bas} …`);
const prov = spawnSync(process.execPath, [path.join(HÄR, 'prov.mjs'), bas], { stdio: 'inherit' });
process.exit(prov.status);
