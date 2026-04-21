# Action Plan: Timeline ← Newsroom Sync

**Created:** April 14, 2026
**Status:** READY TO EXECUTE
**Context:** Cross-referenced the Skyways Timeline Firebase against the curated Sanity.io `earnedMedia` database from the Newsroom restructure project. Found source link gaps on 5 timeline events and a backend `media_mentions` collection that's out of sync.

### Architecture Note
- **`skyways_history_and_story`** (56 docs) → Powers the LIVE timeline website via Firestore REST API. This is the collection that matters.
- **`media_mentions`** (85 docs) → Backend-only database for the media scraper / Slack approval pipeline. NOT used by any frontend. Lower priority to update.

---

## TASK 1: Add Source Links to 5 Timeline Events ✅ DONE (April 14, 2026)

**Priority: HIGH** — These are the actual timeline cards users see on the live site. Several had thin sourcing — our newsroom deep search found high-quality external articles that verify and enrich these events. Updated in both `timeline_events_master.json` and Firestore.

| Timeline Event (ID) | Current Sources | Add These |
|---|---|---|
| **Start of Navy OTA Spiral Dev** (#36 / 2020-01) | Skyways Internal only | FlightGlobal "US Navy studies resupplying ships/subs" (Nov 2020) + IUS "Small UAV Takes on Big Sea Missions" (Nov 2020) |
| **Carrier Deck Trials \| USS Ford** (#13 / 2021-02) | War Zone, USNI News | Maritime Executive "Carrier USS Ford Tests Out Air Cargo Drone" (Aug 2021) + FlightGlobal "US Navy eyes programme of record" (Aug 2021) |
| **Ship-to-Ship Autonomous Flights** (#15 / 2021-07) | USNI News only | Breaking Defense "Navy conducts live test of resupply drones" (Nov 2021) |
| **200+ NM Cargo Delivery Demos** (#22 / 2022-12) | DroneDJ, DroneXL | FlightGlobal "UAVs deliver cargo to ship for first time" (Dec 2022) + Maritime Executive (Dec 2022) + USNI News "Navy to Deploy Up to Four Cargo Drones" (Apr 2022) |
| **ANA Completes Okinawa Trials** (#44 / 2026-03) | Payload Asia, TravelMedia India | ANA Holdings official press release: https://www.anahd.co.jp/group/en/pr/202603/20260305.html |

**Steps:**
1. Update each event's `sources` array and `source_urls` object in `timeline_events_master.json`
2. Add `source_thumbnails` for new sources where available
3. Sync to Firestore `skyways_history_and_story` collection
4. Verify source dropdowns render correctly on live site (desktop + mobile)

**New source URLs:**
- Breaking Defense: https://breakingdefense.com/2021/11/navy-conducts-live-test-of-resupply-drones-for-ashore-at-sea-missions/
- FlightGlobal (Nov 2020): https://www.flightglobal.com/military-uavs/us-navy-studies-resupplying-ships-and-submarines-using-small-uavs/141175.article
- FlightGlobal (Aug 2021): https://www.flightglobal.com/military-uavs/us-navy-eyes-programme-of-record-for-cargo-drones-to-resupply-ships/144776.article
- FlightGlobal (Dec 2022): https://www.flightglobal.com/military-uavs/uavs-deliver-cargo-to-us-navy-ship-at-sea-for-first-time/151684.article
- Maritime Executive (Aug 2021): https://www.maritime-executive.com/article/video-carrier-uss-ford-tests-out-air-cargo-drone
- Maritime Executive (Dec 2022): https://www.maritime-executive.com/article/video-u-s-navy-s-drone-logistics-trials-take-flight
- USNI News (Apr 2022): https://news.usni.org/2022/04/12/navy-to-deploy-up-to-four-cargo-drones-on-an-aircraft-carrier-this-year
- IUS (Nov 2020): https://insideunmannedsystems.com/small-uav-takes-on-big-sea-missions-resupply-warships-and-submarines/
- ANA HD: https://www.anahd.co.jp/group/en/pr/202603/20260305.html

---

## TASK 1B: Enrich Timeline Event Details from Newsroom Findings ✅ DONE (April 14, 2026)

All three enrichments applied to both `timeline_events_master.json` and Firestore:
- ANA Okinawa: Added precise flight times (1h04m / 1h01m) + temperature-controlled cargo detail
- Carrier Deck Trials: Added "80% of critical spare parts needs" stat + 2 new source links
- 200+ NM Demos: Added "90% of critical mission failures under 20 lbs" stat + 3 new source links

### Sanity Correction (DONE ✅ — April 14, 2026)
- **Austin American-Statesman** description: Fixed "250,000 sq ft" → "25,000 sq ft" (was a typo — extra zero). Timeline had the correct value per Charles Acknin.

---

## TASK 1C: Charles-Only Source Audit ✅ DONE (April 14, 2026)

Audited all 16 timeline events that had "Skyways Internal — Charles Acknin" as the sole source. Cross-referenced against Sanity earnedMedia database and web searches.

**Upgraded (3 events):**
| Event | Sources Added |
|---|---|
| ID 29 — JMSDF Destroyer Resupply | JMSDF PAO (X/Twitter), drone.jp, trafficnews.jp. Date corrected Jul→Aug 2024 per JMSDF official post (Aug 15-25). |
| ID 19 — DIU/USN Contract | Inside Unmanned Systems, Potomac Officers Club. Title renamed to "Blue Water Maritime Logistics UAS." Detail enriched with 50-lb/250-mi target, 95% parts stat, CV landing. |
| ID 18 — Series A $13M | Crunchbase confirms Jan 2022 Series A. Note: CB lists $15M; Charles's $13M is authoritative. |

**No public sources available (11 events):**
IDs 7, 16, 17, 21, 23, 30, 45, 103, 104, 105, 106 — all predate Skyways' public press footprint (earliest coverage Oct 2019) or are internal engineering milestones.

**Pending check (1 event):**
- ID 26 (V3 Block 1 First Flight, Feb 2024) — sUAS News article from March 2024 ("Skyways V3") may cover this. Needs content verification.

**Confirmed separate from public coverage (1 event):**
- ID 31 (DIU TCP Demo / III MEF, Jul 2024) — NOT the same as RIMPAC 2024. RIMPAC was Hawaii/NAWCAD/USS Curtis Wilbur (Jun 19-24). TCP demo was Okinawa/DIU contract mod/III MEF. No public coverage of the TCP demo specifically.

**Flagged as unverifiable (1 event):**
- ID 30 (JASDF Inter-Island Resupply) — Exhaustive search (23+ queries, English and Japanese) found zero public evidence. Title prefixed with `[NOT PUBLIC / NO EXTERNAL SOURCES]` and audit note added.

### TASK 1D: JMSDF Deep Search Results (April 14, 2026)

Comprehensive search for all publicly available Skyways + JMSDF information. Found 7 unique sources organized by mission:

**JMSDF Autonomous Destroyer Resupply (Aug 2024 — DD-115 Akizuki):**
1. JMSDF Public Affairs Office (X/Twitter) — official post confirming Aug 15-25 drone trials at Funabashi wharf, DD-115 Akizuki
2. drone.jp — Japanese coverage with flight details (23km, 40-min autonomous flights)
3. Yahoo Japan News — syndicated coverage of JMSDF trials
4. trafficnews.jp — Japanese transportation trade coverage
5. Asagumo Shimbun — Japanese defense newspaper coverage
6. Charles Acknin LinkedIn — operational context (food delivery, autonomous resupply)

**Key Details Confirmed:**
- Ship: DD-115 Akizuki (Akizuki-class destroyer)
- Location: Funabashi wharf, Chiba Prefecture
- Date: August 15-25, 2024 (NOT July as originally listed)
- Distance: ~23 km flights, ~40 minutes each
- Cargo: Food supplies
- Mode: Fully autonomous

**JASDF Inter-Island Resupply (ID 30):**
- Zero public sources found after 23+ search queries in English and Japanese
- Flagged as `[NOT PUBLIC / NO EXTERNAL SOURCES]` — remains Charles-only

---

## TASK 2: Add Round 2 Source Links to Timeline Events (When Complete)

**Priority: MEDIUM** — Depends on completing Newsroom Round 2 adds first (9 articles pending in Sanity action plan).

Once verified and added to Sanity, also add as source links on these timeline events:

| Timeline Event | New Source to Add |
|---|---|
| RIMPAC 2024 (#27) | The Aviationist (Jul 2024) |
| Project ULTRA (#36) | Avionics International (Jul 2025) |
| Carrier Deck Trials / Ship-to-Ship (#13, #15) | Janes 4th article (Nov 2021) |
| Start of Navy OTA Spiral Dev (#36) | Defense Post (Nov 2020) |
| 200+ NM Cargo Delivery Demos (#22) | Defense Post (Dec 2022) |

---

## TASK 3: Sync `media_mentions` Backend Database

**Priority: LOW** — This collection doesn't power the live site. It feeds the media scraper/Slack pipeline. Update when time permits.

**4a. Add 12 missing articles** (from Sanity Round 1 + podcasts + ANA HD) to `media_mentions_master.json` and Firestore.

**4b. Classify all 85 entries by status.** Currently all show `Needs Review`. Apply newsroom audit criteria:
- `Published` — Original editorial, Skyways primary/co-primary
- `Wire Pickup` — Verbatim syndication (Yahoo Finance, MarketWatch, AP News, Reuters, etc.)
- `Brief` — Skyways mentioned in passing
- `Press Release` — Skyways' own PRs
- `Dead Link` — 404s
- `Declined` — Doesn't meet criteria

**Known wire pickups:** Yahoo Finance, MarketWatch, AP News, Reuters/TradingView, Street Insider, Silicon UK, Airframer, Defence Industries, UAS Weekly (all $37M contract syndication). Also Yahoo Finance ($5M debt) and Unmanned Systems Technology (offshore wind GlobeNewswire rewrite).

**Note:** The timeline may want to KEEP all mentions for tracking total coverage breadth. The status field classifies them — doesn't mean delete.

---

## Reference Links

- **Newsroom action plan:** `~/.claude/projects/-Users-shaewilson-Desktop-Claude-Marketing---Earned-Media-DB/memory/action_plan_media_features_round2.md`
- **Newsroom criteria:** `~/.claude/projects/-Users-shaewilson-Desktop-Claude-Marketing---Earned-Media-DB/memory/criteria_media_features.md`
- **Timeline master JSON:** `/Users/shaewilson/Desktop/Claude/Skyways Timeline/Data/timeline_events_master.json`
- **Media mentions JSON:** `/Users/shaewilson/Desktop/Claude/Skyways Timeline/Data/media_mentions_master.json`
- **Sanity API:** Project `zlpq6b94`, Dataset `production`
- **Firebase:** Project `marketing---earned-media-db`
- **Live timeline:** GitHub Pages (skyways-shaewilson.github.io)
