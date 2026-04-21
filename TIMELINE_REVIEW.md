# Timeline Cleanup Review

**Date**: April 21, 2026
**Scope**: 60 entries on skyways-timeline.vercel.app
**Status**: DRAFT — awaiting Shae approval per item before any commits

Each finding includes **WHY** I'm recommending the change. Mark approve/reject/modify per item, then I'll batch-apply.

---

## TIER 1: CRITICAL BUGS (must fix; not stylistic)

### 1.1 Duplicate ID 104 used 3 times
**Why this matters**: `id="event-N"` is the HTML anchor that the contracts table click-to-scroll uses. With 3 cards sharing id="event-104", clicks would always land on the first one (V2.0 Built 2017-06), not the intended target.

| Current ID | Date | Title | Recommended new ID |
|---|---|---|---|
| 104 | 2017-06 | V2.0 Built & Flown \| First Carbon Fiber Composite Airframe | **stays as 104** (oldest entry keeps it) |
| 104 | 2021-10 | Orbital UAV Partnership \| Heavy Fuel Engine MoU | **107** |
| 104 | 2026-04 | Series B Fundraising Begins | **108** |

**Action**: Renumber the two newer entries. Doesn't affect any current scrollToContract() targets (none of the duplicates are referenced in the breakdown table).

### 1.2 ID 38 has WRONG SOURCE URL
**Why this matters**: "11 Consecutive Resupply Flights in One Day" (Sept 2025) is sourced to a DroneVideos article titled "skyways-gets-37-million-to-develop-next-gen-military-drones" — that's a STRATFI announcement, NOT documentation of the 11-flight milestone.

**Current source**: `DroneVideos.com (Jun 2025)` → `https://dronevideos.com/skyways-gets-37-million-to-develop-next-gen-military-drones/`

**Options**:
- **A**: Find correct DroneVideos URL (or other media coverage) for the 11-flight milestone
- **B**: Remove the wrong URL and add internal-only source (Charles confirmation)
- **C**: Find Skyways' own LinkedIn / newsroom post about the 11-flight day

Recommend B if no public source exists for the 11-flight milestone specifically.

### 1.3 ID 24 (SkyNav Launch) likely WRONG SOURCE
**Why**: "SkyNav Autonomous Software Platform Launches" (April 2023) is sourced to a Nov 2025 sUAS News article about RWE Arkona offshore wind. That article is about wind farm operations, not the 2023 SkyNav launch announcement.

**Current source**: `sUAS News — Arkona Milestone Story (Nov 2025)` → `https://www.suasnews.com/2025/11/milestone-story-skyways-delivers-precision-under-pressure-with-historic-long-range-offshore-cargo-drop/`

**Action**: Remove this URL. Keep `Skyways Internal — Charles Acknin` as the source (which is approved-public anyway). The card would render with inline italic Charles attribution instead of a dropdown.

### 1.4 Broken external links (404s)
**Why**: Dead links break the credibility of the timeline as a verified-source artifact.

Both on **ID 29 (JMSDF resupply)**:
- `https://article.yahoo.co.jp/detail/442b94c0a9ff357f1315efb5d75a11f18d9bfd48` — 404 (Yahoo Japan article taken down)
- `https://www.asagumo-news.com/homepage/htdocs/news/newsflash/202411/241118/24111801.html` — 404 (Asagumo article taken down)

**Action**: Remove both URLs from `source_urls`. Keep the source label strings since they document where the info came from historically.

### 1.5 Tag mismatch on ID 102
**Why**: Category is `contracts` but tag is `Defense`. Inconsistent — will render as a contracts (blue) card with a defense (orange) tag chip.

ID 102 (2020-01) "Start of Navy OTA Spiral Development | Follow-on Contracts" — change tag from `Defense` to `Contract — U.S. Navy`.

---

## TIER 2: FACTUAL ACCURACY IMPROVEMENTS

### 2.1 ID 11 dollar figure imprecise
**Why**: Detail says "approximately $2.3M" for the Navy OTA spiral total. Verified actual is $2,066,701.73 per signed P00007 mod doc. Either round honestly to "$2.07M" or stay "approximately $2.3M" if we want the higher figure.

