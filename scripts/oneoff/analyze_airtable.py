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

success_counts = {}
takeoff_counts = 0
models = {}
flight_nums = []

while True:
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}?fields%5B%5D=Flight%20%23&fields%5B%5D=Success%3F&fields%5B%5D=%23%20Takeoffs&fields%5B%5D=AC"
    if offset:
        url += f"&offset={offset}"
    
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {pat}"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            records = data.get("records", [])
            for r in records:
                fields = r.get("fields", {})
                num = fields.get("Flight #", 0)
                suc = str(fields.get("Success?", "MISSING"))
                to = fields.get("# Takeoffs", 0)
                ac = str(fields.get("AC", "Unknown"))
                
                if num: flight_nums.append(num)
                success_counts[suc] = success_counts.get(suc, 0) + 1
                if isinstance(to, int) and to > 0:
                    takeoff_counts += 1
                models[ac] = models.get(ac, 0) + 1
                
            offset = data.get("offset")
            if not offset:
                break
    except Exception as e:
        print(f"Error: {e}")
        break

print(f"Total Rows Pulled: {len(flight_nums)}")
print(f"Min Flight #: {min(flight_nums) if flight_nums else 0}")
print(f"Max Flight #: {max(flight_nums) if flight_nums else 0}")
print(f"Success Breakdown: {success_counts}")
print(f"Flights with >0 Takeoffs: {takeoff_counts}")
print(f"Aircraft Breakdown: {dict(list(models.items())[:5])}...")
