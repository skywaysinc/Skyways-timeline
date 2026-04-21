#!/usr/bin/env python3
"""
Atomic timeline cleanup: Tier 1 critical bugs + Tier 2 factual + Tier 3 titles + Tier 4 tag em dashes.

Per the approved plan at ~/.claude/plans/do-one-last-full-misty-teacup.md.
Loads timeline_events_master.json, applies all edits, validates, writes back.
"""
import json
import sys
from pathlib import Path
from copy import deepcopy

JSON_PATH = Path(__file__).parent.parent / "Data" / "timeline_events_master.json"

# ============================================================================
# Tier 1.1 — Renumber duplicate ID 104 (3 entries collide)
# ============================================================================
RENUMBER_BY_TITLE = {
    "V2.0 Built & Flown | First Carbon Fiber Composite Airframe": 107,
    "Orbital UAV Partnership | Heavy Fuel Engine MoU": 108,
    "Series B Fundraising Begins": 109,
}

# ============================================================================
# Tier 3 — Title rewrites (current → new)
# ============================================================================
TITLE_REWRITES = {
    "Charles Acknin Begins Building Skyways with V1 in San Francisco Apartment":
        "The First Aircraft | V1 Built in San Francisco",
    "V2.1 & V2.2 Build Phase Begins | 18ft Wingspan, Composite Airframe":
        "V2.1 & V2.2 | First 18ft Composite Airframes",
    "Fleet Battle Problem 23-1 | First Logistics Drone in a Fleet Exercise":
        "Fleet Battle Problem 23-1 | First Logistics Drone in a Navy Fleet Exercise",
    "[NOT PUBLIC / NO EXTERNAL SOURCES] JSDF | Inter-Island Resupply with JASDF":
        "JASDF Inter-Island Resupply",
    "Navy NAWCAD CLIN 0006 | V3 Temperature Controlled Payload Development Contract":
        "Navy CLIN 0006 | V3 Temperature-Controlled Payload Development",
    "SkyNav Autonomous Software Platform Launches":
        "SkyNav Launch | Autonomous Multi-Aircraft Coordination",
    "Series B Fundraising Begins":
        "Series B Round Opens",
    "V3 Production Ramp Begins":
        "V3 Production Ramp",
    "V2 Flight Testing & Continuous Iteration":
        "V2 Flight Test Campaign | V2.2 → V2.6b Sub-Variants",
    "Moved Into Manor Office, 5,000 Square Feet":
        "Manor Office | 5,000 SF Expansion",
    "Moved Into Austin Cross Park Drive, 10,000 Square Feet":
        "Cross Park Drive | 10,000 SF Austin Facility",
    "Moved into Austin Tech Ridge, 25,000 Square Feet":
        "Tech Ridge | 25,000 SF North Austin HQ",
}

# ============================================================================
# Tier 2 — Detail field edits (em dashes + dollar precision)
# ============================================================================
def fix_detail(entry, expected_id):
    """Apply Tier 2 detail edits keyed by id."""
    eid = entry.get("id")
    if eid != expected_id:
        return False
    detail = entry.get("detail", "")
    new_detail = detail
    if eid == 11:
        new_detail = new_detail.replace(
            "approximately four times its original value (approximately $2.3M)",
            "approximately four times its original value ($2.07M)"
        )
    elif eid == 19:
        new_detail = new_detail.replace(" — addressing", ", addressing")
    elif eid == 29:
        new_detail = new_detail.replace(
            " — launch, transit, deck landing on a moving ship, and return — ",
            " (launch, transit, deck landing on a moving ship, and return) "
        )
    elif eid == 10:
        new_detail = new_detail.replace(" — maximum", ": maximum")
    elif eid == 107:  # V2.0 entry, renumbered from 104
        new_detail = new_detail.replace(
            " — the company's first carbon fiber composite airframe",
            ", the company's first carbon fiber composite airframe"
        )
    if new_detail != detail:
        entry["detail"] = new_detail
        return True
    return False


# ============================================================================
# Tier 4 — Tag em dash → pipe replacement
# ============================================================================
def fix_tag(entry):
    """Replace ' — ' with ' | ' in tag string."""
    tag = entry.get("tag", "")
    if " — " in tag:
        entry["tag"] = tag.replace(" — ", " | ")
        return True
    return False


# ============================================================================
# Tier 1.5 — ID 102 tag fix
# ============================================================================
def fix_id_102_tag(entry):
    """Change ID 102 tag from 'Defense' to 'Contract | U.S. Navy'."""
    if entry.get("id") == 102 and entry.get("tag") == "Defense":
        entry["tag"] = "Contract | U.S. Navy"
        return True
    return False


# ============================================================================
# Tier 1.2 — ID 38 source fix
# ============================================================================
def fix_id_38(entry):
    """Replace DroneVideos URL with Charles-internal source + V2 ship thumbnail."""
    if entry.get("id") != 38:
        return False
    new_label = "Skyways Internal — Charles Acknin (V2 operational record: 11 flights / 9.4 hrs / 466 NM / 8-min turnarounds, Sept 2025)"
    entry["sources"] = [new_label]
    entry["source_urls"] = {}
    entry["source_thumbnails"] = {
        "Skyways (V2 aboard ship)": "https://www.skyways.com/_astro/v2-aboard-ship.Dm1shnLv_ZVithb.webp"
    }
    entry["thumbnail_status"] = "fallback_v2_ship"
    return True


