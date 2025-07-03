import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"

def pretty(r):
    print(f"\n{r.request.method} {r.request.url}")
    print("Status:", r.status_code)
    try:
        print("Response:", r.json())
    except Exception:
        print("Response (raw):", r.text)

def register_and_login(email, password="TestPassword11234444", first_name="UserEEEEE", last_name="TestEEEEEE"):
    reg = requests.post(f"{BASE_URL}/users/", json={
        "email": email, "password": password,
        "first_name": first_name, "last_name": last_name,
    })
    pretty(reg)
    assert reg.status_code == 201
    login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email, "password": password
    })
    pretty(login)
    assert login.status_code == 200
    return reg.json()["id"], login.json()["access_token"]

def create_place(token, title="My place"):
    r = requests.post(f"{BASE_URL}/places/", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "title": title, "price": 50, "latitude": 10, "longitude": 10, "amenities": []
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
    # REGISTER + LOGIN 2 USERS
    uid1, token1 = register_and_login("user1111111@ivane.com")
    uid2, token2 = register_and_login("user2222222@ivane.com")

    # 1. POST /places/ SANS TOKEN => 401
    r = requests.post(f"{BASE_URL}/places/", json={
        "title": "Should fail", "price": 1, "latitude": 1, "longitude": 1, "amenities": []
    })
    pretty(r)
    assert r.status_code == 401

    # 2. User1 crée un lieu
    place_id = create_place(token1, "Chez User1111111")

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
