import requests
from pprint import pprint

BASE = "http://127.0.0.1:8080/api/v1/verifier"

payload = {
    "id": 3,
    "name": "Kajal",
    "pendingVerifications": 10,
    "approvedActions": 95,
    "rejectedItems": 4
}

print("🟢 Upserting verifier with fixed ID...")
res = requests.post(f"{BASE}/upsert", json=payload)
pprint(res.json())

print("\n🔹 Fetching verifier dashboard...")
res2 = requests.get(f"{BASE}/3")
pprint(res2.json())
