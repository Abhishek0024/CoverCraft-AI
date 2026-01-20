import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_register():
    print("Testing Registration...")
    payload = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.status_code == 200 or response.status_code == 400  # 400 if already exists

def test_login_minimal():
    print("\nTesting Login (Minimal - Email/Pass)...")
    payload = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

def test_login_full():
    print("\nTesting Login (Full - as per UserCreate)...")
    payload = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    if test_register():
        test_login_minimal()
        test_login_full()
