import uuid
import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1"
USER_URL = f"{BASE_URL}/users/"
PLACE_URL = f"{BASE_URL}/places/"
REVIEW_URL = f"{BASE_URL}/reviews/"
AMENITY_URL = f"{BASE_URL}/amenities/"

class TestReviewEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        user_res = requests.post(USER_URL, json={
            "email": f"user_{uuid.uuid4().hex[:6]}@test.com",
            "first_name": "SHAI",
            "last_name": "HULUD"
        })
        cls.user = user_res.json()

        amenity_res = requests.post(AMENITY_URL, json={"name": f"TV {uuid.uuid4().hex[:4]}"})
        cls.amenity = amenity_res.json()

        place_res = requests.post(PLACE_URL, json={
            "title": "Gotham",
            "description": "Loving place",
            "price": 100,
            "latitude": 45.0,
            "longitude": 5.0,
            "owner_id": cls.user["id"],
            "amenities": [cls.amenity["id"]]
        })
        cls.place = place_res.json()

    def test_01_create_review_valid(self):
        payload = {
            "text": "Excellent stay!",
            "rating": 5,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        }
        res = requests.post(REVIEW_URL, json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIn("id", data)
        self.assertEqual(data["rating"], 5)

    def test_02_create_review_invalid_attrs(self):
        invalids = [
            {"text": "", "rating": 3, "user_id": self.user["id"], "place_id": self.place["id"]},
            {"text": "No rating", "rating": 0, "user_id": self.user["id"], "place_id": self.place["id"]},
            {"text": "Too high", "rating": 6, "user_id": self.user["id"], "place_id": self.place["id"]}
        ]
        for payload in invalids:
            res = requests.post(REVIEW_URL, json=payload)
            self.assertEqual(res.status_code, 400)

    def test_03_create_review_invalid_ids(self):
        payload = {
            "text": "Invalid IDs",
            "rating": 4,
            "user_id": "invalid-user-id",
            "place_id": "invalid-place-id"
        }
        res = requests.post(REVIEW_URL, json=payload)
        self.assertIn(res.status_code, [400, 404])

    def test_04_get_review_by_id(self):
        res = requests.post(REVIEW_URL, json={
            "text": "Will retrieve this",
            "rating": 4,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })
        review = res.json()
        review_id = review["id"]

        res = requests.get(REVIEW_URL + review_id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["text"], "Will retrieve this")

    def test_05_get_review_invalid_id(self):
        res = requests.get(REVIEW_URL + "invalid-id")
        self.assertEqual(res.status_code, 404)

    def test_06_get_reviews_by_place(self):
        res = requests.get(f"{REVIEW_URL}by_place/{self.place['id']}")

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)
        for review in res.json():
            self.assertEqual(review["place_id"], self.place["id"])

    def test_07_update_review_valid(self):
        res = requests.post(REVIEW_URL, json={
            "text": "Before update",
            "rating": 3,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })
        review = res.json()

        res = requests.put(REVIEW_URL + review["id"], json={
            "text": "After update",
            "rating": 4,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["text"], "After update")

    def test_08_update_review_invalid_data(self):
        res = requests.post(REVIEW_URL, json={
            "text": "To invalidate",
            "rating": 3,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })
        review = res.json()

        res = requests.put(REVIEW_URL + review["id"], json={
            "text": "",
            "rating": 0,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })
        self.assertEqual(res.status_code, 400)

    def test_09_delete_review(self):
        res = requests.post(REVIEW_URL, json={
            "text": "To be deleted",
            "rating": 3,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })
        review_id = res.json()["id"]

        res = requests.delete(REVIEW_URL + review_id)
        self.assertEqual(res.status_code, 200)

        res = requests.get(REVIEW_URL + review_id)
        self.assertEqual(res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
