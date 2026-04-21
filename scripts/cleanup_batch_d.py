#!/usr/bin/env python3
"""
Batch D: $-in-title for 9 contract entries + ID 27 RIMPAC reword + ID 36 Project ULTRA rephrase.
"""
import json
import sys
from pathlib import Path

JSON_PATH = Path(__file__).parent.parent / "Data" / "timeline_events_master.json"

TITLE_REWRITES = {
    "USMC/GTRI | First Purchase Order for Two V2.2 Aircraft":
        "$272,711 | USMC/GTRI First Purchase Order (Two V2.2 Aircraft)",
    "Navy OTA Contract Awarded | Blue Water Maritime Logistics UAS":
        "$2,066,702 | Navy OTA Award (Blue Water Maritime Logistics UAS)",
    "Start of Navy OTA Spiral Development | Follow-on Contracts":
        "$575,141 | Navy OTA Spiral Development Begins",
    "DIU/USN Blue Water Maritime Logistics UAS Contract":
        "$1,807,149 | DIU/USN OTA (Blue Water + Spiral Mods)",
    "End of Navy OTA Spiral Development | Follow-on Contracts":
        "$2,066,702 | Navy OTA Final Value (Blue Water Spiral Complete)",
    "Navy NAWCAD BWUAS 2.0 Prototype Contract Awarded":
        "$479,053 | Navy NAWCAD BWUAS 2.0 Prototype",
    "USAF SBIR Phase 3 IDIQ Contract & STRATFI Selection":
        "$2,200,000 Obligated / $4,999,999 Ceiling | USAF SBIR Phase 3 IDIQ + STRATFI Selection",
    "Navy NAWCAD CLIN 0005 | Project ULTRA Demonstration Contract":
        "$361,832 | Navy CLIN 0005 (Project ULTRA Demonstration)",
    "Navy CLIN 0006 | V3 Temperature-Controlled Payload Development":
        "$982,850 | Navy CLIN 0006 (V3 Temperature-Controlled Payload)",
}


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    change_log = []

    # Title rewrites
    for entry in data:
        old = entry.get("title", "")
        if old in TITLE_REWRITES:
            entry["title"] = TITLE_REWRITES[old]
            change_log.append(f"id={entry['id']}: title '{old}' -> '{entry['title']}'")

    # ID 27 RIMPAC: reword 'Three Skyways aircraft' to '3 of 6 total UAS launched alongside PteroDynamics'
    for entry in data:
        if entry.get("id") == 27:
            old_detail = entry.get("detail", "")
            new_detail = old_detail.replace(
                "Three Skyways aircraft launched and recovered from USS Curtis Wilbur (DDG-54) during Trident Warrior at the Rim of the Pacific Exercise (RIMPAC) 2024",
                "Skyways aircraft (3 of 6 total Unmanned Aircraft Systems launched alongside PteroDynamics X-P4) launched and recovered from USS Curtis Wilbur (DDG-54) during Trident Warrior at the Rim of the Pacific Exercise (RIMPAC) 2024"
            )
            if new_detail != old_detail:
                entry["detail"] = new_detail
                change_log.append("id=27: RIMPAC count reworded to '3 of 6 total UAS alongside PteroDynamics'")

    # ID 36 Project ULTRA: rephrase chase-plane claim to match newsroom (airport-to-airport)
    for entry in data:
        if entry.get("id") == 36:
            old_detail = entry.get("detail", "")
            # Look for any "chase plane" / "without chase plane" / "first BVLOS" wording
            new_detail = old_detail
            replacements = [
                ("first BVLOS without chase plane on military installation",
                 "first unmanned, fully autonomous Beyond Visual Line of Sight (BVLOS) cargo flights between two U.S. airports"),
                ("first BVLOS without a chase plane on a military installation",
                 "first unmanned, fully autonomous Beyond Visual Line of Sight (BVLOS) cargo flights between two U.S. airports"),
            ]
            for old_phrase, new_phrase in replacements:
                new_detail = new_detail.replace(old_phrase, new_phrase)
            if new_detail != old_detail:
                entry["detail"] = new_detail
                change_log.append("id=36: Project ULTRA chase-plane claim reworded to airport-to-airport BVLOS framing")

    # ID 22: keep "20 lbs / 90% NAWCAD" claim per Charles authority, but add Charles to sources for auditability
    for entry in data:
        if entry.get("id") == 22:
            sources = entry.get("sources", [])
            charles_label = "Skyways Internal — Charles Acknin (NAWCAD finding: 90% of critical mission failures repairable with under 20 lb payloads — public sources cite a separate 50 lb threshold for general logistics)"
            if not any("Charles Acknin" in s for s in sources):
                # Prepend Charles so it shows first
                entry["sources"] = [charles_label] + sources
                change_log.append("id=22: Added Charles attribution + audit note for the 90%/20 lbs NAWCAD claim")

    # Validation
    titles = [e.get("title", "") for e in data]
    if len(set(titles)) != len(titles):
        dupes = [t for t in set(titles) if titles.count(t) > 1]
        print(f"WARNING: duplicate titles after rewrites: {dupes}", file=sys.stderr)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("=== CHANGE LOG ===")
    for line in change_log:
        print(f"  • {line}")
    print(f"\n{len(change_log)} edits applied.")


if __name__ == "__main__":
    main()
