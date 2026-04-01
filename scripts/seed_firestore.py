#!/usr/bin/env python3
"""
Seed the Skyways Timeline Firestore collection from timeline_events_master.json.

Usage:
  1. Create a new Firebase project in the Firebase Console
  2. Download the service account key JSON and place it in this project
  3. Update SERVICE_ACCOUNT_PATH below
  4. Run: python3 scripts/seed_firestore.py

This script:
  - Reads Data/timeline_events_master.json (47 events)
  - Normalizes categories to short keys (contracts, product, milestone, defense)
  - Merges sources + source_urls into [{label, url}] objects
  - Creates documents with [YYYY-MM] Title format IDs
  - Seeds the `timeline_events` collection
"""

import json
import os
import sys

import firebase_admin
from firebase_admin import credentials, firestore

# ── CONFIG ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
JSON_PATH = os.path.join(PROJECT_ROOT, "Data", "timeline_events_master.json")

# Service account key (same Firebase project as Earned Media DB)
SERVICE_ACCOUNT_PATH = os.path.join(
    os.path.expanduser("~"), "Desktop", "Claude", "Marketing - Earned Media DB",
    "marketing---earned-media-db-firebase-adminsdk-fbsvc-57c1abc041.json"
)

COLLECTION = "skyways_history_and_story"

# ── Category normalization ──
CATEGORY_MAP = {
    "Major Milestones": "milestone",
    "Contracts & Funding": "contracts",
    "Product Development": "product",
    "Defense Milestones": "defense",
}


def normalize_category(raw):
    return CATEGORY_MAP.get(raw, raw.lower().replace(" ", "_"))


def build_sources(source_labels, source_urls):
    """Merge source label list + URL map into [{label, url}] array."""
    results = []
    urls = source_urls or {}
    for label in (source_labels or []):
        results.append({
            "label": label,
            "url": urls.get(label, None),
        })
    return results


def pick_thumbnail(source_thumbnails):
    """Pick the best thumbnail from the source_thumbnails map."""
    if not source_thumbnails:
        return None
    # Prefer non-fallback thumbnails
    for label, url in source_thumbnails.items():
        if "fallback" not in label.lower():
            return url
    # Fall back to whatever is available
    return next(iter(source_thumbnails.values()), None)


def build_doc_id(sort_date, title):
    """Create [YYYY-MM] Title format doc ID."""
    # sort_date is already YYYY-MM
    clean_title = title.replace("/", "-")  # Firestore doesn't allow /
    return f"[{sort_date}] {clean_title}"


def parse_year(raw):
    """Extract the first 4-digit year from a value like '2020' or '2020–2022'."""
    import re
    match = re.search(r'\d{4}', str(raw))
    return int(match.group()) if match else 0


def transform_event(event):
    """Transform a local JSON event into the Firestore document schema."""
    return {
        "title": event["title"],
        "date": event["sort_date"],
        "date_display": event["date"],
        "year": parse_year(event["year"]),
        "sort_date": event["sort_date"],
        "category": normalize_category(event["category"]),
        "detail": event["detail"],
        "tag": event.get("tag", ""),
        "sources": build_sources(event.get("sources", []), event.get("source_urls", {})),
        "thumbnail": pick_thumbnail(event.get("source_thumbnails", {})),
        "thumbnail_status": event.get("thumbnail_status", None),
    }


def main():
    if not os.path.exists(SERVICE_ACCOUNT_PATH):
        print(f"ERROR: Service account key not found at:\n  {SERVICE_ACCOUNT_PATH}")
        print("\nTo fix:")
        print("  1. Go to Firebase Console > Project Settings > Service Accounts")
        print("  2. Click 'Generate new private key'")
        print("  3. Save the JSON file as:")
        print(f"     {SERVICE_ACCOUNT_PATH}")
        sys.exit(1)

    if not os.path.exists(JSON_PATH):
        print(f"ERROR: Timeline data not found at:\n  {JSON_PATH}")
        sys.exit(1)

    # Initialize Firebase
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # Load events
    with open(JSON_PATH, "r") as f:
        events = json.load(f)

    print(f"Loaded {len(events)} events from {JSON_PATH}")
    print(f"Seeding collection: {COLLECTION}")
    print()

    # Seed each event
    for i, event in enumerate(events, 1):
        doc_data = transform_event(event)
        doc_id = build_doc_id(event["sort_date"], event["title"])

        db.collection(COLLECTION).document(doc_id).set(doc_data)
        print(f"  [{i:2d}/{len(events)}] {doc_id}")

    print(f"\nDone! {len(events)} documents seeded to '{COLLECTION}'.")


if __name__ == "__main__":
    main()
