import unittest
import requests
import uuid

class TestReviewEndpoints(unittest.TestCase):
    BASE_URL = "http://localhost:5000/api/v1"

    @classmethod
    def setUpClass(cls):
        # Email unique pour chaque run
        email = f"reviewtest_{uuid.uuid4().hex[:8]}@example.com"
        cls.user_payload = {
            "email": email,
            "first_name": "Test",
            "last_name": "User",
            "is_admin": False
        }
        user_res = requests.post(f"{cls.BASE_URL}/users", json=cls.user_payload)
        cls.assert_status_code(user_res, 201, "User creation failed")
        cls.user = user_res.json()
        cls.user_id = cls.user["id"]

        # Crée un lieu associé à l'utilisateur
        cls.place_payload = {
            "title": "Test Place",
            "description": "Nice place",
            "latitude": 48.858844,
            "longitude": 2.294351,
            "price": 120,
            "owner_id": cls.user_id,
            "amenities": []
        }
        place_res = requests.post(f"{cls.BASE_URL}/places", json=cls.place_payload)
        cls.assert_status_code(place_res, 201, "Place creation failed")
        cls.place = place_res.json()
        cls.place_id = cls.place["id"]

    @staticmethod
    def assert_status_code(response, expected_code, msg=""):
        assert response.status_code == expected_code, f"{msg}: {response.status_code} - {response.text}"

    def test_01_create_review(self):
        payload = {
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        res = requests.post(f"{self.BASE_URL}/reviews", json=payload)
        self.assertEqual(res.status_code, 201, f"Review creation failed: {res.text}")
        data = res.json()
        self.__class__.review_id = data["id"]
        self.assertEqual(data["text"], "Great place!")
        self.assertEqual(data["rating"], 5)

    def test_02_get_all_reviews(self):
        res = requests.get(f"{self.BASE_URL}/reviews")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_03_get_reviews_by_place(self):
        res = requests.get(f"{self.BASE_URL}/reviews/by_place/{self.place_id}")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_04_get_review_by_id(self):
        res = requests.get(f"{self.BASE_URL}/reviews/{self.review_id}")
        self.assertEqual(res.status_code, 200, f"Review get by id failed: {res.json()}")
        data = res.json()
        self.assertEqual(data["id"], self.review_id)

    def test_05_get_nonexistent_review(self):
        res = requests.get(f"{self.BASE_URL}/reviews/invalid-id")
        self.assertEqual(res.status_code, 404)

    def test_06_create_review_invalid_data(self):
        payload = {
            "text": "",
            "rating": 10,
            "user_id": "invalid",
            "place_id": "invalid"
        }
        res = requests.post(f"{self.BASE_URL}/reviews", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_07_update_review_valid(self):
        payload = {
            "text": "Updated review text",
            "rating": 4
        }
        res = requests.put(f"{self.BASE_URL}/reviews/{self.review_id}", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["text"], "Updated review text")
        self.assertEqual(data["rating"], 4)

    def test_08_update_review_invalid_data(self):
        payload = {
            "rating": 999  # invalid rating
        }
        res = requests.put(f"{self.BASE_URL}/reviews/{self.review_id}", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_09_delete_review(self):
        # Suppression de la review
        res = requests.delete(f"{self.BASE_URL}/reviews/{self.review_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["message"], "review deleted successfully")
        
        # Vérification qu'elle n'existe plus (doit retourner 404)
        res_check = requests.get(f"{self.BASE_URL}/reviews/{self.review_id}")
        self.assertEqual(res_check.status_code, 404)
        self.assertIn("error", res_check.json())

    def test_10_delete_nonexistent_review(self):
        res = requests.delete(f"{self.BASE_URL}/reviews/nonexistent-id")
        self.assertEqual(res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
