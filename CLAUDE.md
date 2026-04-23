# Project: Skyways Timeline

## Repository
- GitHub: `git@github.com:skyways-shaewilson/Skyways-timeline.git`
- Branch: `main`
- Single-file project: `index.html` (no build tools, no package.json)
- SSH auth configured (ed25519 key)
- Hosted on GitHub Pages

## User: Shae Wilson
- Director of Marketing at Skyways Air Transportation Inc.
- Tests primarily on mobile (iPhone/Safari) — always validate mobile behavior
- Prefers concise, compact UI — single-line elements over multi-line blocks
- Wants changes pushed to GitHub immediately after each edit (no batching)
- Iterative workflow: edit → push → test on device → report issues → fix
- Does not want local dev servers — just edit files and push
- Prefers direct action over planning discussions — just do it
- Don't ask Shae to check things manually — verify yourself via APIs, scripts, or Firestore REST API
- At the end of every project session: update CLAUDE.md, PRD, MEMORY.md, and all project docs

## Typography
- **Font:** Founders Grotesk (self-hosted WOFF2), replaced Google Fonts Inter (April 14, 2026)
- **Font files:** `/Founders Grotesk Family/WOFF2/` — 10 files (Light, Regular, Medium, Semibold, Bold × normal + italic)
- **10 `@font-face` declarations** in `<style>` block, `font-display: swap`
- **`font-family: 'Founders Grotesk', sans-serif`** on `body`
- **Weight mapping:** Light=300, Regular=400, Medium=500, Semibold=600, Bold=700
- **Detail text, subtitle, search input:** `font-weight: 450` (interpolates between Regular and Medium — Founders Grotesk renders lighter than Inter at the same weight)
- **Card titles:** `font-size: 22px` desktop, `19px` mobile

## Technical Lessons (Mobile Safari / iOS)
- NEVER put `overflow-x: hidden` on `html` or `body` — it breaks `position: sticky`
- NEVER put `overflow: hidden` on `.event-card` — it clips source dropdown menus. Put it on `.event-card-bg` instead.
- NEVER put `overflow: hidden` on `.stat` — it clips the `.stat-menu` drawer. The drawer is absolutely positioned and needs to escape its parent.
- Use `overflow-x: clip` on individual content containers instead
- Touch devices need explicit `click`/`touchstart` handlers — CSS `:hover` doesn't work
- `min-width` on absolutely positioned elements can cause horizontal scroll — constrain with `calc(100vw - Npx)` or `max-width`
- Always include `-webkit-sticky` for Safari sticky positioning support
- Mobile stats/filter section: keep compact (~40% smaller than desktop)
- Year label sticky offset tracks the animated header height via a ResizeObserver, not per-scroll-frame getBoundingClientRect

## Sticky Header Scroll Behavior
- **Threshold:** `scrollY > 4` minimizes; `scrollY <= 4` restores. No hysteresis — low threshold feels "fast enough" per Shae.
- **No scroll compensation.** The old `scrollBy(0, -delta)` bounce-loop-prevention pattern was removed so the threshold could be this low. Content does shift once on minimize; at 4px scroll the user doesn't notice.
- **Animated layout transitions:** `.brand-bar` height, `.logo-wrap` height, `.hero-section` padding, `.stats-banner-inner` padding, `.stat-value` font-size all animate 220ms `cubic-bezier(0.4,0,0.2,1)`. Was instant snap (required by scroll compensation); compensation is gone so these can animate smoothly.
- **Year-label sync:** `ResizeObserver` on `#stickyHeader` calls `syncYearLabelOffset()` whenever the animated height actually changes. Do NOT call sync per scroll frame — that forces layout and causes stutter at zoom/narrow viewports.
- **`updateYearLabels` read/write batching:** three passes (read all rects → compute all target styles → write all styles). Interleaved read/write loops cause per-label layout thrash on scroll.
- **Cached NodeLists:** `getYearLabels()` / `getYearSections()` memoize `querySelectorAll` between scroll frames. `renderTimeline()` calls `invalidateYearLabelCache()` + `invalidateYearSectionCache()` after `innerHTML =`.

