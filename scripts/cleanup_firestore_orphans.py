#!/usr/bin/env python3
"""Delete Firestore docs that don't appear in the local JSON's expected doc_id set."""
import json
import sys
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore

JSON_PATH = Path(__file__).parent.parent / "Data" / "timeline_events_master.json"
KEY_PATH = Path("/Users/shaewilson/Desktop/Claude/Marketing - Earned Media DB/secrets/marketing---earned-media-db-firebase-adminsdk-fbsvc-57c1abc041.json")
COLLECTION = "skyways_history_and_story"


def make_doc_id(date, title):
    return f"[{date}] {title.replace('/', '-')}"


def main():
    cred = credentials.Certificate(str(KEY_PATH))
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        local_entries = json.load(f)
    expected_ids = {make_doc_id(e["date"], e["title"]) for e in local_entries}
    print(f"Expected {len(expected_ids)} doc IDs from local")

    existing_docs = list(db.collection(COLLECTION).stream())
    orphans = [d for d in existing_docs if d.id not in expected_ids]
    print(f"Found {len(existing_docs)} Firestore docs; {len(orphans)} orphans")

    for d in orphans:
        data = d.to_dict()
        eid = data.get("id")
        title = data.get("title", "")
        print(f"  DELETE [id={eid}] {d.id}")
        db.collection(COLLECTION).document(d.id).delete()

    final = list(db.collection(COLLECTION).stream())
    print(f"\nFinal count: {len(final)} (local: {len(local_entries)})")
    if len(final) != len(local_entries):
        print("ERROR: count mismatch", file=sys.stderr)
        sys.exit(1)
    print("Cleanup complete.")


if __name__ == "__main__":
    main()
