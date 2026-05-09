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

## Pricing (locked 2026-05-09 after competitor research)

- **Nightly**: 990 kr (whole apartment, up to 5 guests, all-inclusive — cleaning, linens, Wi-Fi, parking)
- **Weekly**: 5,500 kr (786 kr/night — 21% volume discount)
- **Monthly**: 14,000 kr (467 kr/night — 53% discount, weekly cleaning included)
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
- [x] All 5 language versions have hreflang in head + sitemap
- [x] **Real pricing live** (2026-05-09) — replaced "examples" placeholders with 990/5500/14000 kr
- [x] **Swedish (/sv/) pricing updated** to match EN
- [x] **Hero copy updated** with "lowest rates in Öjebyn" + 990 kr signal

### Open / pending Tony's manual action
- [ ] **GSC + Bing Webmaster verification** — see SEO_NEXT_STEPS.md (highest leverage right now — site not yet indexed)
- [ ] **Google Business Profile finish** — take exterior photo, upload, complete profile (postcard verification ~5-10 days)
- [ ] **Free directory backlinks** — email Visit Pite, Swedish Lapland, pitea.se, Bothnian Coastal Route (~30 min, big SEO win)
- [ ] **Translate price changes to /de/, /pl/, /ro/** — same pattern as EN/SV (Tony or future Jarvis pass)
- [ ] **Test on phone** — actual mobile booking flow not yet verified
- [ ] **Doushka review** — confirm she's happy with 990/5500/14000 pricing (decided autonomously based on competitor data)

### Decision deferred
- [ ] **OTA listings (Booking.com / Airbnb)** — see OTA_DISTRIBUTION_ANALYSIS.md. Recommendation: hold for Months 1-3, list Month 4 if direct-book volume insufficient.

### Optional / future
- [ ] favicon (32x32 .ico or .png) — not yet referenced in `<head>`
- [ ] YouTube property tour video — embed iframe (signals video to Google)
- [ ] ImprovMX (free inbound forwarding) + Brevo SMTP for `info@` branding — only when booking volume justifies
- [ ] Clean up unused Loopia email forwarders (info@, booking@) — orphaned but harmless

## Live URLs
- Production: https://stationshotellet.com
- GitHub repo: https://github.com/sorenssl/stationshotellet
- Pages settings: https://github.com/sorenssl/stationshotellet/settings/pages