## Search System
- **Always-visible search bar** in header — white background, navy text, placeholder "Search events..."
- Replaces previous toggle/magnifying-glass pattern — search is always accessible
- Filters cards in real-time by title and detail text
- Styled to match header in both expanded and minimized (scrolled) states

## Hero Section
- **Layout:** three stacked block elements inside `.dashboard-title-area-inner`:
  1. `.dashboard-eyebrow` — "AUTONOMOUS AIR NETWORK" (plain block, no pulse-dot; dot was removed because its inline-flow offset pushed the eyebrow text out of alignment with the h1/subtitle below)
  2. `<h1>HISTORY & TIMELINE</h1>` — 48px desktop, `text-transform: uppercase; letter-spacing: 1px; word-spacing: -0.05em` (both tightened so the ampersand doesn't render with big visible gaps)
  3. `.h1-subtitle` — "9 Years of Flying. Built for the Mission."
- All three share the same x — no `|` divider, no horizontal indents, no decorative elements that would push any line's text off alignment.
- **Next to hero:** `.war-room-panel` (live flight telemetry). Stays inline with the title down to 720px (~50% of a 1440px desktop window). Below 720px stacks vertically via a dedicated `@media (max-width: 720px)` block — the earlier 1024px break was too eager and made tablet feel empty.
- Page title: "Skyways — History & Timeline" (removed "Company Timeline" branding)

## Legend Note
- Clarification text moved to the filter legend row, right-aligned: `Founded 2017 · First public Demo Day November 2025 · All publicly verified milestones`
- Uses `margin-left: auto` for right alignment within the legend flex row

## Year Label Animations
- **Year fade:** When the next year's sticky label approaches the current one, the current label fades out. Compares `labels[i+1].getBoundingClientRect().top` against the current label's `stickyTop` position with a 50px fade zone
- **Year separator line removed** — `.year-label-col::after` vertical line deleted (not needed with fade animation)
- **Year highlight function removed** — no more `.year-suffix` CSS/HTML/JS

## Year Background Gradient
- Fixed overlay div with scroll-based color transitions
- **Year-specific RGB colors** for 2016–2026 (navy/blue/teal/green palette)
- Uses linear interpolation (lerp) between adjacent years based on scroll position
- Opacity: 0.45
- Colors update as user scrolls through different year sections

## Thumbnail Color Tinting
- Canvas-based color extraction from card thumbnail images
- Samples 32×32 downscaled image, skips pixels with brightness <30 or >220
- Applies extracted color as `backgroundColor` on card at **9% opacity** (default) / **13% opacity** (hover)
- Uses `crossOrigin = 'anonymous'` for cross-origin image access
- Subtle effect — adds visual variety without overpowering card content

## Filter System
- Legend items in `.legend-row` use `data-filter` attribute matching `data-category` on event cards
- JS `toggleFilter()` function reads `data-category` from `.event-card` elements
- When adding new categories: update legend HTML, add CSS for `.legend-dot`, `.event-dot`, `.event-tag`, and highlight states
- **Layout:** `.legend-row` is a 5-column CSS grid (`grid-template-columns: repeat(5, 1fr)`) — matches `.stats-row` above so each filter sits directly under its stat counterpart. Flex layout with `flex-wrap` was wrapping on narrow desktops and misaligning with the stats.
- **No horizontal padding on `.legend-item`** — grid gap handles spacing. Horizontal padding would offset the filter text from the stat text above.
- Keyboard a11y: each legend-item has `role="button"`, `tabindex="0"`, `aria-pressed`, Enter/Space handlers, and a `:focus-visible` outline. `toggleFilter()` updates `aria-pressed` when state changes.

## Stat Source Drawers (`$46M+` table + four source lists)
- **Unified hover + tap handler** in JS (bindStatMenus IIFE near the bottom of `<script>`):
  - Desktop hover: mouseenter on `.stat-value` / `.stat-label` / `.stat-menu` opens the drawer; mouseleave on all three schedules a 120ms hide. The delay lets the cursor traverse the 8px gap between stat text and drawer. CSS `:hover` couldn't solve this — `visibility: hidden` on the hidden menu blocks pointer-events on the `::after` bridge.
  - Tap: same value/label target toggles the drawer. Tap outside closes. Contract-row clicks in the contracts-table call `scrollToContract()` which closes the drawer directly.
  - **No scroll-close.** Fires of `classList.remove('menu-open')` during the browser's scroll animation caused the drawer to stutter-then-close on slow trackpad scroll. The drawer lives in a sticky header so it travels with the viewport — auto-close on scroll solves a problem we don't have.
- **`.drawer-active` class on `#stickyHeader`** (set in `show()`, cleared in `hide()`): zeros the layout-affecting transitions on `.brand-bar`, `.logo-wrap`, `.hero-section`, `.stats-banner-inner`, `.stat-value` while a drawer is open. The drawer's `top: 100%` anchor re-computes every frame during the 220ms minimize transition; snapping instead of animating makes the drawer's anchor jump once cleanly instead of sliding under the cursor.
- **Hover zone = text ink only.** `.stat-value` and `.stat-label` have explicit `width: max-content; max-width: 100%;` — block children of a flex-column don't always shrink to content even with `align-items: flex-start`. Without this the hover zone was the full 1/5 grid column, and hovering empty space to the right of "$46M+" would open the drawer.
- **Drawer positioning per breakpoint:**
  - Desktop/tablet: `position: absolute; top: 100%; left: 0` inside its `.stat`. Width 220–260px on source drawers so they fit inside a single stat cell (~262px desktop / ~180px tablet). The 4th and 5th stat flip to `left: auto; right: 0` (with the `::before` tail pointer flipped too) so the drawer doesn't overflow the stats-banner's right edge.
  - Mobile (≤720px): non-contracts drawers still anchor to their stat (`position: absolute`, `width: min(240px, calc(100vw - 20px))`) so they emanate from the tapped stat instead of snapping to a fixed viewport position. Right-half stats (nth-child 4–5) flip to `right: 0`. The contracts-table drawer is the only one wide enough to need viewport-fixed behavior (`position: fixed; left: 8px; right: 8px`).
- **5 categories** with colors:
  - `contracts` — Blue (`--blue: #009AEB`)
  - `funding` — Green (`--green: #34A853`)
  - `product` — Purple (`--purple: #6F52AE`)
  - `milestone` — Teal (`--teal: #42C6C1`)
  - `defense` — Orange (`--orange: #FF9013`)

## Title / Copy Formatting Rules (user-visible text anywhere on the site)
- Use `|` as separator before dollar amounts and subtitles, and for "Publisher | Article" source-link labels. Never commas / em dashes / en dashes.
- Commas only for geographic/location context (e.g., "Cedar Park, TX") or for short list items inside a drawer bullet.
- **Zero** em dashes (`—`), en dashes (`–`), or arrow symbols (`→`, `←`) in any user-visible copy: card titles / details / tags, stat drawer descriptions, source link labels, contracts-table rows, or HTML entities (`&mdash;`, `&ndash;`, `&rarr;`, `&larr;`). CSS/JS comments are fine to leave alone.
- Date ranges use hyphens (`2017-18`, `2019-22`), not en dashes.
- Arrow replacements: `"→"` becomes `" to "` or `" through "` ("V2.0 to V2.6b"), never a literal arrow character or entity.
- All acronyms must be spelled out in full within each card's detail text.

### Scan before commit (catches regressions in index.html AND Firestore)
```bash
# index.html render-path scan (skips <style>, <script>, and <!-- --> blocks)
python3 -c "
import re
src = open('index.html').read()
for block in [r'<style[^>]*>.*?</style>', r'<script[^>]*>.*?</script>', r'<!--.*?-->']:
    src = re.sub(block, '', src, flags=re.DOTALL)
for bad in ['&mdash;', '&ndash;', '&rarr;', '&larr;', '—', '–', '→', '←']:
    if bad in src: print(f'HIT: {bad}')
"
# Firestore scan (user-visible fields only)
python3 -c "
import firebase_admin; from firebase_admin import credentials, firestore
firebase_admin.initialize_app(credentials.Certificate('/path/to/service-account.json'))
for d in firestore.client().collection('skyways_history_and_story').stream():
    doc = d.to_dict()
    for f in ('title','detail','tag','date_display'):
        for bad in ['—','–','→','←']:
            if bad in (doc.get(f) or ''):
                print(f'HIT id={doc.get(\"id\")} [{f}] <{bad}> {doc.get(f)[:80]}')
"
```

## Content Accuracy Notes
- Cross Park Drive move was April 2021 (per Charles Acknin correction)
- Tech Ridge move was May 2024 (per Charles Acknin correction)
- Facility after Cross Park is "Tech Ridge" in North Austin, 25,000 SF
- Founded January 2017 (Delaware incorporation Feb 13, 2017)
- V1 built in San Francisco apartment Summer 2016 (pre-founding)
- **V3 capabilities are payload OR range, not both simultaneously:**
  - 157 nautical miles range with 100 lbs payload
  - ~35 lbs cargo at 1,000 nautical miles
  - Source: internal engineering slide 49
  - Never say "100 lbs over 1,000 miles" — that implies both at once
- Event details should be thorough enough that clicking source links isn't required
- All dates and facts must match published sources
- Always run engineer feedback past the data before publishing — capability specs change
- Charles corrections override published sources — cite as "Skyways Internal — Charles Acknin"
- Engineer corrections override published sources — note correction source
- Cards without any source: cite as "Skyways Internal — No Source"
- Charles comment rounds I, II, and III all fully addressed

## Timeline Database (Firebase Firestore)
- **Firebase Project:** `marketing---earned-media-db` (shared with Earned Media DB)
- **Collection:** `skyways_history_and_story` — **65 documents** (Apr 23, 2026: added CVSI id=118 for Nov 2024 Gulf of Mexico Computer Vision Ship Intercept demo)
- **Local backup:** `Data/timeline_events_master.json` (always keep in sync with Firestore)
- **Seed script:** `scripts/seed_firestore.py`
- **Service account key:** `~/Desktop/Claude/Marketing - Earned Media DB/marketing---earned-media-db-firebase-adminsdk-fbsvc-57c1abc041.json`
- **REST API key:** `AIzaSyCSsKbZzs2xRSbZC_Ask_-8uX59GiDSnmw` (public read)
- **Doc ID format:** `[YYYY-MM] Event Title` (two-digit months, `/` replaced with `-`)
- **Categories:** contracts, funding, product, milestone, defense
- **date = sort_date** — both YYYY-MM format, always identical
- **Sources:** array of `{label, url}` objects
- **Thumbnails:** 28 unique verified URLs, no consecutive repeats, 7 Skyways fallback images rotated for variety
- When updating data: always update BOTH `timeline_events_master.json` AND Firestore

## Firestore Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Event headline |
| date | string | Yes | YYYY-MM (same as sort_date) |
| date_display | string | Yes | YYYY-MM (same as sort_date) |
| year | number | Yes | 4-digit year |
| sort_date | string | Yes | YYYY-MM for chronological ordering |
| category | string | Yes | contracts, funding, product, milestone, or defense |
| detail | string | Yes | Full description, all acronyms spelled out |
| tag | string | Yes | Short label for tag chip |
| sources | array | Yes | `[{label, url}]` objects |
| thumbnail | string | No | URL to event image |
| thumbnail_status | string | No | fallback_hero, fallback_v2_ship, etc. |

## Firestore Rules (deployed)
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /media_mentions/{document} {
      allow read: if true;
      allow write: if false;
    }
    match /skyways_history_and_story/{document} {
      allow read: if true;
      allow write: if false;
    }
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

## Charles-Only Source Audit Results (April 14, 2026)
- 16 events had Charles Acknin as sole source
- 3 upgraded with public sources (IDs 18, 19, 29)
- 11 are internal milestones with no public coverage (pre-2019 or product dev)
- 1 pending check (ID 26 — sUAS News)
- 1 confirmed separate from public coverage (ID 31 — TCP demo is NOT the RIMPAC event)
- **RIMPAC vs III MEF TCP demo:** These are two separate July 2024 events. RIMPAC was Hawaii/USS Curtis Wilbur/NAWCAD. TCP demo was Okinawa/DIU contract mod/III MEF. Public articles only cover RIMPAC.

## index.html Stats Banner (verify when data changes)
| Stat | Value | Source |
|------|-------|--------|
| Gov't Contracts | $40M+ | STRATFI $37M + Navy OTA ~$2.3M + SBIRs ~$0.8M + OTA $0.575M |
| Flights Logged | 2,950+ | Updated per internal data |
| km Flown | 40,500+ | Internal flight logs |
| Aircraft Iterations | 20+ | SBIR.gov portfolio |
| Continents | 3 | North America, Asia, Europe |
| Cost of Helicopter | 1/30th | BusinessWire press release |
| Navy Relationship | 7 yrs | ANTX 2019 to present |
| Founded | 2017 | Delaware incorporation |
| Stealth exit | November 2025 | First press Demo Day |

## Thumbnail Background on Cards
- Right-aligned, 45% width desktop / 35% mobile
- Gradient mask fades left-to-right
- Opacity: 28% default, 38% hover (desktop) / 20% (mobile)
- `overflow: hidden` on `.event-card-bg`, NOT on `.event-card`
- **64 cards, 64 unique thumbnails, 0 repeats** (deduped April 22, 2026).
  Fillers for cards without a usable article photo come from the Skyways
  newsroom's Sanity CDN (`cdn.sanity.io/images/zlpq6b94/production/…`) —
  real Skyways marketing assets, authoritative source, no licensing risk.
- When adding a new timeline card: prefer the source article's own image
  (check the card's `source_thumbnails` dict — sometimes a better
  alternative is already there but unused); if no article exists, use a
  Skyways Sanity asset that isn't already on another card. Run a quick
  repeat check: `python3 -c "..."` against the Firestore collection
  before committing.

## Earned Media Database (Firebase Firestore)
- **Project ID:** `marketing---earned-media-db`
- **Collection:** `media_mentions` — 85 documents
- **Service account key:** `~/Desktop/Claude/Marketing - Earned Media DB/marketing---earned-media-db-firebase-adminsdk-fbsvc-*.json` (gitignored)
- **Local backup:** `Data/media_mentions_master.json`
- Only update specific documents — never delete and re-seed the whole collection
- Status options: `Needs Review`, `Declined`, `Published`, `Unpublished`
- Descriptions: Skyways-focused, fact-based, no opinions, 2-3 sentences

## Media Scraper (Daily Automated)
- **Script:** `scripts/media_scraper.py`
- **Scheduled task:** `skyways-media-scraper` — runs daily at ~8am
- **Slack channel:** `#earned-media-and-mentions` (ID: `C0AQ5MMP2MR`)
- 14 RSS feeds, deduplication, Skyways mention verification
- Slack approval: "approve" → Published | "decline" → Declined | "not related" → deleted + filter learned
- Manual link drops supported in channel

## Quality Check Process (run before marking any phase complete)
1. **Data:** dates YYYY-MM, 5 valid categories, non-empty sources, no duplicates, no em dashes in titles, all acronyms spelled out
2. **Infrastructure:** JSON ↔ Firestore sync (count + titles), REST API public read, all thumbnail URLs 200 OK
3. **Accuracy:** index.html stats match data, Charles Round III covered, legend categories match data

## Newsroom → Timeline Sync
- **Action plan:** `ACTION_PLAN_NEWSROOM_SYNC.md`
- ✅ **DONE:** 5 timeline events enriched with new source links + detail text (April 14, 2026)
- ✅ **DONE:** Sanity typo fix (250k → 25k sq ft on Austin American-Statesman)
- ✅ **DONE:** Charles-only source audit — 3 of 16 events upgraded with public sources (April 14, 2026)
  - ID 29: JMSDF Destroyer Resupply — date corrected Jul→Aug 2024, 3 Japanese sources added
  - ID 19: DIU contract — renamed to Blue Water, 2 sources added, detail enriched
  - ID 18: Series A — Crunchbase added (Charles $13M figure remains authoritative over Crunchbase $15M)
- **ACTION ITEM:** ID 26 (V3 Block 1 First Flight) — check sUAS News March 2024 article for coverage
- **MEDIUM:** 9 more source links pending (Round 2 Sanity adds)
- **LOW:** `media_mentions` collection (backend only, NOT used by frontend) needs 12 new articles + status classification

## Firestore Document Management Lessons
- **`+` in document IDs:** Must URL-encode as `%2B` using `quote(doc_id, safe='')` — otherwise `+` is interpreted as a space, creating ghost documents
- **Title changes = new document:** When renaming a Firestore doc (title changes the ID), delete the old doc and create a new one — PATCH only updates fields, not the document ID
- **`|` vs `-` in doc IDs:** Original docs used `|` in IDs; replacement docs should match the format used in the collection. Always search by title field, not assumed ID format
- **Ghost document cleanup:** If a ghost appears on the live site (year "0", wrong category), it was likely created by a URL encoding bug. Find and delete via REST API

## CSS Lessons
- **Source dropdown z-index:** `.event-card` needs `z-index: 1` base value so `.event-card.sources-open { z-index: 20 }` properly stacks above siblings
- **Card shadow:** `box-shadow: 0 2px 8px rgba(0,0,0,0.1), 0 1px 3px rgba(0,0,0,0.08)` — strengthened after thumbnail tinting made lighter shadows invisible. Cards MUST have explicit `background: var(--white)` for shadow visibility.
- **Thumbnail color ≠ shadow color:** When adding color tinting to cards, apply to `backgroundColor` not `borderLeft` or gradient overlays — those look like colored shadows instead of card tinting
- **Font weight interpolation:** `font-weight: 450` works to interpolate between 400/500 weight stops — useful when swapping font families that render at different visual weights
- **Drawer anchored by `top: 100%` slides when parent animates.** The `.stat-menu`'s top recalculates every frame during a `.stat` height transition, so the drawer visually slides under the cursor. Fix: freeze the layout transitions on the header (`.drawer-active` class) while a drawer is open — the minimize snap becomes instant but only happens once.
- **Grid cells block-level children don't always shrink to content** even with `align-items: flex-start` on a flex column. When the hover/click zone needs to match the text ink, use explicit `width: max-content`.
- **CSS `:hover` bridges don't work when the target has `visibility: hidden` + `pointer-events: none`.** The `::after` invisible bridge between a trigger and a hidden menu can't catch the cursor crossing the gap. Switch to JS `mouseenter`/`mouseleave` with a short hide delay.
- **Internal banner alignment:** the red "INTERNAL ONLY" banner is a direct child of `.event-card` with `grid-column: 1 / -1` and negative horizontal margins equal to the card's horizontal padding. Previously it was nested inside `.event-content` (grid col 2) with only enough negative margin to reach the content column's edges — it stopped short of the card's true left edge.

## Spreadsheet Formatting Preferences
- Related columns must be adjacent
- Preserve existing template formatting
- New columns in their logical group, not appended

## Live Flight Stats (Airtable → Static Snapshot → UI)
- **Dashboard panel shows 3 live counters** in the war-room panel:
  - LIFETIME FLIGHTS (integer, dedup'd across tables)
  - FLIGHT TIME (SEC) (integer seconds, all-time)
  - KM FLOWN (integer km, cruise distance, all-time)
- **Data source:** `Data/live_stats.json` (static file, served by GitHub Pages)
- **Generator:** `scripts/update_live_stats.py` — pulls from Airtable base `appoHrNhrbURTxmuh`:
  - Starts with every row in `Merged flights` (already contains SKYWAYS + ANA + SKYPORTS)
  - Adds any rows from `Flights` whose `Flight #` is not already on the SKYWAYS side of Merged (catches recent flights not yet merged)
  - Sums `Flight time (s)` and `Dist Cruise (km)` for flight-time and distance totals
- **Why this dedup:** Merged flights is the rollup, but a tail of ~12 recent Skyways flights can lag behind the merge. The delta ensures archive completeness without double-counting.
- **Credentials:** `AIRTABLE_PAT` + `AIRTABLE_BASE_ID` in `.env.local` (gitignored)
- **Scheduled task:** `skyways-timeline-live-stats` runs every 15 min:
  - Regenerates `Data/live_stats.json`
  - Only commits/pushes if values changed
  - Refuses to push if any counter decreased (sanity guard)
- **Frontend behavior:** browser fetches `Data/live_stats.json?t=<now>` on load (cache-busted) and re-polls every 60 sec. On fetch failure, falls back to `STATS_FALLBACK` hardcoded in `index.html` — keep that block in sync with the most recent authoritative values so the site never shows zeros.
- **When adding/removing an Airtable flight table:** update `scripts/update_live_stats.py` (FLIGHTS_TABLE / MERGED_TABLE constants), update `STATS_FALLBACK` in index.html, regenerate snapshot, commit.
