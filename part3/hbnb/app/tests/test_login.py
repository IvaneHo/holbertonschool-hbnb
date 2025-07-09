import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"

# Identifiants admin à ADAPTER selon ceux dans ta base :
ADMIN_LOGIN = {
    "email": "admin@ivane.com",
    "password": "12345678"  # DOIT être celui utilisé lors de la création en base
}

NEW_USER = {
    "first_name": "Test",
    "last_name": "User",
    "email": "test_user@ivanee.com",
    "password": "supertest423"
}

def admin_token():
    r = requests.post(f"{BASE_URL}/auth/login", json=ADMIN_LOGIN)
    print("ADMIN LOGIN STATUS:", r.status_code)
    print("ADMIN LOGIN RESPONSE:", r.json())
    assert r.status_code == 200, f"Admin login failed: {r.status_code}, {r.text}"
    return r.json()["access_token"]

def register(token):
    url = f"{BASE_URL}/users/"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(url, json=NEW_USER, headers=headers)
    print("REGISTER STATUS:", resp.status_code)
    print("REGISTER RESPONSE:", resp.json())

def login():
    url = f"{BASE_URL}/auth/login"
    resp = requests.post(url, json={"email": NEW_USER["email"], "password": NEW_USER["password"]})
    print("LOGIN STATUS:", resp.status_code)
    print("LOGIN RESPONSE:", resp.json())

if __name__ == "__main__":
    print("----- Login admin & register user -----")
    token = admin_token()
    register(token)
    print("\n----- Login user -----")
    login()
