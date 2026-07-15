# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Stations Hotellet** — A single-page marketing/booking website for an Airbnb accommodation in a converted railway station in Öjebyn, Sweden.

**Status**: 🟢 LIVE at https://stationshotellet.com (launched 2026-05-03).
**Domain**: registered at Loopia. **Hosting**: GitHub Pages (free, HTTPS via Let's Encrypt). **DNS**: LoopiaDNS (~12,49 kr/mo).
**Email**: direct to `posetivemind67@gmail.com` — no custom-domain mailbox or forwarding (chose simplicity; can upgrade later when bookings justify it).

## Architecture

Single `index.html` file with inline CSS and JS. No build tools, no frameworks, no dependencies.

- **Booking form**: Uses Formspree — form action URL still needs a real Formspree form ID (line 1044)
- **Map**: Google Maps iframe pointed at `Västra Järnvägsgatan 5, 943 31 Öjebyn` (line 1140, address-based query format — no API key needed)
- **Photos**: All 14 photos in `images/full/` and `images/thumb/` are wired into gallery (11 items) and slideshow (14 slides). Hosts photo at `images/thumb/hosts.png`.
- **Email**: `posetivemind67@gmail.com` used throughout — direct Gmail, no forwarding chain. Decided 2026-05-03 after Loopia→Gmail forwarding hit `554 Relay access denied` (industry-known problem). Volume is zero, simplicity wins. Can upgrade later to ImprovMX (free) + Brevo SMTP (free) for `info@` branding when bookings justify it.
- **Open Graph**: og:url + og:image + twitter:card meta tags set (line 12-15) — share preview will show `kitchen-dining-wide.jpg` once site is live.

## Development

Open `index.html` directly in a browser. No build step required.

## Deployment

Hosted via GitHub Pages. Push to `main` branch, then enable Pages in repo Settings → Pages → Source: "Deploy from a branch" → `main` / `/ (root)`.

## Pricing (updated 2026-07-15 by Soren — final ladder: ~10% / ~20% off nightly)

- **Nightly**: 990 kr (whole apartment, up to 5 guests, all-inclusive — cleaning, linens, Wi-Fi, parking)
- **Weekly**: 6,200 kr (886 kr/night — 10.5% off vs 7×990 = 6,930; cards say "save 10%")
- **Monthly**: 23,800 kr (793 kr/night — 19.9% off vs 30×990 = 29,700; cards say "save 20%"; weekly cleaning included)
- Ladder logic (Soren 2026-07-15): clean ~10%/~20% volume discounts. He first wanted weekly 8,000 but that exceeds 7×990 — savings claims must stay honest.
- 2026-07-15 market check: Piteå hotels 1,224–1,912 kr/night (Kust, Stadshotell), avg ~1,100 kr, hostel floor ~590–700 kr → 990 kr whole-apartment is the cheapest real accommodation; do not raise nightly above ~1,010 or the "lowest rates in Öjebyn" claim breaks (Öjebyn comp: 1,013 kr).
- History: launch 2026-05-09: 5,500/14,000 → 2026-07-15 morning: 6,500/19,000 (`update_prices_20260715.py`) → 2026-07-15 final: 6,200/23,800 (`update_prices_20260715b.py`). Scripts are one-shot.
- **Cancellation tiers**: 1-2 nights flexible (3 days), weekly moderate (7 days), monthly strict (1-month deposit, refundable 30+ days out)
- **Strategy**: cheapest 2BR whole-apartment within 30 km radius. Closest direct comp ("Centralt belägen villa i Öjebyn") is 1,013 kr/night with cleaning extra; we're 990 kr all-inclusive. Piteå-area 2BR median is 1,420 kr.
- **Source documents**: `OTA_DISTRIBUTION_ANALYSIS.md` (whether to list on Booking/Airbnb) + `SEO_NEXT_STEPS.md` (manual actions for Tony — GSC, GBP, backlinks)

## Launch checklist (last reviewed 2026-05-09)

### ✅ Done — site is LIVE with optimized pricing + SEO
- [x] Domain `stationshotellet.com` registered at Loopia
- [x] LoopiaDNS subscribed, custom DNS records configured
- [x] DNS A records (4 GitHub IPs) on apex + CNAME on www
- [x] GitHub repo `stationshotellet` under github.com/sorenssl
- [x] GitHub Pages enabled with custom domain
- [x] TLS certificate provisioned (Let's Encrypt via GitHub)
- [x] Enforce HTTPS enabled
- [x] Formspree form ID `xkoyoery` wired (booking form delivers to Gmail)
- [x] Email: posetivemind67@gmail.com used directly (no forwarding chain)
- [x] Schema.org LodgingBusiness + geo coordinates + amenityFeature
- [x] **Enriched JSON-LD** (2026-05-09): numberOfRooms, occupancy, makesOffer (3 tiers), containsPlace Apartment
- [x] **FAQPage JSON-LD** (2026-05-09): 7 Q&A entries — drives FAQ rich snippets in SERP
- [x] **BreadcrumbList JSON-LD** (2026-05-09)
- [x] Open Graph + Twitter card share previews + image dimensions
- [x] robots.txt + sitemap.xml (lastmod refreshed 2026-05-09)
- [x] Google Maps embed on real address
- [x] All 14 photos wired (gallery + slideshow)
- [x] Mobile-responsive (verified — viewport, media queries, hamburger nav, touch swipe, tel: links)
- [x] **Six** language versions: EN / SV / FR / DE / PL / RO — all with hreflang + sitemap
- [x] **Real pricing live** (2026-05-09) — replaced "examples" placeholders with 990/5500/14000 kr in EN, SV, DE, PL, RO
- [x] **French (/fr/) language version added** (2026-05-09) — full translation, new pricing card, hreflang/og:locale on all sister pages
- [x] **Hero copy updated** with "lowest rates in Öjebyn" + 990 kr signal
- [x] **Image optimization (2026-05-09)**: WebP versions of all 28 images generated alongside JPEGs. Every `<img>` wrapped in `<picture>` with WebP source + JPEG fallback. Hero CSS uses `image-set()`. hosts.png (434 KB) replaced by hosts.jpg + hosts.webp (27 KB WebP, 49 KB JPEG fallback). **First-paint weight: 658 KB → 146 KB (78% reduction)**. Full gallery: 1.18 MB → 525 KB (55%). Helper scripts: `optimize_images.py`, `update_picture_tags.py`.
- [x] **Cloudflare Web Analytics (2026-05-09)**: privacy-friendly cookie-less analytics live on all 6 language versions. No cookie banner, no GDPR consent paperwork, GDPR-compliant by design. Token: `56268582f31646be956658d1aaefaab9`. Dashboard at https://dash.cloudflare.com/?to=/:account/web-analytics. 30-day rolling retention.
- [x] **Tourist-SEO + style upgrade (2026-07-14)** — rollback tag `pre-upgrade-2026-07-14`, see `ROLLBACK.md`. Scripts: `upgrade_20260714_{assets,seo_content,style_ux}.py` (one-shot, NOT idempotent). All 6 languages:
  - Favicon set from SH monogram (`favicon.ico`, 32px PNG, apple-touch-icon) — Google shows favicons in mobile SERPs
  - Hero + og:image swapped to the real northern-lights exterior photo (matches GBP cover). Hero WebP is 28 KB → faster LCP; also fixed pre-existing bug where `image-set()` dropped the darkening gradient
  - Titles/descriptions rewritten with tourist keywords (Swedish Lapland / Laponie suédoise / Schwedisch-Lappland / etc.)
  - Translated pages got the full enriched LodgingBusiness JSON-LD (was EN-only since May) + translated FAQPage schema
  - New visible FAQ section (6 Q&As: aurora, Pite Havsbad, airport, price, check-in, cancellation), matching schema
  - **Pite Havsbad distance corrected ~5 km → ~15 km** (5 km was from central Piteå, not from Öjebyn — verified)
  - Entrance-veranda photo (from Soren's `Airbnb_Entre.jpg`) added to gallery + slideshow; aurora photo added as slide 14 (hero click opens it)
  - CSS: serif heading stack (matches SH monogram), scroll-margin-top fix (anchors no longer hide behind navbar), `:focus-visible` outlines, `prefers-reduced-motion` support, sticky mobile "Book now" bar (auto-hides at booking form)

### Open / pending Tony's manual action
- [ ] **GSC + Bing Webmaster verification** — see SEO_NEXT_STEPS.md (highest leverage right now — site not yet indexed)
- [ ] **Google Business Profile finish** — take exterior photo, upload, complete profile (postcard verification ~5-10 days)
- [ ] **Free directory backlinks** — email Visit Pite, Swedish Lapland, pitea.se, Bothnian Coastal Route (~30 min, big SEO win)
- [ ] **Test on phone** — actual mobile booking flow not yet verified

### Decisions confirmed (2026-05-09)
- [x] **Pricing** — 990 kr/5,500 kr/14,000 kr confirmed by Tony AND Doushka 2026-05-09
- [x] **DE/PL/RO/FR translations** — same new pricing structure live across all language versions

### Decision deferred
- [ ] **OTA listings (Booking.com / Airbnb)** — see OTA_DISTRIBUTION_ANALYSIS.md. Recommendation: hold for Months 1-3, list Month 4 if direct-book volume insufficient.

### Optional / future
- [x] favicon — DONE 2026-07-14 (SH monogram: favicon.ico + favicon-32x32.png + apple-touch-icon.png)
- [ ] YouTube property tour video — embed iframe (signals video to Google)
- [ ] ImprovMX (free inbound forwarding) + Brevo SMTP for `info@` branding — only when booking volume justifies
- [ ] Clean up unused Loopia email forwarders (info@, booking@) — orphaned but harmless

## Live URLs
- Production: https://stationshotellet.com
- GitHub repo: https://github.com/sorenssl/stationshotellet
- Pages settings: https://github.com/sorenssl/stationshotellet/settings/pages
