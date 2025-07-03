import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"

REGISTER_PAYLOAD = {
    "first_name": "Test",
    "last_name": "User",
    "email": "test_user@ivanee.com",
    "password": "supertest423"
}

LOGIN_PAYLOAD = {
    "email": "test_user@ivanee.com",
    "password": "supertest423"
}

def register():
    url = f"{BASE_URL}/users/"
    resp = requests.post(url, json=REGISTER_PAYLOAD)
    print("REGISTER STATUS:", resp.status_code)
    print("REGISTER RESPONSE:", resp.json())

def login():
    url = f"{BASE_URL}/auth/login"
    resp = requests.post(url, json=LOGIN_PAYLOAD)
    print("LOGIN STATUS:", resp.status_code)
    print("LOGIN RESPONSE:", resp.json())

if __name__ == "__main__":
    print("----- Register user -----")
    register()
    print("\n----- Login user -----")
    login()
