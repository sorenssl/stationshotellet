// Stationshotellets Worker på Cloudflare (flytten från GitHub Pages, Tonys ja 2026-10-01).
//
// Uppgift: svara EXAKT som GitHub Pages gjorde (facit mätt 2026-10-01, se prov.mjs), plus
// säkerhetsrubrikerna GitHub inte kunde ge. Ingen sida får byta adress — det kostar rankning.
//
//   /sv/            → sv/index.html                         (200)
//   /sv             → 301 /sv/                               (mapp utan snedstreck)
//   /terms          → terms.html                             (200, som GitHub)
//   /terms.html     → terms.html                             (200, ingen omdirigering)
//   /terms/, /x     → 404.html med status 404
//   www.… och http  → 301 https://stationshotellet.com<samma sökväg>
//   *.workers.dev   → allt får X-Robots-Tag: noindex (förhandsskölden), ingen omdirigering

const KANON = 'stationshotellet.com';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const förhand = url.hostname.endsWith('.workers.dev') || url.hostname === 'localhost' || url.hostname === '127.0.0.1';

    if (!förhand && (url.hostname !== KANON || url.protocol === 'http:')) {
      return Response.redirect(`https://${KANON}${url.pathname}${url.search}`, 301);
    }

    const res = await svara(request, env, url);
    const ut = new Response(res.body, res);
    if (förhand) {
      ut.headers.set('X-Robots-Tag', 'noindex');
    } else {
      // Utan includeSubDomains: Loopias webmail/autodiscover-underdomäner ska inte tvingas (Edwin 2026-10-01).
      ut.headers.set('Strict-Transport-Security', 'max-age=31536000');
    }
    // GitHub gav charset=utf-8 på text-svar; Cloudflares asset-server utelämnar det på text/plain (llms.txt
    // har å/ö → "PiteÃ¥"). Vision mätte det 2026-10-02.
    const ct = ut.headers.get('content-type') || '';
    if (/^text\/(html|plain|css)/.test(ct) && !/charset/i.test(ct)) ut.headers.set('content-type', `${ct}; charset=utf-8`);
    ut.headers.set('X-Content-Type-Options', 'nosniff');
    ut.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    return ut;
  },
};

async function svara(request, env, url) {
  const väg = url.pathname;
  const hämta = (p) => env.ASSETS.fetch(new Request(new URL(p, url.origin), request));

  if (väg.endsWith('/')) {
    const r = await hämta(`${väg}index.html`);
    return r.status === 404 ? saknas(env, url) : r;
  }
  const sista = väg.slice(väg.lastIndexOf('/') + 1);
  if (!sista.includes('.')) {
    const sida = await hämta(`${väg}.html`);
    if (sida.status !== 404) return sida;
    const mapp = await hämta(`${väg}/index.html`);
    if (mapp.status !== 404) return Response.redirect(`${url.origin}${väg}/${url.search}`, 301);
    // GitHub gav 301 även för mappar utan index (t.ex. /images → /images/ → 404) — vi ger 404 direkt.
    return saknas(env, url);
  }
  const r = await hämta(väg);
  return r.status === 404 ? saknas(env, url) : r;
}

async function saknas(env, url) {
  const sida = await env.ASSETS.fetch(new URL('/404.html', url.origin));
  return new Response(sida.body, { status: 404, headers: sida.headers });
}
