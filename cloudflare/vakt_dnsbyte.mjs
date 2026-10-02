// Väntar tills GitHub-posterna (apex A 185.199.x, www CNAME) är borta ur CF-zonen, kör då publicera.mjs --skarpt.
import dns from 'node:dns/promises';
import { spawnSync } from 'node:child_process';

const [nsIp] = await dns.resolve4('kipp.ns.cloudflare.com');
const r = new dns.Resolver(); r.setServers([nsIp]);
const tid = () => new Date().toISOString();
const slut = Date.now() + 2 * 3600 * 1000;

while (Date.now() < slut) {
  const a = await r.resolve4('stationshotellet.com').catch(() => []);
  const c = await r.resolveCname('www.stationshotellet.com').catch(() => []);
  const ghA = a.filter((ip) => ip.startsWith('185.199.'));
  const ghC = c.filter((n) => /github\.io/.test(n));
  if (!ghA.length && !ghC.length) {
    console.log(`${tid()} GitHub-posterna borta (A=${a} CNAME=${c}) → publicerar skarpt`);
    const p = spawnSync(process.execPath, ['C:/Git/Hotell/cloudflare/publicera.mjs', '--skarpt'], { cwd: 'C:/Git/Hotell', stdio: 'inherit' });
    console.log(`${tid()} publicera.mjs slut, kod ${p.status}`);
    process.exit(p.status);
  }
  await new Promise((ok) => setTimeout(ok, 5000));
}
console.log(`${tid()} gav upp efter 2 h — posterna ligger kvar`);
process.exit(3);
