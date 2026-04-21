# Skyways Timeline — Migration Plan

## Overview
Migrate the Skyways Timeline from hardcoded HTML + Excel to a Firestore-backed system. Address all Charles comment rounds in the process.

---

## Phase 1: Address Charles Comments (Data Only) — COMPLETE
**Goal:** Produce a corrected, verified JSON file with all timeline events.

- [x] Fix all Charles Round I, II, and III comments
- [x] Add missing events (Series A, JSDF, V1 origin, V2.0/V2.1/V2.2 build phases, White Sands demo)
- [x] Break V3 into separate milestone rows
- [x] Remove incorrect entries
- [x] Output: `Data/timeline_events_master.json`

---

## Phase 2: Create Firestore Collection + Seed — COMPLETE
**Goal:** Seed `skyways_history_and_story` collection.

- [x] Define schema (title, date, sort_date, category, detail, sources, thumbnail)
- [x] Write seed script (`scripts/seed_firestore.py`)
- [x] Seed all events with `[YYYY-MM] Event Title` doc IDs
- [x] Verify all source URLs
- [x] Assign varied thumbnails (no consecutive repeats)
- [x] Deploy Firestore security rules (public read, no write)

---

## Phase 3: Rebuild index.html to Read from Firestore — COMPLETE
**Goal:** Timeline page pulls data from Firestore dynamically.

- [x] Fetch from Firestore REST API (no SDK needed)
- [x] Render cards dynamically with category dots, tags, source dropdowns
- [x] Thumbnail background images with gradient fade
- [x] 5 category filters (contracts, funding, product, milestone, defense)
- [x] Preserve sticky header, year labels, mobile Safari behavior
- [x] Stats banner verified accurate ($40M+, 1,100+ flights, 7 yrs Navy, etc.)
- [x] Push to GitHub

---

## Phase 4: Final QA + Documentation — COMPLETE
**Goal:** Full quality audit and documentation update.

- [x] Data quality check: 0 issues (dates, categories, sources, duplicates, acronyms)
- [x] Infrastructure check: JSON ↔ Firestore sync, REST API working, 28 thumbnail URLs verified
- [x] Accuracy check: all stats match, Charles Round III covered, categories aligned
- [x] All broken thumbnail URLs replaced
- [x] Updated: CLAUDE.md, PRD.md, FIRESTORE_SCHEMA.md, MEMORY.md, this migration plan

---

## Current State (April 2026)
- **54 documents** in Firestore, synced with `timeline_events_master.json`
- **5 categories:** contracts, funding, product, milestone, defense
- **12 years covered:** 2016–2027
- **28 unique thumbnail URLs**, all verified working
- **index.html** reads from Firestore REST API, no hardcoded events
- All Charles comment rounds (I, II, III) fully addressed
