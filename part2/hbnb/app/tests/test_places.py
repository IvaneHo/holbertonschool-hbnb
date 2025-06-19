import unittest
import requests
import uuid

BASE_URL = "http://localhost:5000/api/v1"
PLACE_URL = f"{BASE_URL}/places/"
USER_URL = f"{BASE_URL}/users/"
AMENITY_URL = f"{BASE_URL}/amenities/"

class TestPlaceEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Crée un utilisateur
        res = requests.post(USER_URL, json={
            "email": f"user_{uuid.uuid4().hex[:6]}@test.com",
            "first_name": "Jean",
            "last_name": "Test"
        })
        assert res.status_code == 201, "User creation failed"
        cls.user = res.json()

    def setUp(self):
        # Crée une nouvelle amenity valide pour chaque test
        res = requests.post(AMENITY_URL, json={"name": f"Wifi {uuid.uuid4().hex[:4]}"})
        assert res.status_code == 201, "Amenity creation failed"
        self.amenity = res.json()

    def test_01_create_place_valid(self):
        payload = {
            "title": "Appartement moderne",
            "description": "Très bien situé",
            "price": 100.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": [self.amenity["id"]]
        }
        res = requests.post(PLACE_URL, json=payload)
        print("Test 01 response status:", res.status_code)
        print("Test 01 response body:", res.text)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], payload["title"])

    def test_02_create_place_invalid_attrs(self):
        invalids = [
            {"title": "A", "price": -1, "latitude": 0, "longitude": 0, "owner_id": self.user["id"]},
            {"title": "A", "price": 10, "latitude": 200, "longitude": 0, "owner_id": self.user["id"]},
            {"title": "A", "price": 10, "latitude": 0, "longitude": -300, "owner_id": self.user["id"]}
        ]
        for data in invalids:
            data["amenities"] = [self.amenity["id"]]
            res = requests.post(PLACE_URL, json=data)
            self.assertEqual(res.status_code, 400)

    def test_03_create_place_invalid_ids(self):
        payload = {
            "title": "Bad",
            "description": "Should fail",
            "price": 50,
            "latitude": 40.7,
            "longitude": -74,
            "owner_id": "fake-id",
            "amenities": ["fake-amenity"]
        }
        res = requests.post(PLACE_URL, json=payload)
        self.assertIn(res.status_code, [400, 404])

    
    def test_04_get_place_by_id(self):
        payload = {
        "title": "Place Get",
        "description": "Test GET",
        "price": 100,
        "latitude": 45.0,
        "longitude": 5.0,
        "owner_id": self.user["id"],
        "amenities": [self.amenity["id"]]
    }
        res = requests.post(PLACE_URL, json=payload)
        print("DEBUG test_04_create:", res.status_code, res.text)
        self.assertEqual(res.status_code, 201)
        place_id = res.json()["id"]

        res = requests.get(PLACE_URL + place_id)
        print("DEBUG test_04_get:", res.status_code, res.text)
        self.assertEqual(res.status_code, 200)
        self.assertIn("owner_id", res.json())
        self.assertIn("amenities", res.json())


    def test_05_get_place_invalid_id(self):
        res = requests.get(PLACE_URL + "invalid-id")
        self.assertEqual(res.status_code, 404)

    def test_06_get_all_places(self):
        res = requests.get(PLACE_URL)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)
        for place in res.json():
            self.assertIn("id", place)
            self.assertIn("title", place)

    def test_07_update_place_valid(self):
        res = requests.post(PLACE_URL, json={
            "title": "ToUpdate",
            "description": "desc",
            "price": 50,
            "latitude": 10,
            "longitude": 10,
            "owner_id": self.user["id"],
            "amenities": [self.amenity["id"]]
        })
        self.assertEqual(res.status_code, 201)
        pid = res.json()["id"]
        update = {
            "title": "Updated",
            "description": "desc new",
            "price": 70,
            "latitude": 12,
            "longitude": 12,
            "owner_id": self.user["id"],
            "amenities": [self.amenity["id"]]
        }
        res = requests.put(PLACE_URL + pid, json=update)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["title"], "Updated")

    def test_08_update_place_invalid_data(self):
        res = requests.post(PLACE_URL, json={
            "title": "InvalidUpdate",
            "description": "test",
            "price": 10,
            "latitude": 1,
            "longitude": 1,
            "owner_id": self.user["id"],
            "amenities": [self.amenity["id"]]
        })
        self.assertEqual(res.status_code, 201)
        pid = res.json()["id"]

        bad = {
            "title": "oops",
            "description": "bad",
            "price": -99,
            "latitude": 1,
            "longitude": 1,
            "owner_id": self.user["id"],
            "amenities": [self.amenity["id"]]
        }
        res = requests.put(PLACE_URL + pid, json=bad)
        self.assertEqual(res.status_code, 400)

    def test_09_update_place_invalid_id(self):
        res = requests.put(PLACE_URL + "invalid", json={
            "title": "fail",
            "description": "fail",
            "price": 50,
            "latitude": 5,
            "longitude": 5,
            "owner_id": self.user["id"],
            "amenities": [self.amenity["id"]]
        })
        self.assertEqual(res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
















