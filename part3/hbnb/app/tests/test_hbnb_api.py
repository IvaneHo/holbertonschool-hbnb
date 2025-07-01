import requests

BASE_URL = "http://localhost:5000/api/v1"

def safe_json(response, label="response"):
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"❌ Failed to decode {label}")
        print("🔎 Response text:", response.text)
        return None

# === 1. Create User ===
user_data = {
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser@example.com"
}
user_res = requests.post(f"{BASE_URL}/users/", json=user_data)
user = safe_json(user_res, "user creation")
print("✅ Created user:", user)

# === 2. Create Amenity ===
amenity_data = {"name": "Jacuzzi"}
amenity_res = requests.post(f"{BASE_URL}/amenities/", json=amenity_data)
amenity = safe_json(amenity_res, "amenity creation")
print("✅ Created amenity:", amenity)

# === 3. Create Place ===
place_data = {
    "title": "Ocean View",
    "description": "A great place by the sea",
    "price": 150.0,
    "latitude": 42.5,
    "longitude": 3.1,
    "owner_id": user.get("id") if user else None,
    "amenities": [amenity.get("id")] if amenity else []
}
place_res = requests.post(f"{BASE_URL}/places/", json=place_data)
print("📨 Place creation response text:", place_res.text)
place = safe_json(place_res, "place creation")
print("✅ Created place:", place)

# === 4. Create Review ===
review_data = {
    "text": "Amazing stay!",
    "rating": 5,
    "user_id": user.get("id") if user else None,
    "place_id": place.get("id") if place else None
}
review_res = requests.post(f"{BASE_URL}/reviews/", json=review_data)
print("📨 Review creation response text:", review_res.text)
review = safe_json(review_res, "review creation")
print("✅ Created review:", review)

# === 5. Get all users ===
users_res = requests.get(f"{BASE_URL}/users/")
users = safe_json(users_res, "all users")
print("📋 All users:", users)

# === 6. Get all places ===
places_res = requests.get(f"{BASE_URL}/places/")
places = safe_json(places_res, "all places")
print("📋 All places:", places)

# === 7. Get all reviews ===
reviews_res = requests.get(f"{BASE_URL}/reviews/")
reviews = safe_json(reviews_res, "all reviews")
print("📋 All reviews:", reviews)
