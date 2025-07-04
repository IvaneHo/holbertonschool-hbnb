import requests
import time
import sqlite3
from pathlib import Path

BASE_URL = "http://127.0.0.1:5000/api/v1"
SQLITE_DB = "./instance/hbnb.dev.db"
ADMIN_HASH = "$argon2id$v=19$m=65536,t=3,p=4$CiHEOEeoda5V6n0vRWjtfQ$aK6puA1eXLqLtLtpZ83f0YM7rVOvougIXMFU7KN3Dio"  # MDP: 12345678
ADMIN_UUID = "7e6873c6-e892-413a-b3dc-1b8d194ed8a0"

def pretty(r, desc=""):
    print(f"\n{desc}")
    print(f"{r.request.method} {r.request.url}")
    print("Status:", r.status_code)
    try:
        print("Response:", r.json())
    except Exception:
        print("Response (raw):", r.text)

def login(email, password):
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    pretty(r, "Login")
    assert r.status_code == 200
    return r.json()["access_token"]

def register(email, password, first_name="User", last_name="Test", admin_token=None):
    data = {
        "email": email, "password": password, "first_name": first_name, "last_name": last_name
    }
    headers = {}
    if admin_token:
        headers["Authorization"] = f"Bearer {admin_token}"
    r = requests.post(f"{BASE_URL}/users/", json=data, headers=headers)
    pretty(r, f"Register user (admin_token={bool(admin_token)})")
    return r

def is_user_created_or_exists(r):
    """True si création ok, ou email déjà existant, ou forbidden."""
    if r.status_code in (200, 201, 403):
        return True
    if r.status_code == 400:
        try:
            msg = r.json()
            # Certains frameworks mettent "email already registered" dans "message" ou "error"
            if "email already registered" in msg.get("message", "").lower():
                return True
            if "email already registered" in msg.get("error", "").lower():
                return True
        except Exception:
            pass
    return False

def assert_user_created_or_exists(r, who="user"):
    if not is_user_created_or_exists(r):
        raise Exception(f"{who} non créé (status {r.status_code}) !")

def ensure_admin_sqlite(email, password):
    print(f"Tentative de création manuelle de l'admin '{email}' dans la base locale...")
    db_path = Path(SQLITE_DB)
    if not db_path.exists():
        raise Exception(f"DB not found: {SQLITE_DB}")
    import datetime
    now = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) VALUES (?, ?, ?, ?, ?, 1, ?, ?)",
        (ADMIN_UUID, "Admin", "Root", email, ADMIN_HASH, now, now)
    )
    conn.commit()
    conn.close()
    print("✅ Admin inséré dans la DB SQLite.")

def ensure_admin_exists(admin_email, admin_pass):
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": admin_email, "password": admin_pass})
    if r.status_code == 200:
        print("Admin exists and can log in.")
        return login(admin_email, admin_pass)
    print("Admin does not exist, creating...")
    r = register(admin_email, admin_pass, "Admin", "Root", admin_token=None)
    if r.status_code in (401, 403):
        print("⚠️ Impossible via API, tentative via DB SQLite…")
        ensure_admin_sqlite(admin_email, admin_pass)
        time.sleep(1)
        return login(admin_email, admin_pass)
    elif not is_user_created_or_exists(r):
        raise Exception("Impossible de créer l'admin, vérifiez vos droits ou la DB !")
    time.sleep(0.5)
    return login(admin_email, admin_pass)

def create_amenity(name, desc, token):
    r = requests.post(f"{BASE_URL}/amenities/", json={
        "name": name, "description": desc
    }, headers={"Authorization": f"Bearer {token}"})
    pretty(r, "Create amenity")
    return r

def update_amenity(aid, new_name, token):
    r = requests.put(f"{BASE_URL}/amenities/{aid}", json={
        "name": new_name
    }, headers={"Authorization": f"Bearer {token}"})
    pretty(r, "Update amenity")
    return r

def create_place(token, title):
    r = requests.post(f"{BASE_URL}/places/", json={
        "title": title, "price": 50, "latitude": 10, "longitude": 10, "amenities": []
    }, headers={"Authorization": f"Bearer {token}"})
    pretty(r, "Create place")
    return r

def update_place(pid, token, title="Admin update"):
    r = requests.put(f"{BASE_URL}/places/{pid}", json={
        "title": title
    }, headers={"Authorization": f"Bearer {token}"})
    pretty(r, "Update place")
    return r

def create_review(token, place_id, text="Nice!"):
    r = requests.post(f"{BASE_URL}/reviews/", json={
        "text": text, "rating": 5, "place_id": place_id
    }, headers={"Authorization": f"Bearer {token}"})
    pretty(r, "Create review")
    return r

def update_review(rid, token, text="Admin update review"):
    r = requests.put(f"{BASE_URL}/reviews/{rid}", json={
        "text": text
    }, headers={"Authorization": f"Bearer {token}"})
    pretty(r, "Update review")
    return r

# --- SETUP USERS ---
admin_email = "admin@ivane.com"
user_email = "user@ivane.com"
user2_email = "user2@ivane.com"
admin_pass = "12345678"   # <= Utilise le MDP du hash argon2 !
user_pass = "UserPassword123456"

