# Session Log — April 23, 2026

Continuation of the line-by-line cleanup + comprehensive contract audit kicked off April 21.

## What landed today

| Commit | Summary |
|---|---|
| [d173080](https://github.com/skywaysinc/Skyways-timeline/commit/d173080) | Contract audit fixes: ID 9 award amount $2.07M → $575K (award-date base, not ending total); ID 109 category contracts → funding |
| [244d3da](https://github.com/skywaysinc/Skyways-timeline/commit/244d3da) | Restore card thumbnails: renderer fallback to `source_thumbnails` (top-level `thumbnail` field had been wiped by Apr 21 `set(merge=False)` sync) |
| [bb5e2f6](https://github.com/skywaysinc/Skyways-timeline/commit/bb5e2f6) | Contract title standardization (6 entries) + 3 Navy DLA PO timeline cards (id=115/116/117 with placeholder amounts) + expanded $46M+ drawer with "Additional U.S. gov agreements" sub-section |
| [d5e7c1f](https://github.com/skywaysinc/Skyways-timeline/commit/d5e7c1f) | Year-section drawer-clipping fix using `:has()`; ID 101 source → Charles Acknin; ID 109 source → Shae Wilson |
| [7285a97](https://github.com/skywaysinc/Skyways-timeline/commit/7285a97) | Search bar overlap fix: suppressed native webkit search-clear button + widened input padding |
| [8a03442](https://github.com/skywaysinc/Skyways-timeline/commit/8a03442) | **Deep-search payoff**: filled in actual dollar amounts for all 4 previously-undocumented contracts |

## Contract audit — all amounts now verified

After deep Drive + Slack search:

- **NSLP-CRADA-NAWCADPAX-25-533** (id=113) — full agreement found: signed Mar 18-20, 2025 by Charles Acknin and J.E. Dougherty IV (RDML, USN, Commander NAWCAD). Title "SKYWAYS V2.6 UNMANNED AERIAL SYSTEM DEMONSTRATION." Article 16: no funds transferred. Article 19: publicly releasable. Equipment: 3 V2.6 aircraft (AV1/AV2/AV3) + 6 GCS + 3 TS Shore + 3 TS Ship + 4 VTOL battery packs + 3 GSE kits.
- **DGPS PO PFR006115** (id=115) — **$71,070.00** (DGPS hardware $11,385 + Engineering $48,185 + SOE Freight $11,500), Mar 15, 2023
- **SATCOMv2 PO PFR007234** (id=116) — **$203,735.00** (SKYTRAC DLS-100 hardware $86,595 + V2.6b SATCOMv2 NRE/Test $105,110 + Integration $4,830 + SPP-720M airtime $7,200), May 26, 2023
- **Intelligen PO PFR007445** (id=117) — **$79,545.00** (V2.6b Intelligen onboard start $36,765 + AV1-3 Integration/testing $42,780), Jun 15, 2023

**$46M+ banner total updated**: $45,967,784.18 → **$46,322,134.18** (+$354,350 from 3 DLA POs).

Drawer restructured: 13 funded contracts in main table, NSLP-CRADA in "Additional U.S. gov agreement (non-monetary)" sub-section below total. 3 pill states: Internal (orange), Public (green), Lease (no $).

## Stats audit — flagged items resolved

| Flag | Resolution |
|---|---|
| ID 22 "90% / 20 lbs NAWCAD" unverified | Kept (Charles authority) + audit note added to bullet |
| ID 27 "Three Skyways aircraft" RIMPAC | Reworded to "Skyways aircraft (3 of 6 total UAS launched alongside PteroDynamics X-P4)" |
| ID 36 "first BVLOS without chase plane" | Rephrased to match Skyways newsroom: "first unmanned, fully autonomous BVLOS cargo flights between two U.S. airports" |
| ID 13 "500 mi / 30 lb V2.5" unverified | Kept (Charles authority) + Round IV charles_corrections note |
| ID 19 "50/250/95% DIU program target" | Kept (Charles authority) + Round IV note + per-Charles inline in bullet |
| **"1/30th cost of helicopter" source unidentified** | **RESOLVED**: confirmed DroneXL Feb 7, 2026 as canonical source; drawer updated with full-precision dollars + $100/hr at-scale projection + DroneXL link added |
| BVLOS acronym not spelled out on id=36 | Fixed: "BVLOS" → "Beyond Visual Line of Sight (BVLOS)" first use |

## Bug fixes

- **Card thumbnails restored**: every card had been blank since Apr 21 sync. Root cause: `set(merge=False)` from local JSON missing the top-level `thumbnail` field wiped Firestore. Fix: renderer now falls back to first URL in `ev.source_thumbnails` when `ev.thumbnail` is empty.
- **Search bar layout overlap**: native `<input type="search">` clear X was rendering inside the search bar between count digits. Suppressed via `::-webkit-search-cancel-button { display: none }` + widened input padding.
- **End-of-year drawer clipping**: source dropdowns at the BOTTOM of a year section were hidden under the next year's cards (because `content-visibility: auto` creates per-section stacking contexts). Fix: `.year-section:has(.event-card.sources-open) { z-index: 50 }` lifts the year section above siblings while a drawer is open.

## Memory archive updates (saved Apr 23 to `~/.claude/.../memory/`)

- `feedback_research_patterns.md` — new 7-step deep-search drill-down for hidden gov contracts; Drive query-syntax fixes; Slack-result subagent-delegation pattern; WebSearch quote-attribution caveat
- `reference_skyways_contract_archive.md` — 13 contracts ($46.3M) + NSLP-CRADA full agreement + Navy OTA mod-by-mod progression + 5 candidate CRADA valuations
- `reference_timeline_css_quirks.md` — `content-visibility` stacking-context fix via `:has()`; native search-input clear-button suppression; renderer schema-tolerance fallback pattern
- `process_timeline_data_sync.md` — `set(merge=False)` wipes-fields critical warning; orphan-cleanup pattern; current count = 64
- `project_timeline_frontend.md` — current state (64 docs, $46.3M banner, Vercel reconnected)
- `project_vercel_disconnect.md` — marked RESOLVED Apr 22; runbook preserved
- `feedback_collaboration_patterns.md` — 4 new failure modes from this session

## Current open thread

Shae is confident there's a SPECIFIC NSLP-CRADA dollar amount somewhere I haven't found yet (not the Navy build cost, not insurance, not BOM, not export license). See `STATS_AUDIT.md` open items.

### Exhaustive internal-search log (Apr 23, 2026)
Searched for a specific NSLP-CRADA dollar amount across these sources, **all returning zero direct CRADA-attached $ value**:

**Drive** (Google Drive MCP, `fullText contains '...'` queries, all paired with `CRADA`, `LP-CRADA`, `NSLP-CRADA`, `NSLP-CRADA-NAWCADPAX-25-533`, `AV1 AV2 AV3`, or `Macchione`):
- `cost`, `value`, `amount`, `worth`
- `Government Furnished`, `GFP`, `GFE`, `Acquisition Cost`
- `in-kind`, `cost share`, `cost-share`
- `Navy owned`, `pitch deck`, `investor`
- `Research Plan`, `Attachment A`
- `aircraft value`, `Navy aircraft`

**Drive folder reads**: `2025 LP-CRADA` folder (only contains the 2 CRADA PDFs — FINAL + draft; no appendix, no research plan, no valuation memo).

**Drive full-PDF reads**: Full signed `NSLP-CRADA-NAWCADPAX-25-533 Skyways - FINAL.pdf` (Article 16: "No funds are transferred"). `Attachment 2, Government Furnished Property.pdf` (only ZPX-B $12k × 3 populated; aircraft/GCS/TS unit-cost fields left blank). P00003 SF30 signed mod ($464k→$1.56M for AV2 spiral). P00006 SF30 signed mod ($1.92M→$1.97M for SATCOM). V2.6/V3B1 BOM Cost Summary spreadsheet (128,851 chars — audit-quality sweep via subagent returned ZERO matches for CRADA/Navy/GFP/AV1-3/acquisition/fair-value labels).

**Slack** (skywaysworkspace, `in:` and free-text queries with CRADA, NSLP, LP-CRADA, AV1/AV2/AV3 + cost/value/amount/worth):
- Channels swept: `#stratfi`, `#team-finance`, `#weekly-leads-meeting`, `#sales-government`, `#sales-commercial`, `#swe-general`, `#v2`, `#shop`, `#avionics`, `#flight-testing`, `#blue-uas-cert`, `#progress`, `#conferences`, `#the-office`, `#brand-and-marketing`, `#jmsdf-demo-coordination`, `#gomex-cvsi-2024`, `#project-ultra-2025`, `#skyports-support-internal`, `#regulations`
- `from:@Charles CRADA`: 2 results, both about config/change-tracking (no $)
- `Macchione CRADA dollar OR amount OR value`: 10 results, none attach a CRADA $ figure
- `CRADA Bill Macchione value`: 15 results (mostly general BD context)
- `"in-kind" OR "cost share" OR "cost-share" CRADA`: 0 results
- `CRADA "$"`: 0 results

**Decks read**: DoW 101 (Feb 2026), Brand Strategy 2025, MarCom Plan FY 2026, MarCom Summary Q3 2025, Project ULTRA Readiness Review, RIMPAC 2024, V3B2 PDR, V3B2 CDR, Skyways AFWERX Weekly. None contain a CRADA-specific $.

**Defense History Article** (`SKY-022_Defense_History_Article_V5`): mentions BVLOS + STRATFI + 100% milestone delivery but no CRADA $ figure.

### Second-pass sweep (additional sources checked, all returning zero CRADA-attached $)
- **Gmail** (3 queries: `CRADA AND ($ OR cost OR value OR amount OR worth)`, `"NSLP-CRADA" OR "LP-CRADA" OR "NSLP CRADA"`, `Macchione (lease OR CRADA OR aircraft OR value OR cost)`, `"aircraft value" OR "replacement cost" OR "insured value" AND (Navy OR CRADA OR V2.6)`): only Pax-AIRSHOW threads, zero CRADA-financial threads. From-filter `from:william.a.macchione.civ@us.navy.mil`: 0 results.
- **Apple Notes** (50-note sweep + read of "Bill x Shae" Apr 7 1:1 note): note covers Houma/Part 108/SORA/LinkedIn invites; no CRADA $.
- **TAA Transmittal Letter** (master Skyways gov contract index): NSLP-CRADA-NAWCADPAX-25-533 is **NOT in the index** (index ends at "2025 OTA RPED Project ULTRA"). Confirms CRADA is tracked separately from priced contracts.
- **Drive search by V2.6 part number `0000039-501`**: returned only NSLP-CRADA PDFs, the GFP attachment (Unit Acquisition Cost field blank for the V2.6 aircraft entries, only ZPX-B IFF transponder shows $12k), and the equipment manifest sheet (qty only, no $).
- **Asana** (3 queries: CRADA, Macchione, "Navy lease V2.6"): **0 tasks** in workspace.
- **Slack DMs** (`CRADA $ value cost amount` in IM/MPIM channels): zero CRADA-financial messages — only marketing/budget discussions.
- **Slack all channels** (`"NSLP" OR "LP-CRADA" OR "limited purpose CRADA"`): **0 results** workspace-wide.
- **Govt Counteroffer folders** (`Govt Counteroffer 02-26-2025` and `Govt Counteroffer 04-08-2025` — same timeframe as CRADA signing): contents are 100% STRATFI counteroffer (Total $29,125,555.26), not CRADA.
- **WebSearch** (`NAWCAD NSLP-CRADA-NAWCADPAX-25-533 Skyways value dollar amount`, `"Skyways" CRADA Navy V2.6 aircraft value lease 2025`): the agreement number is not publicly indexed by Google with any $ figure.

### Most defensible candidate values (unchanged after second-pass sweep)
- **CRADA agreement**: $0 (Article 16: "No funds are transferred")
- **GFP attachment unit acquisition cost field for V2.6 aircraft**: BLANK in the only GFP doc that exists (Attachment 2 to BWUAS contract; the Navy never priced the aircraft on the document)
- **Navy build cost** (the $ Navy paid Skyways to build AV1/AV2/AV3): **$2,066,701.73** total per signed P00007 mod — this is the closest thing to a "CRADA equipment cost basis" that exists as a hard signed-doc figure
- **Insurance**: $2,250,000 ($750k × 3 aircraft, hull insurance)
- **BOM**: $681,023 ($227,007.68 × 3 aircraft, internal cost-to-build)
- **Export license**: varies $300k-$700k per aircraft (regulatory declared value)
- **3 DLA POs combined**: $354,350 (DGPS + SATCOMv2 + Intelligen — but these are payloads, not the CRADA aircraft)

### RESOLVED — V2.6 hull-insurance valuation found (Apr 23, 2026)

After Shae's hint to "try different search terms maybe its not under crada," the alternate-framing sweep surfaced the figure in **Slack `#skyways-skyports`** (Oct 31 to Nov 28, 2024). Harry Plested (Skyports) asked Avery Walker for the V2.6 hull-insurance value before scoping a Skyports policy, and Isaac Roberts (Skyways VP Commercial) replied with Skyways' own internal-coverage standard:

> "we have our own policies on the aircraft to cover ourselves, and we use the **coverage amount of $1M USD per aircraft**. I think this would be the target, but **750k USD would suffice as the total amount**." — Isaac Roberts, 2024-11-04

> "the quote i have received is for **750K USD**." — Harry Plested, 2024-11-28 (Skyports' export quote)

> Margaret Prentice confirmed the figure flowed onto Skyways export paperwork.

**Applied to the 3 CRADA-leased aircraft (AV1, AV2, AV3):**

| Per-aircraft basis | Total for AV1+AV2+AV3 | Source |
|---|---|---|
| **$1M** (Skyways standard target) | **$3,000,000** | Isaac Roberts, Slack #skyways-skyports, 2024-11-04 |
| **$750K** (acceptable minimum / Skyports export-quote) | **$2,250,000** | Harry Plested, Slack #skyways-skyports, 2024-11-28 |

Of the two, **$3M total ($1M × 3 aircraft)** is the cleaner, more memorable round number tied directly to Skyways' own hull-insurance standard. **$2.25M** is the conservative export-paperwork figure.

### Why earlier sweeps missed it
- Slack search anchored on `CRADA` returned zero — the figure lives in a Skyports lease/insurance discussion, not a CRADA discussion.
- Drive search anchored on `hull insurance` / `aircraft insurance` returned zero — the figure was never written into a Drive document, only into Slack.
- The thread parent was `#skyways-skyports` (commercial customer channel), not a defense / Navy / CRADA channel.
- Searching `"AV1" OR "AV2" OR "AV3" insurance value cost` in Slack returned zero — because the AV1-3 designations are Navy-specific and the hull-insurance discussion just said "the aircraft" generically.

### Lesson for next time
For a "hidden" valuation tied to a Navy lease/CRADA: search **commercial-customer channels** (Skyports, ANA, DSV) first, since Skyways' standard pricing structure for commercial leases (hull-insurance value, monthly lease rate, flight-hour rate) is reused as the cost-basis reference for all aircraft including Navy-owned units. The CRADA itself is structured as $0 (no funds transferred per Article 16), so the implicit valuation lives in the commercial-pricing equivalents.

### Bonus: ANA lease-pricing structure (also surfaced this sweep)
Same week as the CRADA was signed, Skyways executed an ANA Holdings lease (file `1qlVQrdcdb5UCcIqTBo4vvkU5SNnCII2t`, dated 4/22/2025). Pricing structure for ANA's 2 V2.6 aircraft + 2 V3 Block 2 aircraft over a 24-month term:
- **$7,500/month per aircraft** (recurring fee)
- **$450/flight hour per aircraft**
- **Minimum $18,000/month per aircraft** (i.e. 40 flight hours/month minimum)

If Shae wanted to express CRADA value on a service-equivalent basis (rather than hull-insurance basis), 3 aircraft × 24 months × $18,000/month minimum = **$1,296,000/year** equivalent service value, or **$2,592,000** over a 2-year demo period.

### Final candidate values (full set)
- **$3,000,000** — 3 × $1M Skyways standard hull-insurance target (most likely "the number Shae remembered")
- **$2,250,000** — 3 × $750K Skyports export-quote / acceptable minimum
- **$2,592,000** — 24-month ANA-equivalent service value (3 × $18K/mo × 24 mo)
- **$2,066,701.73** — Navy build cost (P00007 mod total — what Navy paid Skyways to build the leased equipment)
- **$681,023** — BOM build cost ($227K × 3)
- **$0** — per CRADA Article 16 ("No funds are transferred")

## Total entries on collection: 65
- 60 original (after Apr 21 Tier 1-4 cleanup)
- +1 V3 Block 2L placeholder (id=114)
- +3 Navy DLA POs (id=115 DGPS, id=116 SATCOMv2, id=117 Intelligen)
- +1 CVSI Nov 2024 (id=118, added Apr 23 evening)

---

## Evening session — storytelling rewrite + correction audit

### Copywriting/storytelling overhaul

Applied a framework (HOOK · TURN · STAKES, 7 principles + checklist) to the narrative copy on the timeline. Framework now saved as memory reference at `reference_storytelling_framework.md`.

| Commit | Summary |
|---|---|
| [f677471](https://github.com/skywaysinc/Skyways-timeline/commit/f677471) | Rewrite era taglines as prose, fact-checked, in Charles's voice. Fixed Era 1 factual errors (Delaware incorp not Austin, Navy demos are 2019). Era 2-4 taglines restructured to single-arc prose with connective tissue. |
| [04898f9](https://github.com/skywaysinc/Skyways-timeline/commit/04898f9) | Retitle 3 eras: DoW Operation Molding → **Earning the Navy**, Platform Improvements → **V3 and Allies**, Public Emergence → **Program & Public**. Founding and Scaling kept. |
| [b609c35](https://github.com/skywaysinc/Skyways-timeline/commit/b609c35) | Rewrite 11 year headlines as prose, single-subject + parallel verbs. Replaced pipe-separated noun lists with story beats. Fixed 2017 false "Navy demos" and 2026 "Japan ops scale" rule violation. |

Current era arc: **Founding → Earning the Navy → V3 and Allies → Program & Public → Scaling**

### Storytelling gaps backlog

| Commit | Summary |
|---|---|
| [449e812](https://github.com/skywaysinc/Skyways-timeline/commit/449e812) | Added `docs/STORYTELLING_GAPS.md` — 20-gap table ranked P0-P3 for investor + wider-public story. P0s include capital-efficiency ratio, Charles's hobby-kit origin, mission-impact framing, PoR glossary, competitive moat. |

### Event-by-event correction audit (Tom Martin + Charles Excel rounds)

Gathered Tom Martin ("T-Money," `U04ALK2USCS`, `tom@skyways.com`) identity and his 5 Slack corrections (Apr 2–6, 2026). Extracted all 40 Charles Excel corrections (Rounds II+III, Mar 19 – Apr 1, 2026). Saved consolidated audit to `docs/EVENT_CORRECTIONS_AUDIT.md` with per-item verification status.

**Automated regex sweep across all 64 (now 65) events** against every removal pattern and every required-presence check. Found 3 gaps; resolved all 3.

| Commit | Summary |
|---|---|
| [b864a9c](https://github.com/skywaysinc/Skyways-timeline/commit/b864a9c) | Fix id=27 RIMPAC (removed PteroDynamics X-P4 + "3 of 6" framing per Charles R3) and id=31 III MEF (clarified stateside, added 6hr/300+mi/10 bags blood 3-6 °C per Charles R2). Mirrored to Firestore. Added `EVENT_CORRECTIONS_AUDIT.md`. |
| [faa69b3](https://github.com/skywaysinc/Skyways-timeline/commit/faa69b3) | Add CVSI event (id=118, Nov 2024 Gulf of Mexico demo, Inside Unmanned Systems public source). Update id=43 Leadership to include "~39 employees end of 2025" (Anthony-confirmed via DM Mar 19). |
| [1953ab8](https://github.com/skywaysinc/Skyways-timeline/commit/1953ab8) | Final era cleanup: CVSI thumbnail swapped to skyways.com fallback (non-Sanity per Shae); id=109 Series B "production scaling" → "production ramp" for Era 5 reservation rule. |

### Era-by-era audit outcome

All 45 Charles/Tom correction items verified across 65 events:

| Era | Events | Status |
|---|---|---|
| Era 1 Founding (2016-2018) | 11 | ✓ all honored (pattern sweep clean) |
| Era 2 Earning the Navy (2019-2022) | 18 | ✓ all honored |
| Era 3 V3 and Allies (2023-2024) | 14 + CVSI added | ✓ all honored after 3 fixes today |
| Era 4 Program & Public (2025-2026) | 21 | ✓ all honored after headcount + Series B polish |
| Era 5 Scaling (2027+) | 0 live | n/a (upcoming) |

### Memory archive updates (Apr 23 evening)

- `reference_tom_martin_feedback.md` — new: Tom Martin identity, voice pattern, V3-OR-not-AND global rule, standing corrections
- `reference_storytelling_framework.md` — new: HOOK · TURN · STAKES framework + 7 principles + checklist for future narrative copy
- `MEMORY.md` index — two new reference entries added

### Flagged for separate future session (not Charles/Tom feedback)

- ~~63 pre-existing em/en dashes live in source labels~~ — **RESOLVED same session, see next section.**
- Tom's Apr 23 re-review reaction was `:eyes:`; no new corrections yet at time of writing.
- ANA Oct 2025 row (id=41) was live before this session; should reconfirm with Jessica before next press cycle (Charles C-16 compliance hold).

---

## Em-dash cleanup + source-visibility banner rules

Two related pieces of work triggered by the earlier em-dash flag.

| Commit | Summary |
|---|---|
| [4e5b2ec](https://github.com/skywaysinc/Skyways-timeline/commit/4e5b2ec) | Em-dash cleanup (63 instances) across source labels + source_urls keys. Mirrored to Firestore (47 docs updated). Contracts stat drawer gained "Internal = no public press release found" disclaimer. New `docs/README.md` folder map. |
| [09b7ff8](https://github.com/skywaysinc/Skyways-timeline/commit/09b7ff8) | Mobile header aircraft bg fix (Shae's concurrent edit) bundled with banner refactor from same file-session. |

**Source-visibility banner rules formalized into four states** (see `docs/SOURCE_VISIBILITY_RULES.md` for the canonical reference):

| State | Banner color | Trigger |
|---|---|---|
| Internal only | **Red** `#d93025` | Skyways Internal + contract #/CLIN/PO, or `[NOT PUBLIC` flag. Military contract pattern. |
| Mixed | **Orange** `#c05621` | Public source validates card + internal-only addendum |
| Charles-only | **Beige** `#d4c18c` | Charles Acknin / No Source / Not Published is sole source |
| Fully public | no banner | External press only |

Code changes: `classifySource(label)` function added (3 buckets: internal / charles-approved / external). Separator regex now accepts `|`, em dash, en dash, and hyphen so it works after the em-dash cleanup. Charles-only cards now correctly show the beige banner (previously got no banner at all — bug).

Memory rule `feedback_internal_marking_style.md` rewritten with the four-state table, classifier logic, and Apr 23, 2026 revision history so future sessions don't re-litigate.

### Em-dash cleanup scope

- 63 instances of em / en dashes in source labels and `source_urls` keys replaced with `|` separator across all 65 events
- 47 Firestore documents updated (only those with actual changes)
- 74 unique thumbnails preserved (em-dash fix was purely label text)
- Render-path scan on index.html: zero em dashes in user-visible HTML (code comments preserved per CLAUDE.md rule)
- Pre-existing "INTERNAL ONLY" banner logic uncovered and fixed for the pipe separator (regex was em-dash-only, would have silently failed post-cleanup)

---

## Bullet restructuring + card styling rules

Followup work on event card readability and consistency.

| Commit | Summary |
|---|---|
| [0fe73e4](https://github.com/skywaysinc/Skyways-timeline/commit/0fe73e4) | Bullet-structure 6 event cards. Discovery: renderer already supports `ev.bullets` array at line 3766 with dedicated `.event-bullets` CSS, no code change needed. Populated the field on id=7 (USMC/GTRI POs), id=9 (Navy OTA mods), id=43 (Leadership hires), id=113 (NSLP-CRADA equipment), id=115 (DLA DGPS line items), id=116 (DLA SATCOMv2 line items). |
| [56136a7](https://github.com/skywaysinc/Skyways-timeline/commit/56136a7) | Card styling fixes + new `docs/CARD_STYLING_RULES.md` for future cards. Four content fixes: id=114 title simplified `V3 Block 2L (V3.2) | Forthcoming` → `V3.2 | Forthcoming` (drop insider nomenclature); id=111 removed misleading "Program ceiling $18.25M → $100M" bullet (parent-program figure, not Skyways-centric); id=111/36/28 fixed three bullets with arrow characters (↔ and → that earlier em-dash sweep missed). |
| [5e477a3](https://github.com/skywaysinc/Skyways-timeline/commit/5e477a3) | Extend UPCOMING_KEYWORDS to include "First Article Build" and "Forthcoming" so id=45 (V3 Block 2 Jun 2026) and id=114 (V3.2 Dec 2026) render with dashed-border greyed-out upcoming treatment matching other future cards. |
| [9275a8e](https://github.com/skywaysinc/Skyways-timeline/commit/9275a8e) | id=43 Leadership: remove Jeff Weinstein VP Production (let go). Also drop "production" from the detail's list of strengthened functions to match the three remaining hires. |

### New project rule doc: `docs/CARD_STYLING_RULES.md`

Documents standing rules for every timeline card so future work doesn't re-introduce the same issues:

- **Bullets vs. prose decision tree** (3+ parallel items → bullets; narrative/emotional → prose; reference examples id=7, id=43, id=103)
- **Bullet pattern consistency** (label:value preferred, plain descriptive acceptable, never mix inside one card)
- **Banned character list** for user-visible copy (em/en dashes, all arrows including ↔ bidirectional, HTML tags)
- **Skyways-centric content rule** — only what Skyways did, earned, delivered, or directly experienced; parent-program ceiling figures don't belong on Skyways cards. Project ULTRA case study included.
- **Version designation preference** — V3.2 over V3 Block 2L in user-visible copy
- **V3 capability rule** — `or`, never `and` (Tom + Charles's standing rule)
- **Card-review checklist** for before-shipping

Cross-referenced from `docs/README.md`. Memory-side rules stay pointed at `memory/reference_tom_martin_feedback.md` and `memory/feedback_internal_marking_style.md`.

### Full arrow character audit

The earlier em-dash cleanup scanned only em (U+2014) and en (U+2013) dashes plus simple → ← arrows. It missed ↔ (U+2194 bidirectional) and other arrow Unicode range variants. Full range scan (U+2190–U+2199) now clean across all 65 events' titles, details, bullets, and sources. Added to the CARD_STYLING_RULES.md never-in-copy list so the full arrow range stays out of future content.
