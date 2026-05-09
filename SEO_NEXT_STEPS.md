# SEO Next Steps — Manual Actions for Tony

**As of**: 2026-05-09 — after Jarvis's autonomous SEO upgrade pass
**Site state**: Live but not yet indexed by Google (`site:stationshotellet.com` returned zero results 2026-05-09)

The site-side technical SEO is now strong. These next steps require Tony at the keyboard / phone — they can't be done autonomously.

---

## 🔴 Highest leverage — do first (~45 min total)

### 1. Google Search Console — get indexed

1. Go to https://search.google.com/search-console
2. Add property: `https://stationshotellet.com/` (URL prefix property)
3. Verify ownership — easiest method: HTML tag (paste in `<head>` of `index.html`)
   - Tell Jarvis the verification tag and he'll add it
4. Once verified: Sitemaps → Add sitemap → `sitemap.xml`
5. URL Inspection → enter `https://stationshotellet.com/` → "Request Indexing"
6. Repeat URL Inspection for `/sv/`, `/de/`, `/pl/`, `/ro/`

**Expected result**: Site starts appearing in Google search within 1-7 days. Without this step, indexing can take 2-8 weeks.

### 2. Bing Webmaster Tools (5 min)

1. https://www.bing.com/webmasters/
2. Add site, import from Google Search Console (one click after step 1)
3. ~5% of Swedish search is Bing — small but free.

### 3. Google Business Profile — finish setup

You already started this 2026-05-03 but skipped the exterior photo. Now's the time:

1. Take the exterior photo of the converted railway station building (best lighting: golden hour)
2. Take 2-3 interior photos (your existing kitchen-dining-wide.jpg is good for the cover)
3. Go back to https://business.google.com/
4. Complete profile: photos, business hours, services list (apartment rental), description
5. Verify by mail/phone (Google sends a postcard with code — takes 5-10 days)
6. Once verified: respond to any reviews, post weekly "what's nearby" content

**Why this matters most**: Google Business Profile is THE #1 driver of local search visibility. The "Map Pack" (top 3 map results) shows up before regular organic results for searches like "lägenhet Öjebyn" or "boende Piteå." Free, dominates clicks.

---

## 🟡 Free backlinks — do this week (~30 min total)

These are tourism/business directories that will list you for free AND give you a SEO backlink. Each backlink raises your domain authority.

### 4. Visit Pite (Pite tourism board)

- Email: https://www.visitpitea.se/ — find their contact form or accommodation submission
- Pitch: "Newly opened apartment in converted railway station, Öjebyn. Would like to be listed in your accommodation directory."
- Result: free directory listing + backlink (visitpitea.se has high domain authority)

### 5. Swedish Lapland (regional tourism)

- https://www.swedishlapland.com/pitea/
- Same pitch. Even higher authority site.

### 6. Bothnian Coastal Route

- https://bothniancoastalroute.com/
- Listed: Pite Havsbad, others. Submit your listing.

### 7. pitea.se/inflyttare/boende (Piteå municipality)

- They list local accommodation under the "Inflyttare" (newcomers) section
- Email municipality, request listing for short-term accommodation

### 8. Norrbottens Handelskammare (Chamber of Commerce)

- If you join (membership fee), you're listed in their corporate-housing directory
- Healthcare contractors often discover via this — very on-target audience
- Cost: ~3,000-5,000 kr/year. Probably not worth Year 1; revisit Year 2.

### 9. Local PR — railway station story angle

- Pite-Tidningen (https://www.pt.se/) and Norrbottens-Kuriren (https://www.kuriren.nu/)
- Pitch: "Old railway station gets new life as Öjebyn's most affordable apartment rental"
- Free coverage, valuable local backlinks
- Doushka can do this — she has the local angle

---

## 🟢 Optional but valuable (Month 2+)

### 10. Tripadvisor

- Free listing for accommodations
- Slow to gain reviews but generates Google trust

### 11. YouTube property tour video

- 60-90 second walkthrough, embed on the site
- Signals video content to Google → richer search snippets
- Even a phone-recorded tour works — authenticity beats production value

### 12. Wikidata entry

- The original railway station building probably has historical significance. A Wikidata/Wikipedia entry with a citation back to your site is a powerful backlink.
- Doushka likely knows the building's history.

---

## 🔵 Things I (Jarvis) already did on the site (no action needed from you)

- ✅ Tightened `<title>` to 56 chars (was 71, Google truncates at 60)
- ✅ Tightened `<meta description>` to 154 chars (was 167)
- ✅ Updated keywords meta with Swedish + English long-tail keywords
- ✅ Strengthened OpenGraph + Twitter card metadata
- ✅ Enriched JSON-LD `LodgingBusiness` schema:
  - Added `numberOfRooms`, `occupancy`, `containsPlace` (Apartment sub-entity)
  - Added `makesOffer` array with all three pricing tiers
  - Expanded `amenityFeature` from 5 to 9 amenities
  - Added `currenciesAccepted`, `paymentAccepted`, `slogan`, `petsAllowed`, `smokingAllowed`
- ✅ Added `FAQPage` JSON-LD with 7 questions (drives FAQ rich snippets in SERP)
- ✅ Added `BreadcrumbList` JSON-LD
- ✅ Added `googlebot` and `bingbot` meta directives
- ✅ Added `max-image-preview:large` for richer image previews in search
- ✅ Updated `<h1>` and hero copy to lead with "Lowest rates in Öjebyn" + 990 kr signal
- ✅ Updated `sitemap.xml` lastmod dates (2026-05-09)
- ✅ Updated price card on EN + SV with new pricing, cancellation tiers, cleaning included
- ✅ Removed "Prices are examples" disclaimer (now real prices, not placeholders)

---

## Tracking — how to know it's working

After you do the GSC + GBP steps:

| Metric | Where to check | Target by Month 3 |
|---|---|---|
| Google Search Console impressions | search.google.com/search-console | 200+ impressions/week |
| Google Search Console clicks | search.google.com/search-console | 20+ clicks/week |
| Indexed pages | GSC → Indexing → Pages | 5/5 (all language versions) |
| Google Business Profile views | business.google.com | 100+ views/week |
| Top organic keyword | GSC → Performance → Queries | "Stations Hotellet" should appear |
| Long-tail rank | Google search "lägenhet Öjebyn" | Page 1 of results |

---

## Rough timeline

| Week | Expected progress |
|------|-------------------|
| 1 | Submit to GSC + Bing. Site starts appearing for brand searches ("Stations Hotellet"). |
| 2-3 | Google indexes all 5 language versions. Brand search shows your site. |
| 4-6 | Long-tail searches start including you (e.g. "lägenhet Öjebyn 2 sovrum"). Bottom of page 1. |
| 6-12 | GBP gets first reviews. Map Pack visibility for "lägenhet Öjebyn", "boende Öjebyn". |
| 3-6 mo | Top 3 in Map Pack for Öjebyn-specific searches. Maybe page 1 organic for "lägenhet Piteå" if backlinks strong. |
| 6-12 mo | Established direct-book channel. OTA reliance can drop. |

---

*— Jarvis, 2026-05-09. The site-side work is done; the rest is verification + photos + outreach, all of which require you on the ground.*
