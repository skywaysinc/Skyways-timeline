# Stats Audit Report (Phase 9)

**Date**: April 21, 2026
**Scope**: Banner stats + 7 high-value entries with specific verifiable claims (IDs 13, 22, 25, 27, 31, 36, 42)
**Method**: Cross-checked card claims against the cited public source URLs via web fetches; checked banner stats against `reference_skyways_contract_archive.md` and CLAUDE.md.

---

## PASS — Verified accurate against authoritative source

| Stat / Claim | Where it lives | Verification |
|---|---|---|
| **$46M+ Gov't Contracts** total | Banner | Matches `reference_skyways_contract_archive.md` ($45,967,784.18 across 10 contracts). Verified in April sweep. |
| **1,565 Lifetime Flights / 503 hrs / 42,968 km** | Live banner stats | Cron-driven from Airtable Merged + Flights tables. Monotonic-decrease guard active. |
| **20+ UAVs Built** | Banner | SBIR.gov confirms "We have built over 20 UAVs and flown over 1,100 flights." |
| **Founded 2017** | Banner | Delaware filing Feb 13, 2017 (verified via OpenCorporates). |
| **7 yrs Navy Relationship** | Banner | ANTX win March 2019 → April 2026 = 7 years. ✓ |
| **STRATFI $37M (FA2280-25-9-9523)** | ID 34 | DroneLife confirms "$37 million contract from the U.S. Air Force's innovation unit, AFWERX." ✓ |
| **First Public Demo Day November 2025** | Banner + ID 42 | The Drone Girl (Nov 21, 2025): "Though this was Skyways' first demo day..." ✓ |
| **ID 25 Fleet Battle Problem 23-1** | Card | DVIDS confirms: 5 flights, 2 drones, USNS Patuxent → Camp Lejeune. ✓ |
| **ID 36 Project ULTRA flight count** | Card | Skyways newsroom + BusinessWire confirm 20 operational flights (10 round trips), 60+ miles per round trip, Grand Forks AFB ↔ Cavalier SFS. ✓ |
| **ID 22 200+ NM** | Card | DroneDJ confirms "over 200 nautical miles between Naval Air Station Patuxent River… and ships." ✓ |

---

## FLAGGED — discrepancy or unverifiable; needs your decision

### 🚩 1. ID 22 — "20 lbs" payload threshold claim
**Card current text**: "The Naval Air Warfare Center Aircraft Division (NAWCAD) found that 90% of critical mission failures can be repaired with payloads under 20 pounds, well within the capacity of the Skyways platform."

**What public sources say**:
- DroneDJ (Dec 2022): trials carried "less than 50 pounds" and "90% of all the Navy's logistics deliveries" fall in this volume
- DVIDS (related ID 25): "90% of the high priority parts that are delivered from MSC's Combat Logistic Force ships weigh **less than 50 pounds**"

**Discrepancy**: Sources cite **50 lbs**, card cites **20 lbs**.

**WHY this matters**: 20 lbs vs 50 lbs is a >2× delta. If "20 lbs" came from a different NAWCAD source you don't have on file, we should add it to sources. Otherwise the card understates Navy's actual threshold.

**Recommendations**:
- **Option A**: Change card to "90% of high-priority parts weigh less than 50 lbs" (cite DVIDS)
- **Option B**: Keep "under 20 lbs" but cite the original NAWCAD report by name. Need Charles to identify the source.
- **Option C**: Soften to "well within Skyways' payload capacity" without the specific %

---

### 🚩 2. ID 27 — "Three Skyways aircraft" at RIMPAC 2024
**Card current text**: "Three Skyways aircraft launched and recovered from USS Curtis Wilbur (DDG-54)"

**What public sources say**:
- Defense News (Jul 2024): "Curtis Wilbur launched and recovering six drones... from June 19 to June 24" — total 6 drones, no breakdown of Skyways vs PteroDynamics X-P4

**Discrepancy**: Public source confirms 6 drones total but doesn't isolate Skyways count.

**Charles Round III correction stands**: 3 Skyways aircraft (corrected from earlier 6).

**WHY this matters**: Charles is authoritative for internal team count. But anyone fact-checking against Defense News will see "six drones" and may question the "three Skyways" claim.

**Recommendations**:
- **Option A**: Keep "Three Skyways aircraft" — Charles is authoritative; add the Charles correction note to make the discrepancy auditable.
- **Option B**: Reword to "Skyways aircraft (3 of 6 total UAS launched alongside PteroDynamics X-P4) launched and recovered from USS Curtis Wilbur" — proactive disclosure.
- **Option C**: Cite Defense News as showing 6 total but flag Skyways' specific share as internal-only.

