# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Stations Hotellet** — A single-page marketing/booking website for an Airbnb accommodation in a converted railway station in Öjebyn, Sweden. Custom domain: **stationshotellet.com** (registered at Loopia). Hosting: GitHub Pages (free) + LoopiaDNS (~12,49 kr/mo for DNS records + email forwarding).

## Architecture

Single `index.html` file with inline CSS and JS. No build tools, no frameworks, no dependencies.

- **Booking form**: Uses Formspree — form action URL still needs a real Formspree form ID (line 1044)
- **Map**: Google Maps iframe pointed at `Västra Järnvägsgatan 5, 943 31 Öjebyn` (line 1140, address-based query format — no API key needed)
- **Photos**: All 14 photos in `images/full/` and `images/thumb/` are wired into gallery (11 items) and slideshow (14 slides). Hosts photo at `images/thumb/hosts.png`.
- **Email**: `info@stationshotellet.com` referenced throughout. Will be a forwarding alias via LoopiaDNS → `posetivemind67@gmail.com`. PayPal email kept as `posetivemind67@gmail.com` (line 1174) since PayPal account is bound to that address.
- **Open Graph**: og:url + og:image + twitter:card meta tags set (line 12-15) — share preview will show `kitchen-dining-wide.jpg` once site is live.

## Development

Open `index.html` directly in a browser. No build step required.

## Deployment

Hosted via GitHub Pages. Push to `main` branch, then enable Pages in repo Settings → Pages → Source: "Deploy from a branch" → `main` / `/ (root)`.

## TODO before launch (last reviewed 2026-05-03)

### Done
- [x] Canonical URL set to `https://stationshotellet.com/`
- [x] Schema.org email + contact email set to `info@stationshotellet.com`
- [x] Google Maps embed pointed at real address
- [x] All photos wired into gallery and slideshow
- [x] Open Graph image, URL, and twitter:card meta tags added

### Open
- [ ] **Sign up at Formspree** (free), create a form, paste form ID into form action (`index.html` line 1044, replaces `your-form-id`)
- [ ] **Create GitHub repo** under github.com/sorenssl — suggested name: `stationshotellet`
- [ ] **Push this repo** to that remote (current local repo at `c:\Git\Hotell\` has 1 commit, no remote)
- [ ] **Enable GitHub Pages**: Settings → Pages → Source: `main` / `/ (root)`
- [ ] **Add custom domain**: Settings → Pages → Custom domain → `stationshotellet.com`
- [ ] **In Loopia Kundzon**: subscribe to LoopiaDNS, point CNAME of `www.stationshotellet.com` → `sorenssl.github.io`, set apex A records to GitHub Pages IPs (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 — verify on GitHub Pages docs at deploy time)
- [ ] **In Loopia Kundzon**: set up email forwarding `info@stationshotellet.com` → `posetivemind67@gmail.com`
- [ ] **Verify pricing with Doushka** — currently labeled "examples" (line 1033)
- [ ] **Optional**: decide whether to migrate PayPal account to `info@stationshotellet.com` (currently kept on `posetivemind67@gmail.com` because PayPal accounts are bound to their registration email)
- [ ] **Optional**: add a favicon (32x32 .ico or .png) — not yet referenced in `<head>`
