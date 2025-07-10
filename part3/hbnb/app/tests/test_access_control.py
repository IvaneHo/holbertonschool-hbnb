import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"

# Identifiants d'admin
ADMIN_EMAIL = "admin@hbnb.fr"
ADMIN_PASS = "12345678"

def pretty(r):
    print(f"\n{r.request.method} {r.request.url}")
    print("Status:", r.status_code)
    try:
        print("Response:", r.json())
    except Exception:
        print("Response (raw):", r.text)

def admin_login():
    r = requests.post(f"{BASE_URL}/auth/login", json={
        "email": ADMIN_EMAIL, "password": ADMIN_PASS
    })
    pretty(r)
    assert r.status_code == 200
    return r.json()["access_token"]

def register_user(email, password="TestPassword1123444444", first_name="UserEEZZZEEE", last_name="TestEEEZZ3ZEEE", admin_token=None):
    # La création d'un user nécessite désormais un token admin
    headers = {}
    if admin_token:
        headers["Authorization"] = f"Bearer {admin_token}"
    r = requests.post(f"{BASE_URL}/users/", json={
        "email": email, "password": password,
        "first_name": first_name, "last_name": last_name,
    }, headers=headers)
    pretty(r)
    assert r.status_code in (201, 400), "User creation failed: status %s" % r.status_code
    if r.status_code == 400:
        # L'utilisateur existe déjà, on va chercher son ID par login ensuite
        return None
    return r.json()["id"]

def login(email, password):
    r = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email, "password": password
    })
    pretty(r)
    assert r.status_code == 200
    return r.json()["access_token"]

def get_user_id(email, admin_token):
    r = requests.get(f"{BASE_URL}/users/", headers={"Authorization": f"Bearer {admin_token}"})
    pretty(r)
    assert r.status_code == 200
    for user in r.json():
        if user["email"] == email:
            return user["id"]
    raise Exception(f"User with email {email} not found")

def register_and_login(email, password="TestPassword1123444444", first_name="UserEEZZZEEE", last_name="TestEEEZZ3ZEEE"):
    admin_token = admin_login()
    uid = register_user(email, password, first_name, last_name, admin_token=admin_token)
    # Si déjà existant, on récupère l'id
    if uid is None:
        uid = get_user_id(email, admin_token)
    token = login(email, password)
    return uid, token

def create_place(token, title="My place", description=""):
    r = requests.post(f"{BASE_URL}/places/", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "title": title, "description": description, "price": 50, "latitude": 10, "longitude": 10, "amenities": []
    })
    pretty(r)
    assert r.status_code == 201
    return r.json()["id"]

def create_review(token, place_id, text="Super !"):
    r = requests.post(f"{BASE_URL}/reviews/", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "text": text, "rating": 5, "place_id": place_id
    })
    pretty(r)
    return r

if __name__ == "__main__":
    # REGISTER + LOGIN 2 USERS (créés par admin)
    uid1, token1 = register_and_login("user1111@ivane.com")
    uid2, token2 = register_and_login("user2222@ivane.com")

    # 1. POST /places/ SANS TOKEN => 401
    r = requests.post(f"{BASE_URL}/places/", json={
        "title": "Should fail", "price": 1, "latitude": 1, "longitude": 1, "amenities": []
    })
    pretty(r)
    assert r.status_code == 401

    # 2. User1 crée un lieu (avec description)
    place_id = create_place(token1, "Chez User1111", description="Mon super appart à Dijon")
    
    # Teste que la description est présente et correcte sur le GET one
    r = requests.get(f"{BASE_URL}/places/{place_id}")
    pretty(r)
    assert r.status_code == 200
    assert "description" in r.json()
    assert r.json()["description"] == "Mon super appart à Dijon"

    # Teste que la description est présente dans la liste GET all (au moins pour ce lieu)
    r = requests.get(f"{BASE_URL}/places/")
    pretty(r)
    assert r.status_code == 200
    found = False
    for place in r.json():
        if place["id"] == place_id:
            assert "description" in place
            assert place["description"] == "Mon super appart à Dijon"
            found = True
    assert found, "Le lieu nouvellement créé n'a pas été trouvé dans la liste !"

    # 3. User2 essaye de modifier le lieu de user1 => 403
    r = requests.put(f"{BASE_URL}/places/{place_id}", headers={
        "Authorization": f"Bearer {token2}"
    }, json={"title": "Pirate update"})
    pretty(r)
    assert r.status_code == 403
    assert r.json().get("error") == "Unauthorized action"

    # 4. User1 modifie son lieu => 200
    r = requests.put(f"{BASE_URL}/places/{place_id}", headers={
        "Authorization": f"Bearer {token1}"
    }, json={"title": "Update ok"})
    pretty(r)
    assert r.status_code == 200
    # Vérifie que la description n’a pas été supprimée (toujours présente)
    assert "description" in r.json()
    assert r.json()["description"] == "Mon super appart à Dijon"

    # 5. User1 essaye de se reviewer lui-même => 400
    r = create_review(token1, place_id)
    assert r.status_code == 400
    assert r.json().get("error") == "You cannot review your own place"

    # 6. User2 review le lieu => 201
    review_r = create_review(token2, place_id)
    assert review_r.status_code == 201
    review_id = review_r.json()["id"]

    # 7. User2 essaye de reviewer le même lieu une 2e fois => 400
    r = create_review(token2, place_id)
    assert r.status_code == 400
    assert r.json().get("error") == "You have already reviewed this place"

    # 8. User1 essaye de modifier la review de user2 => 403
    r = requests.put(f"{BASE_URL}/reviews/{review_id}", headers={
        "Authorization": f"Bearer {token1}"
    }, json={"text": "Hack review"})
    pretty(r)
    assert r.status_code == 403

    # 9. User2 modifie sa review => 200
    r = requests.put(f"{BASE_URL}/reviews/{review_id}", headers={
        "Authorization": f"Bearer {token2}"
    }, json={"text": "Nouvelle review"})
    pretty(r)
    assert r.status_code == 200

    # 10. User1 essaye de supprimer la review de user2 => 403
    r = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers={
        "Authorization": f"Bearer {token1}"
    })
    pretty(r)
    assert r.status_code == 403

    # 11. User2 supprime sa review => 200
    r = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers={
        "Authorization": f"Bearer {token2}"
    })
    pretty(r)
    assert r.status_code == 200

    # 12. User2 essaye de modifier le compte de user1 => 403
    r = requests.put(f"{BASE_URL}/users/{uid1}", headers={
        "Authorization": f"Bearer {token2}"
    }, json={"first_name": "Hacker"})
    pretty(r)
    assert r.status_code == 403

    # 13. User1 essaye de modifier son email => 400
    r = requests.put(f"{BASE_URL}/users/{uid1}", headers={
        "Authorization": f"Bearer {token1}"
    }, json={"email": "hacker@evil.com"})
    pretty(r)
    assert r.status_code == 400
    assert r.json().get("error") == "You cannot modify email or password"

    # 14. PUBLIC ENDPOINTS accessibles sans token
    r = requests.get(f"{BASE_URL}/places/")
    pretty(r)
    assert r.status_code == 200
    r = requests.get(f"{BASE_URL}/places/{place_id}")
    pretty(r)
    assert r.status_code == 200

    print("\nALL TESTS PASSED ✅")
