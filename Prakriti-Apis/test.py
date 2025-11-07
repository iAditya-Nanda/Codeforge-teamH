import requests

API_BASE = "http://127.0.0.1:8080/api/v1/submissions"

# 1️⃣ Upload a fake file (optional)
file_path = "test.jpg"
with open(file_path, "wb") as f:
    f.write(b"\xff\xd8\xff")  # create dummy jpeg header

files = {"file": open(file_path, "rb")}
upload_res = requests.post(f"{API_BASE}/upload", files=files)
print("UPLOAD:", upload_res.status_code, upload_res.text)
image_url = upload_res.json().get("url")

# 2️⃣ Add submission
payload = {
    "user_id": 7,
    "title": "Plastic Bottle Sorted",
    "location": "Cafe Mountain Root",
    "image_url": image_url,
}
res = requests.post(f"{API_BASE}/add", json=payload)
print("\nSUBMISSION:", res.status_code, res.text)

# 3️⃣ List all
all_res = requests.get(f"{API_BASE}/all")
print("\nALL SUBMISSIONS:", all_res.status_code)
print(all_res.text)
