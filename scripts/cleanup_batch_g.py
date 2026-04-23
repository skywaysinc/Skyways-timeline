#!/usr/bin/env python3
"""
Batch G: Deep-search findings applied
  1. id=113 (LP-CRADA): update with full NSLP-CRADA-NAWCADPAX-25-533 details; mark public
  2. id=115 (DGPS): update title + detail with PFR006115 / $71,070
  3. id=116 (SATCOMv2): update title + detail with PFR007234 / $203,735
  4. id=117 (Intelligen): update title + detail with PFR007445 / $79,545
"""
import json
from pathlib import Path

JSON_PATH = Path(__file__).parent.parent / "Data" / "timeline_events_master.json"

UPDATES = {
    113: {
        "title": "Aircraft Lease Agreement | Navy NSLP-CRADA-NAWCADPAX-25-533 (V2 AV1-3)",
        "detail": (
            "Non-Standard Limited Purpose Cooperative Research and Development Agreement (NSLP-CRADA) "
            "between Naval Air Warfare Center Aircraft Division Patuxent River (NAVAIRWARCENACDIV) and "
            "Skyways Air Transportation, Inc. Agreement number NSLP-CRADA-NAWCADPAX-25-533, titled "
            "\"SKYWAYS V2.6 UNMANNED AERIAL SYSTEM DEMONSTRATION.\" Signed by Charles Acknin (Skyways CEO) "
            "on March 18, 2025 and by J.E. Dougherty IV, RDML, USN, Commander NAWCAD on March 20, 2025. "
            "Duration up to 4 years from effective date (through ~March 2029). The Navy transfers custody "
            "of three V2.6 aircraft (AV1, AV2, AV3) plus 6 Ground Control Stations, 3 Telemetry Station "
            "Shore units, 3 Telemetry Station Ship units, 4 VTOL Battery Packs, and 3 Ground Support "
            "Equipment kits to Skyways for demonstrations and technology development. No funds are "
            "transferred under the agreement (Article 16); Skyways retains title to its own equipment and "
            "must return all Navy-owned equipment at termination. Per Article 19, the agreement is "
            "releasable to the public."
        ),
        "sources": [
            "Skyways Internal — Contract on File (NSLP-CRADA-NAWCADPAX-25-533, signed March 18 and 20, 2025; publicly releasable per Article 19)"
        ],
    },
    115: {
        "title": "$71,070 | Navy DLA PO — DGPS (SPE8EJ21D0022 PO 0408)",
        "detail": (
            "Defense Logistics Agency (DLA) Purchase Order PFR006115, Order Number PO 0408, under prime "
            "contract SPE8EJ21D0022 (Noble Supply and Logistics is prime; Skyways is component supplier). "
            "PO dated March 15, 2023. Total funded value $71,070.00 breaks out as: Differential Global "
            "Positioning System (DGPS) hardware — 6 units at $1,897.50 = $11,385.00; Engineering services "
            "(integration, ground testing, flight testing, quality assurance) — $48,185.00; Special "
            "Operations Equipment (SOE) freight charges — $11,500.00. Delivery to James Tomasic at "
            "Naval Air Warfare Center Aircraft Division Rapid Prototyping Experimentation and Demonstration "
            "(NAWCAD RPED), Patuxent River, MD."
        ),
        "sources": [
            "Skyways Internal — Contract on File (Noble Purchase Order PFR006115 under DLA prime SPE8EJ21D0022; PO dated Mar 15, 2023; $71,070.00 total funded to Skyways)"
        ],
    },
    116: {
        "title": "$203,735 | Navy DLA PO — SATCOMv2 (SPE8EJ21D0022 PO 0463)",
        "detail": (
            "Defense Logistics Agency (DLA) Purchase Order PFR007234, Order Number PO 0463, under prime "
            "contract SPE8EJ21D0022 (Noble Supply and Logistics is prime; Skyways is component supplier). "
            "PO dated May 26, 2023. Total funded value $203,735.00 breaks out as: SKYTRAC DLS-100 "
            "SATCOMv2 hardware (3 units per aircraft across 3 aircraft = 9 total) at $28,865.00 each = "
            "$86,595.00; V2.6b SATCOMv2 Non-Recurring Engineering and Test (software, mechanical, "
            "electrical, test, flight test) = $105,110.00; SKYTRAC DLS-100 Integration across 3 aircraft "
            "at $1,610.00 each = $4,830.00; SPP-720M airtime plan (720 MB per month for 12 months) at "
            "$600.00 each = $7,200.00. Delivery to James Tomasic at NAWCAD RPED, Patuxent River, MD. "
            "Buyer: Tyler Ray (Noble)."
        ),
        "sources": [
            "Skyways Internal — Contract on File (Noble Purchase Order PFR007234 under DLA prime SPE8EJ21D0022; PO dated May 26, 2023; $203,735.00 total funded to Skyways)"
        ],
    },
    117: {
        "title": "$79,545 | Navy DLA PO — Intelligen (SPE8EJ21D0022 PO 0465)",
        "detail": (
            "Defense Logistics Agency (DLA) Purchase Order PFR007445, Order Number PO 0465, under prime "
            "contract SPE8EJ21D0022 (Noble Supply and Logistics is prime; Skyways is component supplier). "
            "PO dated June 15, 2023. Total funded value $79,545.00 breaks out as: V2.6b Intelligen "
            "onboard start across 3 aircraft at $12,255.00 each = $36,765.00; V2.6b AV1-3 Intelligen "
            "integration and testing across 3 aircraft at $14,260.00 each = $42,780.00. Delivery to "
            "James Tomasic at NAWCAD RPED, Patuxent River, MD. Buyer: Karli King (Noble)."
        ),
        "sources": [
            "Skyways Internal — Contract on File (Noble Purchase Order PFR007445 under DLA prime SPE8EJ21D0022; PO dated Jun 15, 2023; $79,545.00 total funded to Skyways)"
        ],
    },
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    log = []
    for entry in data:
        eid = entry.get("id")
        if eid in UPDATES:
            u = UPDATES[eid]
            entry["title"] = u["title"]
            entry["detail"] = u["detail"]
            entry["sources"] = u["sources"]
            # Clear any stale source_urls mapping (new source labels don't match old keys)
            entry["source_urls"] = {}
            log.append(f"id={eid}: title + detail + sources updated")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("=== CHANGE LOG ===")
    for l in log:
        print(f"  • {l}")


if __name__ == "__main__":
    main()
