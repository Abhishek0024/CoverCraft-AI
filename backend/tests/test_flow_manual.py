import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "flow_test@example.com"
PASSWORD = "password123"

def get_auth_token():
    print("1. Authenticating...")
    # Try register first
    try:
        requests.post(f"{BASE_URL}/auth/register", json={
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": "Flow",
            "last_name": "Tester"
        })
    except:
        pass # Ignore if exists

    # Login
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": EMAIL,
        "password": PASSWORD
    })
    
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return None
    
    token = resp.json()["access_token"]
    print("   Authenticated successfully.")
    return token

def test_upload_resume(token):
    print("\n2. Testing Upload Resume...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create valid dummy file
    with open("dummy_resume.txt", "w") as f:
        f.write("This is a dummy resume content.")
        
    with open("dummy_resume.txt", "rb") as f:
        files = {"file": ("dummy_resume.txt", f, "text/plain")}
        resp = requests.post(f"{BASE_URL}/api/upload-resume", headers=headers, files=files)
        
    if resp.status_code == 200:
        print("   Upload success.")
        print(f"   Response: {resp.json()}")
        return resp.json()["resume_id"]
    else:
        print(f"   Upload failed: {resp.status_code} - {resp.text}")
        return None

def test_submit_jd(token):
    print("\n3. Testing Submit JD...")
    headers = {"Authorization": f"Bearer {token}"}
    params = {"jd_text": "Looking for a python developer."}
    
    resp = requests.post(f"{BASE_URL}/api/submit-jd", headers=headers, params=params)
    
    if resp.status_code == 200:
        print("   Submit JD success.")
        print(f"   Response: {resp.json()}")
        return resp.json()["jd_id"]
    else:
        print(f"   Submit JD failed: {resp.status_code} - {resp.text}")
        return None

def test_generate(token, resume_id, jd_id):
    print("\n4. Testing Generate Cover Letter...")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "resume_id": resume_id,
        "jd_id": jd_id,
        "tone": "formal",
        "focus": "skills"
    }
    
    resp = requests.post(f"{BASE_URL}/api/generate-cover-letter", headers=headers, json=payload)
    
    if resp.status_code == 200:
        print("   Generation success.")
        print(f"   Response: {resp.json().keys()}") # Just show keys to avoid clutter
    else:
        print(f"   Generation failed: {resp.status_code} - {resp.text}")

def test_history(token):
    print("\n5. Testing Get History...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/api/get-history", headers=headers)
    if resp.status_code == 200:
        print("   Get History success.")
        print(f"   Items: {len(resp.json())}")
        if len(resp.json()) > 0:
            print(f"   First Item: {resp.json()[0]['title']}")
    else:
        print(f"   Get History failed: {resp.status_code} - {resp.text}")

def main():
    token = get_auth_token()
    if not token:
        return

    resume_id = test_upload_resume(token)
    jd_id = test_submit_jd(token)
    
    if resume_id and jd_id:
        test_generate(token, resume_id, jd_id)
        test_history(token)
    
    # Cleanup
    if os.path.exists("dummy_resume.txt"):
        os.remove("dummy_resume.txt")

if __name__ == "__main__":
    main()