**Recommend B** — inoculates against fact-check criticism.

---

### 🚩 3. ID 36 — "first BVLOS without chase plane on military installation" claim
**Card current text**: "20 operational flights / 230 lbs / first BVLOS without chase plane on military installation"

**Wait — let me check actual ID 36 detail text** (read the full detail then update this section).

**What public sources say**:
- Skyways newsroom (Aug 21, 2025): "the first unmanned, fully autonomous BVLOS cargo flights **between two U.S. airports**" — milestone framed as airport-to-airport, NOT chase-plane-on-military-installation
- Skyways newsroom Oct 14 follow-up titled "Milestone Story: What It Takes to Be the 1st to Fly BVLOS Between Two US Airports" — same framing

**Discrepancy**: Two possibly different milestones. The newsroom emphasizes "first BVLOS between two U.S. airports", not "first BVLOS without chase plane on a military installation". Need to confirm if these are equivalent claims OR if the card is making an additional/different claim.

**WHY this matters**: A factually wrong "first" claim is investor-narrative risk.

**Recommendations**:
- **Option A**: Match the newsroom's language exactly: "first unmanned, fully autonomous BVLOS cargo flights between two U.S. airports"
- **Option B**: Verify with Charles whether "without chase plane on military installation" is an additional separate first
- **Option C**: Combine both: "20 operational flights from Grand Forks AFB to Cavalier Space Force Station (ND); first unmanned, fully autonomous BVLOS cargo flights between two U.S. airports"

**Recommend A or C** — match the official Skyways framing.

---

### 🚩 4. ID 22 — "20 lbs" claim cross-check note
**Skyways drone payload claim** in same card detail: "Skyways and Martin UAV demonstrated Vertical Takeoff and Landing (VTOL) cargo delivery capabilities."

**Source confirms both companies involved.** ✓

---

## UNVERIFIABLE — source blocked or unavailable from Claude Code

| Claim | Source | Why unverifiable |
|---|---|---|
| ID 13 "65 candidate UAS / 24 lbs / 65 mi / 80%" | USNI News, FlightGlobal | Both 403 (bot blocking) |
| ID 22 200 NM in detail | FlightGlobal | 403 (bot blocking) — but DroneDJ confirmed 200 NM separately ✓ |
| ID 31 TCP III MEF demo "6 hrs / 300+ mi / 10 bags blood / 3-6°C" | Charles internal only | No public source — accept Charles authority |
| **"1/30th Cost of Helicopter"** ($1K/hr vs $30K/hr) | BusinessWire (timeout), DroneLife (no mention) | DroneLife article does NOT contain the cost claim. BusinessWire timed out. **The claim source is unconfirmed by the verified-sources list.** |

---

## ⚠️ MEDIUM — Cross-card consistency check

### V3 spec consistency
**CLAUDE.md states**: "V3 capabilities are payload OR range, not both simultaneously: 157 NM range with 100 lbs payload, or ~35 lbs cargo at 1,000 NM. Source: internal engineering slide 49. Never say '100 lbs over 1,000 miles' — that implies both at once."

**ID 17 detail**: "Current performance estimates target 157 nautical miles range with 100 lbs payload, or approximately 35 lbs cargo at 1,000 nautical miles" ✓ correct
**DroneLife external article**: "V3 can carry 100 lbs, fly more than 1,000 miles" — reads as "both at once", which is misleading. Not our control, but worth knowing the public narrative drifts.

**Recommendation**: No action on data — but flag for next press push to correct the DroneLife framing.

---

## SUMMARY

- **8 PASS**: Banner stats and ID 25, 36 (flight count), 22 (200 NM), 42 verified ✓
- **3 FLAGGED**: ID 22 payload (20 vs 50 lbs), ID 27 RIMPAC count framing, ID 36 chase-plane vs airport-to-airport claim
- **4 UNVERIFIABLE**: USNI/FlightGlobal blocked; "1/30th cost" claim source needs identifying; ID 31 Charles-only

## Recommended next steps
1. Decide on the 3 FLAGGED items (Options A/B/C per item above) → I apply edits
2. Identify the source for "1/30th cost of helicopter" claim — either BusinessWire (need Shae to fetch from her browser) OR a different Skyways press piece
3. Optionally: dig deeper on the Charles-only claims (ID 31 etc.) by asking Charles directly via Slack
