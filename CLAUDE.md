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

## Launch checklist (last reviewed 2026-05-03)

### ✅ Done — site is LIVE
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
- [x] Open Graph + Twitter card share previews
- [x] robots.txt + sitemap.xml
- [x] Google Maps embed on real address
- [x] All 14 photos wired (gallery + slideshow)
- [x] Mobile-responsive (verified — viewport, media queries, hamburger nav, touch swipe, tel: links)

### Open / future
- [ ] **Verify pricing with Doushka** — currently labeled "examples" (line 1033)
- [ ] **Google Business Profile**: take exterior photo of the building, upload to GBP dashboard
- [ ] **Test on phone**: open https://stationshotellet.com in mobile browser, click around all sections
- [ ] **Optional**: favicon (32x32 .ico or .png) — not yet referenced in `<head>`
- [ ] **Optional**: YouTube property tour video — embed iframe in gallery section (signals video to Google)
- [ ] **Optional**: Swedish-language page version with `<link rel="alternate" hreflang="sv">`
- [ ] **Optional later**: ImprovMX (free inbound forwarding) + Brevo SMTP (free outbound) for `info@stationshotellet.com` branding — only worth the setup once bookings volume justifies it
- [ ] **Optional**: clean up unused Loopia email forwarders (info@, booking@) since we're not using them — currently orphaned but harmless

## Live URLs
- Production: https://stationshotellet.com
- GitHub repo: https://github.com/sorenssl/stationshotellet
- Pages settings: https://github.com/sorenssl/stationshotellet/settings/pages
