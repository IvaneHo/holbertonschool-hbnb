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
        res = requests.post(USER_URL, json={
            "email": f"user_{uuid.uuid4().hex[:6]}@test.com",
            "first_name": "Jean",
            "last_name": "Test"
        })
        assert res.status_code == 201, "User creation failed"
        cls.user = res.json()

    def setUp(self):
        res = requests.post(AMENITY_URL, json={"name": f"Amenity_{uuid.uuid4().hex[:6]}"})
        assert res.status_code == 201, "Amenity creation failed"
        self.amenity = res.json()

    def test_create_place_valid(self):
        payload = {
            "title": "Appartement moderne",
            "description": "Très bien situé",
            "price": 100,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": [self.amenity["id"]]
        }
        res = requests.post(PLACE_URL, json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], payload["title"])

    def test_create_place_invalid_attrs(self):
        invalids = [
            {"title": "Ok", "price": -1, "latitude": 0, "longitude": 0, "owner_id": self.user["id"]},
            {"title": "Ok", "price": 10, "latitude": 200, "longitude": 0, "owner_id": self.user["id"]},
            {"title": "Ok", "price": 10, "latitude": 0, "longitude": -300, "owner_id": self.user["id"]}
        ]
        for data in invalids:
            data["amenities"] = [self.amenity["id"]]
            res = requests.post(PLACE_URL, json=data)
            self.assertEqual(res.status_code, 400)

    def test_create_place_invalid_ids(self):
        payload = {
            "title": "Bad",
            "description": "Fake IDs",
            "price": 50,
            "latitude": 40.7,
            "longitude": -74,
            "owner_id": "non-existent-user",
            "amenities": ["non-existent-amenity"]
        }
        res = requests.post(PLACE_URL, json=payload)
        self.assertIn(res.status_code, [400, 404])

    def test_get_place_by_id(self):
        payload = {
            "title": "Place Get",
            "description": "Testing GET",
            "price": 90,
            "latitude": 48.0,
            "longitude": 2.0,
            "owner_id": self.user["id"],
            "amenities": [self.amenity["id"]]
        }
        res = requests.post(PLACE_URL, json=payload)
        self.assertEqual(res.status_code, 201)
        place_id = res.json()["id"]

        res = requests.get(PLACE_URL + place_id)
        self.assertEqual(res.status_code, 200)
        self.assertIn("title", res.json())
        self.assertEqual(res.json()["id"], place_id)

    def test_get_place_invalid_id(self):
        res = requests.get(PLACE_URL + "invalid-id")
        self.assertEqual(res.status_code, 404)

    def test_get_all_places(self):
        res = requests.get(PLACE_URL)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_update_place_partial_valid(self):
        res = requests.post(PLACE_URL, json={
            "title": "ToUpdate",
            "description": "before",
            "price": 30,
            "latitude": 10.0,
            "longitude": 10.0,
            "owner_id": self.user["id"],
            "amenities": [self.amenity["id"]]
        })
        self.assertEqual(res.status_code, 201)
        pid = res.json()["id"]

        res = requests.put(PLACE_URL + pid, json={"title": "Updated only title"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["title"], "Updated only title")

    def test_update_place_invalid_data(self):
        res = requests.post(PLACE_URL, json={
            "title": "Bad update",
            "description": "bad update",
            "price": 25,
            "latitude": 12.0,
            "longitude": 15.0,
            "owner_id": self.user["id"],
            "amenities": [self.amenity["id"]]
        })
        self.assertEqual(res.status_code, 201)
        pid = res.json()["id"]

        res = requests.put(PLACE_URL + pid, json={"price": -100})
        self.assertEqual(res.status_code, 400)

    def test_update_place_invalid_id(self):
        res = requests.put(PLACE_URL + "doesnotexist", json={"title": "fail"})
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
