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

tables = ['tblqPi1dUtTjK1bhk', 'tblb3eu5LS3aD9zVi', 'tblrijmejajlssqh5', 'tblD3LBp0p2m562Oc']
total_flights = 0
total_hours = 0
total_dist = 0

for tid in tables:
    offset = None
    while True:
        url = f"https://api.airtable.com/v0/{base_id}/{tid}?fields%5B%5D=Flight%20time%20(h)&fields%5B%5D=Dist%20Cruise%20(km)"
        if offset: url += f"&offset={offset}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {pat}"})
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                records = data.get("records", [])
                total_flights += len(records)
                for r in records:
                    total_hours += r.get("fields", {}).get("Flight time (h)", 0)
                    total_dist += r.get("fields", {}).get("Dist Cruise (km)", 0)
                offset = data.get("offset")
                if not offset: break
        except Exception as e:
            print(f"Error on {tid}: {e}")
            break

print(f"Total Flights: {total_flights}")
print(f"Total Hours: {total_hours}")
print(f"Total Uptime Mins: {total_hours * 60}")
print(f"Total Dist: {total_dist}")
