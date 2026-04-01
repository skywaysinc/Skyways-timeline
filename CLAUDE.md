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

## Technical Lessons (Mobile Safari / iOS)
- NEVER put `overflow-x: hidden` on `html` or `body` — it breaks `position: sticky`
- NEVER put `overflow: hidden` on `.event-card` — it clips source dropdown menus. Put it on `.event-card-bg` instead.
- Use `overflow-x: clip` on individual content containers instead
- Touch devices need explicit `click`/`touchstart` handlers — CSS `:hover` doesn't work
- Source dropdown menus need: tap to open, tap-outside to close, scroll to dismiss
- `min-width` on absolutely positioned elements can cause horizontal scroll — constrain with `calc(100vw - Npx)` or `max-width`
- Always include `-webkit-sticky` for Safari sticky positioning support
- Mobile stats/filter section: keep compact (~40% smaller than desktop)
- Year label sticky offset must clear the header fade gradient (currently 210px in minimized mode)

## Filter System
- Legend items in `.legend-row` use `data-filter` attribute matching `data-category` on event cards
- JS `toggleFilter()` function reads `data-category` from `.event-card` elements
- When adding new categories: update legend HTML, add CSS for `.legend-dot`, `.event-dot`, `.event-tag`, and highlight states
- **5 categories** with colors:
  - `contracts` — Blue (`--blue: #009AEB`)
  - `funding` — Green (`--green: #34A853`)
  - `product` — Purple (`--purple: #6F52AE`)
  - `milestone` — Teal (`--teal: #42C6C1`)
  - `defense` — Orange (`--orange: #FF9013`)

## Title Formatting Rules
- Use `|` as separator before dollar amounts and subtitles (not commas or em dashes)
- Commas only for geographic/location context (e.g., "Cedar Park, TX")
- No em dashes (`—`) in titles
- All acronyms must be spelled out in full within each card's detail text

## Content Accuracy Notes
- Cross Park Drive move was April 2021 (per Charles Acknin correction)
- Tech Ridge move was May 2024 (per Charles Acknin correction)
- Facility after Cross Park is "Tech Ridge" in North Austin, 25,000 SF
- Founded January 2017 (Delaware incorporation Feb 13, 2017)
- V1 built in San Francisco apartment Summer 2016 (pre-founding)
- Event details should be thorough enough that clicking source links isn't required
- All dates and facts must match published sources
- Charles corrections override published sources — cite as "Skyways Internal — Charles Acknin"
- Cards without any source: cite as "Skyways Internal — No Source"
- Charles comment rounds I, II, and III all fully addressed

## Timeline Database (Firebase Firestore)
- **Firebase Project:** `marketing---earned-media-db` (shared with Earned Media DB)
- **Collection:** `skyways_history_and_story` — **54 documents**
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

## index.html Stats Banner (verify when data changes)
| Stat | Value | Source |
|------|-------|--------|
| Gov't Contracts | $40M+ | STRATFI $37M + Navy OTA ~$2.3M + SBIRs ~$0.8M + OTA $0.575M |
| Flights Logged | 1,100+ | SBIR.gov portfolio |
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
- 7 Skyways fallback images rotated for variety, no consecutive repeats

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

## Spreadsheet Formatting Preferences
- Related columns must be adjacent
- Preserve existing template formatting
- New columns in their logical group, not appended