# ============================================================================
# Tier 1.3 — ID 24 strip wrong sUAS source entirely
# ============================================================================
def fix_id_24(entry):
    """Strip sUAS Arkona source entirely; keep Charles + Round III correction."""
    if entry.get("id") != 24:
        return False
    suas_label = "sUAS News — Arkona Milestone Story (Nov 2025)"
    if "sources" in entry:
        entry["sources"] = [s for s in entry["sources"] if s != suas_label]
    if "source_urls" in entry:
        entry["source_urls"] = {k: v for k, v in entry["source_urls"].items() if k != suas_label}
    if "source_thumbnails" in entry:
        entry["source_thumbnails"] = {k: v for k, v in entry["source_thumbnails"].items() if k != suas_label}
    return True


# ============================================================================
# Tier 1.4 — ID 29 remove 2 dead Japanese URLs (keep labels)
# ============================================================================
def fix_id_29(entry):
    """Remove 2 dead Japanese URLs from source_urls; keep label strings."""
    if entry.get("id") != 29:
        return False
    dead_keys = [
        "Yahoo! Japan News (drone.jp syndication)",
        "Asagumo Shimbun (Japan defense newspaper)",
    ]
    if "source_urls" in entry:
        entry["source_urls"] = {k: v for k, v in entry["source_urls"].items() if k not in dead_keys}
    return True


# ============================================================================
# MAIN
# ============================================================================
def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    original = deepcopy(data)
    change_log = []

    # First: Tier 1.1 renumber duplicate 104s (must happen before Tier 2/3 lookups by id)
    for entry in data:
        if entry.get("id") == 104:
            title = entry.get("title", "")
            new_id = RENUMBER_BY_TITLE.get(title)
            if new_id is not None:
                entry["id"] = new_id
                change_log.append(f"Renumbered '{title}' from id=104 → id={new_id}")

    # Tier 3: Title rewrites
    for entry in data:
        old_title = entry.get("title", "")
        if old_title in TITLE_REWRITES:
            new_title = TITLE_REWRITES[old_title]
            entry["title"] = new_title
            change_log.append(f"id={entry.get('id')}: title '{old_title}' → '{new_title}'")

    # Tier 2: Detail field edits (each function checks the id internally)
    for entry in data:
        for expected_id in (10, 11, 19, 29, 107):
            if fix_detail(entry, expected_id):
                change_log.append(f"id={entry.get('id')}: Tier 2 detail em-dash/dollar fix applied")
                break

    # Tier 1.5: ID 102 tag
    for entry in data:
        if fix_id_102_tag(entry):
            change_log.append(f"id={entry.get('id')}: tag 'Defense' → 'Contract | U.S. Navy'")

    # Tier 1.2: ID 38 source
    for entry in data:
        if fix_id_38(entry):
            change_log.append(f"id=38: source/thumbnail replaced (DroneVideos → Charles-internal + V2 ship thumb)")

    # Tier 1.3: ID 24 strip sUAS
    for entry in data:
        if fix_id_24(entry):
            change_log.append(f"id=24: sUAS Arkona source stripped (sources, urls, thumbnails)")

    # Tier 1.4: ID 29 remove dead URLs
    for entry in data:
        if fix_id_29(entry):
            change_log.append(f"id=29: removed 2 dead Japanese URLs (Yahoo Japan + Asagumo) from source_urls; kept labels")

    # Tier 4: Tag em dash → pipe (apply LAST so earlier edits to tag are preserved)
    for entry in data:
        if fix_tag(entry):
            change_log.append(f"id={entry.get('id')}: tag em-dash → pipe ('{entry.get('tag')}')")

    # ============================================================================
    # Validation
    # ============================================================================
    ids = [e.get("id") for e in data]
    duplicates = [i for i in set(ids) if ids.count(i) > 1]
    if duplicates:
        print(f"ERROR: duplicate ids remain: {duplicates}", file=sys.stderr)
        sys.exit(1)

    # No em dashes in titles or tags
    for e in data:
        for field in ("title", "tag"):
            v = e.get(field, "")
            if " — " in v:
                print(f"ERROR: em dash still in id={e.get('id')} {field}: '{v}'", file=sys.stderr)
                sys.exit(1)

    # Entry count unchanged
    if len(data) != len(original):
        print(f"ERROR: entry count changed: {len(original)} → {len(data)}", file=sys.stderr)
        sys.exit(1)

    # ============================================================================
    # Write back
    # ============================================================================
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("\n=== CHANGE LOG ===")
    for line in change_log:
        print(f"  • {line}")
    print(f"\n{len(change_log)} edits applied.")
    print(f"Entry count: {len(data)} (unchanged).")
    print(f"All ids unique: True. No em dashes in title/tag fields.")


if __name__ == "__main__":
    main()
