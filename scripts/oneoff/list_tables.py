import urllib.request, json
import os
from pathlib import Path

# Load AIRTABLE_PAT + AIRTABLE_BASE_ID from .env.local (gitignored) or the
# process environment. The PAT is a secret — never hardcode it in this file.
def _load_env_local():
    env = {}
    p = Path(__file__).resolve().parent / '.env.local'
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, _, v = line.partition('=')
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env

_ENV = _load_env_local()
pat = os.environ.get('AIRTABLE_PAT') or _ENV.get('AIRTABLE_PAT')
base_id = os.environ.get('AIRTABLE_BASE_ID') or _ENV.get('AIRTABLE_BASE_ID')
if not pat or not base_id:
    raise SystemExit('AIRTABLE_PAT / AIRTABLE_BASE_ID missing. Set them in .env.local.')

# The metadata endpoint for tables:
url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {pat}"})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        tables = data.get("tables", [])
        print(f"Found {len(tables)} tables in the base.")
        for t in tables:
            print(f"- Table: '{t['name']}' (ID: {t['id']})")
except Exception as e:
    print(f"Error accessing metadata endpoint (may require enterprise scope): {e}")

