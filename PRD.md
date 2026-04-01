# Skyways Marketing Platform — Product Requirements Document

## Executive Summary
A Firebase-backed data platform powering two public-facing products for Skyways Air Transportation Inc.: (1) an interactive company timeline and (2) an earned media newsroom. Both share Firebase project `marketing---earned-media-db` but operate as independent workstreams with separate collections, schemas, and documentation.

---

## Project Owner
**Shae Wilson** — Director of Marketing, Skyways Air Transportation Inc.

## Technical Stakeholders
- **Charles Acknin** — CEO, primary content reviewer and fact-checker
- **Web Developer** — Builds newsroom frontend on Sanity.io; receives schema + handoff docs

---

## Product 1: Skyways Timeline Page — LIVE

### Objective
Tell the Skyways story through an interactive, mobile-first timeline of company milestones — from V1 origins (2016) through future production targets (2027). Powered by Firestore, rendered dynamically from the database.

### Firestore Collection
- **Collection:** `skyways_history_and_story`
- **Documents:** 54 events (as of April 2026)
- **Doc ID format:** `[YYYY-MM] Event Title`

### Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Event headline (use `\|` separators, no em dashes) |
| date | string | Yes | YYYY-MM (always equals sort_date) |
| date_display | string | Yes | YYYY-MM (always equals sort_date) |
| year | number | Yes | 4-digit year for grouping |
| sort_date | string | Yes | YYYY-MM for chronological ordering |
| category | string | Yes | contracts, funding, product, milestone, or defense |
| detail | string | Yes | Full description, all acronyms spelled out |
| tag | string | Yes | Short label for tag chip |
| sources | array | Yes | Array of {label, url} objects |
| thumbnail | string | No | URL to event image |
| thumbnail_status | string | No | Fallback image identifier |

### Categories (5)
| Category | Color | Count |
|----------|-------|-------|
| contracts | Blue #009AEB | 10 |
| funding | Green #34A853 | 5 |
| product | Purple #6F52AE | 17 |
| milestone | Teal #42C6C1 | 11 |
| defense | Orange #FF9013 | 11 |

### Content Rules
- Accuracy is the #1 priority — every fact must be verifiable
- Charles Acknin corrections override published sources (cite as "Skyways Internal — Charles Acknin")
- Cards without sources: cite as "Skyways Internal — No Source"
- Details should be thorough enough that clicking source links isn't required
- No opinions, no editorializing — fact-based only
- All acronyms spelled out within each card's detail text
- Titles use `|` separators, never em dashes or double em dashes

### Frontend
- Single-page app: `index.html` (no build tools, no framework)
- Fetches from Firestore REST API (no SDK)
- Mobile-first (Shae tests on iPhone/Safari)
- Sticky header with stats banner and category filters
- Thumbnail background images on cards with gradient fade
- GitHub Pages hosted

### Stats Banner (keep accurate)
| Stat | Value | Verified Source |
|------|-------|-----------------|
| Gov't Contracts | $40M+ | Sum of all government awards |
| Flights Logged | 1,100+ | SBIR.gov portfolio |
| Aircraft Iterations | 20+ | SBIR.gov portfolio |
| Continents | 3 | North America, Asia, Europe |
| Cost vs Helicopter | 1/30th | BusinessWire press release |
| Navy Relationship | 7 yrs | ANTX 2019 to present |

### Completion Status
- Phase 1 (data correction): COMPLETE
- Phase 2 (Firestore seeding): COMPLETE
- Phase 3 (dynamic index.html): COMPLETE
- Phase 4 (QA + documentation): COMPLETE

---

## Product 2: Earned Media Database + Newsroom Pipeline

### Objective
Maintain a comprehensive database of every media mention of Skyways, with an automated daily scrape → human approval → newsroom publish pipeline.

### Firestore Collection
- **Collection:** `media_mentions`
- **Documents:** 85 articles (as of April 2026)
- **Doc ID format:** `[Source] Title`

### Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Article headline (always English) |
| source | string | Yes | Publication name |
| date | string | Yes | YYYY-MM-DD |
| date_precision | string | Yes | day, month, quarter, or year |
| author | string | No | Author's full name |
| description | string | Yes | 2-3 sentences, Skyways-focused, fact-based |
| link | string | No | Full URL to article |
| thumbnail | string | No | URL to article image |
| status | string | Yes | Needs Review, Approved, Declined, Not Related, Published, Unpublished |
| type | string | Yes | Story, Feature, Press Release, etc. |
| topic | string | Yes | What the article covers |
| skyways_role | string | Yes | Primary subject, Mentioned, etc. |

### Automated Pipeline
```
Daily Scrape (8:02am) → Firestore (status: Needs Review) → Slack notification
    ↓
Shae reviews in #earned-media-and-mentions
    ↓
Thread reply: "approve" → Published → Sanity.io newsroom
Thread reply: "decline" → Declined
Thread reply: "not related" → deleted + filter learned
    ↓
Manual link drops in channel → auto-scraped → thread reply for push/publish
```

### Scraping Sources (14 feeds)
Google News, Google Alerts (x2), Talkwalker, DroneLife, DroneXL, The Drone Girl, sUAS News, Defense News, UAS Weekly, Air Cargo Week, The War Zone, Helihub, eVTOL Insights

### Completion Status
- Database: COMPLETE (85 documents)
- Daily scraper: COMPLETE (14 RSS feeds, Slack notifications)
- Slack approval flow: COMPLETE
- Manual link processing: COMPLETE
- Sanity.io integration: NEXT PHASE

---

## Shared Infrastructure

### Firebase Project
- **Project ID:** marketing---earned-media-db
- **Region:** nam5 (us-central)
- **Mode:** Production (Firestore Native)
- **Auth:** Admin SDK via service account key (gitignored)
- **Public read:** REST API with key `AIzaSyCSsKbZzs2xRSbZC_Ask_-8uX59GiDSnmw`

### Key Files
| File | Purpose |
|------|---------|
| `index.html` | Timeline page (GitHub Pages) |
| `Data/timeline_events_master.json` | Local backup of timeline data (54 events) |
| `Data/media_mentions_master.json` | Local backup of media mentions (85 articles) |
| `Data/FIRESTORE_SCHEMA.md` | Timeline Firestore schema documentation |
| `Data/TIMELINE_MIGRATION_PLAN.md` | Migration plan with phase tracking |
| `scripts/seed_firestore.py` | Timeline Firestore seed script |
| `scripts/media_scraper.py` | Daily media scraper |
| `scripts/learned_filters.json` | Dynamically learned false positive filters |
| `scripts/slack_message_map.json` | Slack message → Firestore doc ID mapping |
| `CLAUDE.md` | AI operating instructions |
| `PRD.md` | This document |

---

## Operating Principles

### DOs
- Verify every fact against sources or Charles corrections
- Update BOTH JSON and Firestore when changing timeline data
- Run the 3-part quality check before marking phases complete
- Push changes to GitHub immediately after each edit
- Test all UI changes on mobile Safari
- Spell out all acronyms in card details
- Use `|` separators in titles
- At end of every session: update CLAUDE.md, PRD, MEMORY.md, and all docs
- Verify things yourself via APIs/scripts — don't ask Shae to check manually

### DON'Ts
- Don't trust old spreadsheet data without verification
- Don't put `overflow-x: hidden` on html/body (breaks Safari sticky)
- Don't put `overflow: hidden` on `.event-card` (clips source dropdowns)
- Don't batch multiple edits before pushing
- Don't plan when you should be doing — take direct action
- Don't use em dashes in titles
- Don't use CSS `:hover` for mobile interactions
- Don't skip the approval flow for media mentions
- Don't use consecutive duplicate thumbnail images
