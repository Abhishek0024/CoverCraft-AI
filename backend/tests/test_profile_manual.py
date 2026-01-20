import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "react_retry@example.com"
PASSWORD = "password123"

def test_profile():
    print("1. Authenticating...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": EMAIL,
        "password": PASSWORD
    })
    
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        sys.exit(1)
    
    token = resp.json()["access_token"]
    print("   Authenticated successfully.")

    print("\n2. Fetching History...")
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.get(f"{BASE_URL}/api/get-history", headers=headers)
    
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")

if __name__ == "__main__":
    test_profile()