**Recommendation**: Change "approximately $2.3M" → "$2.07M" (matches what's on `reference_skyways_contract_archive.md`).

### 2.2 ID 11 detail uses em dash
"...the Navy Other Transaction Authority (OTA) expanded through multiple spiral development follow-on awards, growing to approximately four times its original value (approximately $2.3M)" — has em dash via parenthetical structure. Wait, no em dash here. Skip — the em dash flag was triggered by something else. Let me re-check: actually no em dashes in the detail of ID 11. This was a false flag in my script. **Skip.**

### 2.3 ID 19 (DIU/USN OTA) detail uses em dash
**Why**: Em dash detected in detail. Shae preference: NO em dashes.

Detail contains: `"...95% of critical parts needs by weight. DIU partnered with the 4th Fleet..."` — actually that's a period not em dash. Let me re-check. Scanning more carefully — the em dash in ID 19 detail might be in "...in partnership with the U.S. Navy, Naval Air Warfare Center Aircraft Division (NAWCAD), and Military Sealift Command. The award contract was directly issued by Army Contracting Command, New Jersey (ACC-NJ). The Blue Water program targets delivery of payloads up to 50 pounds across distances of 250 miles for ship-based logistics — addressing approximately 95% of critical parts needs by weight." Yes there's an em dash before "addressing".

**Action**: Replace " — addressing" with ", addressing" or " (addressing".

### 2.4 ID 29 (JMSDF) detail has 2 em dashes
**Why**: Shae preference: NO em dashes.

Detail: `"The V2.6 completed the fully autonomous round trip — launch, transit, deck landing on a moving ship, and return — in approximately 40 minutes with no human intervention."` — two em dashes around the parenthetical.

**Action**: Replace ` — ` with ` (` and ` — ` with `) ` so it reads: `"the fully autonomous round trip (launch, transit, deck landing on a moving ship, and return) in approximately 40 minutes"`.

### 2.5 ID 10 detail has 1 em dash
Detail: "Payload and range represent a tradeoff — maximum payload reduces range and vice versa."

**Action**: Replace ` — ` with `: ` → "Payload and range represent a tradeoff: maximum payload reduces range and vice versa."

### 2.6 ID 104 (V2.0 Built) detail has 1 em dash
Detail: "Skyways built and flew V2.0, a small quadplane X8 with a 12ft wingspan — the company's first carbon fiber composite airframe."

**Action**: Replace ` — ` with `, ` → "...12ft wingspan, the company's first carbon fiber composite airframe."

---

## TIER 3: TITLE / COPY — SKIMMABILITY + MILESTONE EMPHASIS

For each, the WHY is the goal Shae stated: "Title should be skimmable friendly while getting to the point and emphasizing milestones where needed."

### 3.1 Long titles (>60 chars) — trim for scan-ability

| ID | Date | Current | Recommended | Why |
|---|---|---|---|---|
| 103 | 2016-06 | "Charles Acknin Begins Building Skyways with V1 in San Francisco Apartment" (75 char) | **"Skyways Begins | V1 Built in SF Apartment"** | Founder name belongs in detail; lead with company milestone |
| 105 | 2017-07 | "V2.1 & V2.2 Build Phase Begins | 18ft Wingspan, Composite Airframe" (66 char) | **"V2.1 & V2.2 | First 18ft Wingspan Composite Build"** | Drop "Build Phase Begins" (verb-end), lead with what it IS |
| 25 | 2023-06 | "Fleet Battle Problem 23-1 | First Logistics Drone in a Fleet Exercise" (69 char) | **"Fleet Battle Problem 23-1 | First Logistics Drone in US Fleet Exercise"** (slight rewrite) OR keep — borderline | Already milestone-emphasized; could trim "in a Fleet Exercise" → "in Fleet Op" |
| 30 | 2024-10 | "[NOT PUBLIC / NO EXTERNAL SOURCES] JSDF | Inter-Island Resupply with JASDF" | **"JASDF | Inter-Island Resupply (Internal)"** | The [NOT PUBLIC] flag is now handled by the red banner — redundant in title |
| 112 | 2025-05 | "Navy NAWCAD CLIN 0006 | V3 Temperature Controlled Payload Development Contract" (80 char) | **"Navy NAWCAD CLIN 0006 | V3 TCP Development"** | TCP is already an industry abbreviation in this context |

### 3.2 Verb-end titles (less skimmable)

| ID | Date | Current | Recommended | Why |
|---|---|---|---|---|
| 24 | 2023-04 | "SkyNav Autonomous Software Platform Launches" | **"SkyNav | Autonomous Software Platform Launch"** | Convert verb-end to noun phrase for scannability |
| 104 (Series B) | 2026-04 | "Series B Fundraising Begins" | **"Series B Fundraising"** OR **"Series B Round Open"** | Drop "Begins" verb; round itself is the milestone |
| 46 | 2026-07 | "V3 Production Ramp Begins" | **"V3 Production Ramp"** | Same — drop verb-end |

### 3.3 Vague title (no specific milestone)

| ID | Date | Current | Recommended | Why |
|---|---|---|---|---|
| 12 | 2020-04 | "V2 Flight Testing & Continuous Iteration" | **"V2 Flight Test Campaign | Sub-Variants V2.2-V2.6b"** | Specific variants > vague "iteration" |

### 3.4 Could be tighter (optional polish)

| ID | Date | Current | Recommended | Why |
|---|---|---|---|---|
| 5 | 2017-05 | "Moved Into Manor Office, 5,000 Square Feet" | **"Manor Office Move | 5,000 SF"** | "Move" as noun is cleaner than "Moved Into" |
| 16 | 2021-04 | "Moved Into Austin Cross Park Drive, 10,000 Square Feet" | **"Cross Park Drive Move | 10,000 SF"** | Same pattern |
| 33 | 2024-05 | "Moved into Austin Tech Ridge, 25,000 Square Feet" | **"Tech Ridge Facility | 25,000 SF"** | Same pattern |

---

## TIER 4: SOURCE / MARKING SANITY

### 4.1 Sources that should be Charles-only inline (already-correct, no change)
These already render as inline italic gray text per the renderer logic. Verifying no changes needed:
- ID 16 Cross Park office, ID 17 V3 Initial Concept, ID 21 V3 Subscale, ID 23 V3 Block 0 First Flight, ID 26 V3 Block 1 First Flight, ID 31 DIU TCP III MEF Demo, ID 45 V3 Block 2 First Article, ID 101 Early Aircraft Prototyping, ID 103, 104, 105, 106 (early aircraft milestones)

**Action**: No change needed. These are correctly Charles-only single-source.

### 4.2 Mixed-source cards (will show "EVENT CONTAINS INTERNAL ONLY INFORMATION" banner)
- ID 9 Navy OTA Aug 2019: NASC + Janes + USNI News (all external) → no banner needed actually since no internal source! Let me re-check…
- ID 19 DIU/USN OTA: has internal contract # source + 3 external → mixed banner CORRECT
- ID 28 Phase 3 IDIQ: SBIR.gov + internal contract # → mixed banner CORRECT
- ID 110, 111, 112 (BWUAS / CLINs): internal contract # only → "NOT APPROVED" banner CORRECT
- ID 113 LP-CRADA: internal only → "NOT APPROVED" banner CORRECT

**Action**: Verify ID 9 has no internal source (recent edits added "Skyways Internal — N00421-19-9-0007 mods"?). If yes → mixed banner; if no → no banner. Need to check the live state.

### 4.3 Tag string consistency
Tags vary in format. Some use em dashes (forbidden):
- "Contract — U.S. Navy" appears 6 times
- "Contract — U.S. Air Force" appears 5 times
- "Defense — U.S. Navy", "Defense — DoD", "Defense — JSDF (Japan)" etc.

**Why**: Tags use em dashes which violate Shae's no-em-dash rule. Also tag values affect the small chip text rendered on each card.

**Action**: Replace ` — ` in all `tag` strings with ` - ` (hyphen) or ` | ` (pipe).

Affected tags (count):
- "Contract — U.S. Navy" (6) → "Contract | U.S. Navy" or "Contract: U.S. Navy"
- "Contract — U.S. Air Force" (5) → same pattern
- "Defense — U.S. Navy" / "Defense — DoD" / "Defense — JSDF (Japan)" / "Defense — USMC / III MEF" → same pattern
- "Contract — DIU / U.S. Navy" → "Contract | DIU / U.S. Navy"
- "Contract — RWE (Germany)" → "Contract | RWE (Germany)"

---

## TIER 5: AIRTABLE OPPORTUNITIES

Current live_stats from Airtable (refreshes via cron every 15 min):
- **Lifetime Flights**: 1,565
- **Flight Time**: 503.3 hours (~21 days continuous airtime)
- **Km Flown**: 42,967.5 km (~circumnavigation since 2024 per Charles)

Currently surfaced on the timeline in the `Fleet Flight Telemetry` panel. Three potential opportunities to surface MORE Airtable data:

### 5.1 Defense vs commercial flight breakdown
**Why useful**: Shae has been asked by Greenhouse Partners (PR firm) to isolate "defense missions" from total flights. The Airtable script currently aggregates all 4 tables (Flights / Merged / ANA / Skyports). If the Airtable has a `customer` or `mission type` field, we could compute "defense flights = X / total = Y" and surface both.

**Action needed**: Investigate Airtable schema (read-only — I'd need to fetch a sample record from the Merged or Flights table to see what fields exist).

### 5.2 Continents / countries flown
**Why useful**: The "3 Continents" stat on the banner is currently hardcoded text. If the Airtable has location metadata per flight, we could compute live "X continents | Y countries" and update the banner stat to be data-driven.

### 5.3 Customer breakdown (SKYWAYS / ANA / SKYPORTS)
**Why useful**: The Merged flights table tracks "End User" per flight. Could surface "1,565 total flights — SKYWAYS X / ANA Y / SKYPORTS Z" giving credibility to the partnership story.

**For all 3 above**: I should first read a sample Airtable record to see what fields exist before recommending implementation. Want me to do that read?

---

## TIER 6: ENTRIES NEEDING DEEPER FACT-CHECK

These I haven't fully verified detail-by-detail yet. Each detail block claims specific facts (dates, ranges, payloads, ship names) that should be cross-checked against sources. Highest-priority for accuracy:

| ID | Why deeper check needed |
|---|---|
| 13 | "After evaluating 65 candidate UAS in 2019, the Navy selected Skyways for its ability to carry 24 pounds up to 65 miles, covering roughly 80% of critical spare parts needs" — verify the 24/65/80% figures against sources |
| 22 | "200+ NM Cargo Delivery" — verify exact NM and ship names |
| 25 | Fleet Battle Problem 23-1 — verify "USNS Patuxent to Marines at Camp Lejeune" |
| 27 | RIMPAC 2024 — verify "Three Skyways aircraft" (Charles correction note says was previously 6, corrected to 3) |
| 31 | DIU TCP III MEF Demo — verify "6 hours / 300+ miles / 10 bags of blood / 3-6°C" |
| 36 | Project ULTRA — verify "20 operational flights / 230 lbs / first BVLOS without chase plane on military installation" |
| 42 | First Public Demo Day Nov 2025 — verify date / what was demo'd / press attendance |

I haven't done deep cross-checks against source articles for these. Want me to verify each before changes?

---

## OPEN QUESTIONS FOR YOU

1. **Tier 1 (critical bugs)**: approve all 5 fixes? Or pick which?
2. **Tier 2 (factual)**: approve all 6 fixes? Most are em-dash removals.
3. **Tier 3 (titles)**: which of the title improvements do you want? Most controversial: trimming "Charles Acknin Begins Building Skyways with V1 in San Francisco Apartment" — strong personal-story title vs cleaner skim-able title.
4. **Tier 4 (tags)**: replace em dashes in all tag strings? (small text but visible on every card)
5. **Tier 5 (Airtable)**: should I read a sample Airtable record to confirm what fields exist before recommending live-data stats?
6. **Tier 6 (deep fact-check)**: want me to verify the listed entries against their sources before making any copy changes?

I'll ping you in chat with this same summary so you can answer per tier.
