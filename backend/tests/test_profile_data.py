import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "react_retry@example.com"
PASSWORD = "password123"

def test_profile_with_data():
    print("1. Authenticating...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": EMAIL,
        "password": PASSWORD
    })
    
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        sys.exit(1)
    
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   Authenticated.")

    print("\n2. Creating Data (Resume/JD/Gen)...")
    # Upload Resume
    with open("tests/test_profile_manual.py", "rb") as f: # just using this file as dummy
        files = {"file": ("dummy.txt", f, "text/plain")}
        r = requests.post(f"{BASE_URL}/api/upload-resume", headers=headers, files=files)
        resume_id = r.json()["resume_id"]

    # Submit JD
    r = requests.post(f"{BASE_URL}/api/submit-jd", headers=headers, params={"jd_text": "Need python dev"})
    jd_id = r.json()["jd_id"]

    # Generate
    payload = {
        "resume_id": resume_id,
        "jd_id": jd_id,
        "tone": "formal",
        "focus": "skills"
    }
    r = requests.post(f"{BASE_URL}/api/generate-cover-letter", headers=headers, json=payload)
    if r.status_code == 200:
        print("   Generated successfully.")
    else:
        print(f"   Generation failed: {r.text}")
        sys.exit(1)

    print("\n3. Fetching History...")
    resp = requests.get(f"{BASE_URL}/api/get-history", headers=headers)
    
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")

if __name__ == "__main__":
    test_profile_with_data()