# --- Création admin si besoin ---
admin_token = ensure_admin_exists(admin_email, admin_pass)

# --- Création des users standards ---
r = register(user_email, user_pass, admin_token=admin_token)
assert_user_created_or_exists(r, "User1")
r = register(user2_email, user_pass, admin_token=admin_token)
assert_user_created_or_exists(r, "User2")

user_token = login(user_email, user_pass)
user2_token = login(user2_email, user_pass)

# --- TESTS ADMIN-ONLY USERS ENDPOINTS ---
print("\n--- TEST /users/ ---")

# 1. SANS token -> création d'un user = 401 (Unauthorized)
r = requests.post(f"{BASE_URL}/users/", json={
    "email": "forbidden@ivane.com", "password": "12345678User",
    "first_name": "noauth", "last_name": "noauth"
})
pretty(r, "User sans token tente de créer un user")
assert r.status_code == 401, "User sans token peut créer un user => devrait échouer (401 Unauthorized)"

# 1.bis User authentifié simple, non admin -> 403 (Forbidden)
r = register("forbidden2@ivane.com", "12345678User", admin_token=user_token)
assert r.status_code == 403, "User authentifié non-admin peut créer un user => devrait échouer (403 Forbidden)"

# 2. Admin peut créer un user = 201 ou 400 (déjà existant)
r = register("nouvel@ivane.com", "Azerty12345", admin_token=admin_token)
if r.status_code == 201:
    print("Admin a créé un nouvel utilisateur : OK")
elif r.status_code == 400 and "email already registered" in r.text:
    print("Utilisateur déjà existant (normal pour rerun)")
else:
    raise Exception("Admin ne peut pas créer un user (code: %s)" % r.status_code)

# 3. User ne peut pas modifier un autre user
uid_r = requests.get(f"{BASE_URL}/users/", headers={"Authorization": f"Bearer {admin_token}"})
users_list = uid_r.json()
uid = next((u['id'] for u in users_list if u["email"] == user_email), None)
r = requests.put(f"{BASE_URL}/users/{uid}", json={"first_name": "hacker"},
                 headers={"Authorization": f"Bearer {user2_token}"})
pretty(r, "User non-admin essaye de modifier un autre user")
assert r.status_code == 403, "Non-admin ne peut modifier autre user"

# 4. Admin peut modifier n'importe quel user
r = requests.put(f"{BASE_URL}/users/{uid}", json={"first_name": "AdminChanged"},
                 headers={"Authorization": f"Bearer {admin_token}"})
pretty(r, "Admin modifie user")
assert r.status_code == 200, "Admin peut modifier tout user"

# 5. Email déjà pris, admin = 400
r = requests.put(f"{BASE_URL}/users/{uid}", json={"email": admin_email},
                 headers={"Authorization": f"Bearer {admin_token}"})
pretty(r, "Admin modifie user avec email déjà pris")
assert r.status_code == 400

# --- TESTS ADMIN-ONLY AMENITIES ---
print("\n--- TEST /amenities/ ---")

# 6. User simple -> créer amenity = 403
r = create_amenity("Piscine", "Cool", user_token)
assert r.status_code == 403, "Non-admin ne doit pas pouvoir créer une amenity"

# 7. Admin peut créer une amenity
r = create_amenity("Sauna", "Super sauna", admin_token)
if r.status_code == 201:
    amenity_id = r.json()["id"]
elif r.status_code == 400 and "already exists" in r.text.lower():
    print("Amenity déjà existante, on continue...")
    # On récupère la première amenity dispo pour la suite
    l = requests.get(f"{BASE_URL}/amenities/", headers={"Authorization": f"Bearer {admin_token}"}).json()
    amenity_id = l[0]["id"]
else:
    raise Exception("Admin ne peut pas créer une amenity (code: %s)" % r.status_code)

# 8. Admin peut modifier une amenity
r = update_amenity(amenity_id, "Super Sauna Update", admin_token)
assert r.status_code == 200, "Admin doit pouvoir modifier une amenity"

# 9. User simple ne peut pas modifier une amenity
r = update_amenity(amenity_id, "Pirate Amenity", user_token)
assert r.status_code == 403, "Non-admin ne doit pas pouvoir modifier une amenity"

# --- TEST ADMIN BYPASS OWNERSHIP ---
print("\n--- TEST admin bypass ownership ---")

# 10. User1 crée un place
r = create_place(user_token, "Chez User")
assert r.status_code == 201
place_id = r.json()["id"]

# 11. Admin peut modifier ce place
r = update_place(place_id, admin_token, "Admin update place")
assert r.status_code == 200, "Admin doit pouvoir modifier tout place"

# 12. User2 crée une review sur ce place
r = create_review(user2_token, place_id, "Sympa")
assert r.status_code == 201
review_id = r.json()["id"]

# 13. Admin peut modifier cette review
r = update_review(review_id, admin_token, "Admin modifie la review")
assert r.status_code == 200, "Admin doit pouvoir modifier toute review"

print("\n=== ALL ADMIN TESTS PASSED ✅ ===")
