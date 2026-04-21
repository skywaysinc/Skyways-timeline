#!/usr/bin/env python3
"""Phase 5: Read 1 sample record from each Airtable flight table to inspect schema."""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = REPO_ROOT / ".env.local"

TABLES = {
    "Flights":         "tblqPi1dUtTjK1bhk",
    "Merged flights":  "tblb3eu5LS3aD9zVi",
    # ANA + Skyports tables — looking up via list-tables endpoint
}


def load_env():
    env = {}
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip("'").strip('"')
    return env


def fetch_one(base_id, table_id, pat):
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}?pageSize=1"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {pat}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def list_tables(base_id, pat):
    url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {pat}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def main():
    env = load_env()
    pat = env["AIRTABLE_PAT"]
    base_id = env["AIRTABLE_BASE_ID"]

    print("=== ALL TABLES IN BASE ===")
    meta = list_tables(base_id, pat)
    for t in meta.get("tables", []):
        fields = [f["name"] for f in t.get("fields", [])]
        print(f"\n📊 {t['name']} (id={t['id']})")
        print(f"   Fields: {fields}")

    print("\n\n=== SAMPLE RECORDS ===")
    for name, tid in TABLES.items():
        print(f"\n--- {name} ---")
        try:
            data = fetch_one(base_id, tid, pat)
            recs = data.get("records", [])
            if recs:
                fields = recs[0].get("fields", {})
                print(f"Field names: {list(fields.keys())}")
                for k, v in fields.items():
                    val_str = str(v)[:80]
                    print(f"  {k}: {val_str}")
        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
