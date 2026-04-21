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

table_id = "tblqPi1dUtTjK1bhk"
offset = None
total_payload = 0

while True:
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}?fields%5B%5D=Payload%20(lb)"
    if offset:
        url += f"&offset={offset}"
    
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {pat}"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            records = data.get("records", [])
            for r in records:
                pl = r.get("fields", {}).get("Payload (lb)", 0)
                if isinstance(pl, (int, float)):
                    total_payload += pl
            offset = data.get("offset")
            if not offset:
                break
    except Exception as e:
        print(f"Error: {e}")
        break

print(f"Total Payload (lbs): {total_payload}")
