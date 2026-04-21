#!/usr/bin/env python3
"""
Sync the cleaned timeline_events_master.json to Firestore.

Strategy:
1. Read all 60 entries from local JSON
2. For each entry, compute the new doc_id from current title+date
3. Fetch all existing Firestore doc IDs
4. For each local entry:
   - If new doc_id matches an existing doc → PATCH (set with merge=False)
   - If new doc_id does NOT match anything → CREATE new + DELETE old (find old by id field)
5. Verify final count matches local count
"""
import json
import sys
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore

JSON_PATH = Path(__file__).parent.parent / "Data" / "timeline_events_master.json"
KEY_PATH = Path("/Users/shaewilson/Desktop/Claude/Marketing - Earned Media DB/secrets/marketing---earned-media-db-firebase-adminsdk-fbsvc-57c1abc041.json")
COLLECTION = "skyways_history_and_story"


def make_doc_id(date: str, title: str) -> str:
    return f"[{date}] {title.replace('/', '-')}"


def main():
    if not KEY_PATH.exists():
        print(f"ERROR: Firebase key not found at {KEY_PATH}", file=sys.stderr)
        sys.exit(1)

    cred = credentials.Certificate(str(KEY_PATH))
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        local_entries = json.load(f)
    print(f"Loaded {len(local_entries)} local entries")

    # Index local by id and by computed new doc_id
    local_by_id = {e["id"]: e for e in local_entries if "id" in e}
    local_doc_ids = {make_doc_id(e["date"], e["title"]): e for e in local_entries}

    # Read all existing Firestore docs (just IDs + id field, not full data)
    existing_docs = list(db.collection(COLLECTION).stream())
    existing_doc_ids = set(d.id for d in existing_docs)
    existing_by_id = {}
    for d in existing_docs:
        data = d.to_dict()
        eid = data.get("id")
        if eid is not None:
            existing_by_id[eid] = d.id  # id → current doc_id
    print(f"Found {len(existing_docs)} existing Firestore docs")

    # ============================================================================
    # Plan operations
    # ============================================================================
    creates = []   # (new_doc_id, entry)
    patches = []   # (doc_id, entry) — same doc_id, just write fields
    deletes = []   # doc_ids to delete (old IDs whose entries got renamed)

    for entry in local_entries:
        eid = entry["id"]
        new_doc_id = make_doc_id(entry["date"], entry["title"])

        if new_doc_id in existing_doc_ids:
            # Doc with this exact ID exists — PATCH
            patches.append((new_doc_id, entry))
        else:
            # Doc with this title+date doesn't exist — could be a renamed entry
            old_doc_id = existing_by_id.get(eid)
            if old_doc_id and old_doc_id in existing_doc_ids:
                # Same numeric id but different title → DELETE old + CREATE new
                deletes.append(old_doc_id)
                creates.append((new_doc_id, entry))
            else:
                # Fresh entry (no matching id in Firestore) — CREATE
                creates.append((new_doc_id, entry))

    # Don't delete a doc we're about to create at the same id
    create_ids = set(c[0] for c in creates)
    deletes = [d for d in deletes if d not in create_ids]

    print(f"\nPlan: {len(patches)} patches, {len(creates)} creates, {len(deletes)} deletes")

    # ============================================================================
    # Apply
    # ============================================================================
    print("\nApplying creates...")
    for new_id, entry in creates:
        db.collection(COLLECTION).document(new_id).set(entry, merge=False)
        print(f"  CREATE {new_id}")

    print("\nApplying patches...")
    for doc_id, entry in patches:
        db.collection(COLLECTION).document(doc_id).set(entry, merge=False)
    print(f"  Patched {len(patches)} docs")

    print("\nApplying deletes...")
    for doc_id in deletes:
        db.collection(COLLECTION).document(doc_id).delete()
        print(f"  DELETE {doc_id}")

    # ============================================================================
    # Verify
    # ============================================================================
    final_docs = list(db.collection(COLLECTION).stream())
    print(f"\nFinal Firestore count: {len(final_docs)} (local: {len(local_entries)})")
    if len(final_docs) != len(local_entries):
        print("ERROR: count mismatch", file=sys.stderr)
        sys.exit(1)

    print("Sync complete.")


if __name__ == "__main__":
    main()
