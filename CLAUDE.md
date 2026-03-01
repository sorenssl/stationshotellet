# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Stations Hotellet** — A single-page marketing/booking website for an Airbnb accommodation in a converted railway station in Öjebyn, Sweden. Hosted on GitHub Pages.

## Architecture

Single `index.html` file with inline CSS and JS. No build tools, no frameworks, no dependencies.

- **Booking form**: Uses Formspree (form action URL needs a real Formspree form ID)
- **Map**: Embedded Google Maps iframe (coordinates may need tuning for exact address)
- **Photos**: Currently CSS gradient placeholders — replace `<div class="gallery-item">` and `<div class="about-image">` contents with `<img>` tags

## Development

Open `index.html` directly in a browser. No build step required.

## Deployment

Hosted via GitHub Pages. Push to `main` branch, then enable Pages in repo Settings → Pages → Source: "Deploy from a branch" → `main` / `/ (root)`.

## TODO before launch

- Replace Formspree URL (`https://formspree.io/f/your-form-id`) with a real endpoint
- Replace placeholder images with actual photos
- Update Google Maps embed with exact coordinates
- Update `<link rel="canonical">` with the real GitHub Pages URL
- Verify pricing with owners
