import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, Base, engine
import pytest
from app.models.user import User

# Setup Test DB
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# dependency override not strictly needed if we use the same DB but safe
# app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_history_flow():
    # 1. Register/Login
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    email = f"test_{unique_id}@example.com"
    password = "password123"
    
    # Try login first, if fails, register
    login_res = client.post("/auth/login", json={"email": email, "password": password})
    if login_res.status_code != 200:
        register_res = client.post("/auth/register", json={
            "email": email, 
            "password": password, 
            "first_name": "History", 
            "last_name": "Tester"
        })
        assert register_res.status_code == 200
        login_res = client.post("/auth/login", json={"email": email, "password": password})
    
    if login_res.status_code != 200:
        print(f"Login failed: {login_res.text}")
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Generate Letter
    payload = {
        "resume_id": "dummy-res-id",
        "jd_id": "dummy-jd-id",
        "tone": "confident",
        "focus": "skills",
        "resume_text": "Experienced Python Developer.",
        "jd_text": "We need a python expert."
    }
    
    gen_res = client.post("/api/generate-cover-letter", json=payload, headers=headers)
    assert gen_res.status_code == 200
    print("\n✅ Generation Successful")
    
    # 3. Fetch History
    hist_res = client.get("/api/get-history", headers=headers)
    assert hist_res.status_code == 200
    history = hist_res.json()
    
    print(f"✅ History Fetched: Found {len(history)} items")
    if len(history) > 0:
        latest = history[0]
        print(f"   Latest Title: {latest['title']}")
        print(f"   Content Snippet: {latest['content'][:50]}...")
        assert "confident" in latest['title'].lower()

if __name__ == "__main__":
    try:
        test_history_flow()
        print("\n🎉 History Flow Verification Passed!")
    except Exception as e:
        print(f"\n❌ Verification Failed: {e}")
        # print details
        import traceback
        traceback.print_exc()
