import unittest
import requests
import uuid

BASE_URL = "http://localhost:5000/api/v1/users"

class TestUserEndpoints(unittest.TestCase):
    def test_01_create_valid_user(self):
        email = f"testuser+{uuid.uuid4().hex}@example.com"
        valid_user = {
            "first_name": "Test",
            "last_name": "User",
            "email": email
        }
        res = requests.post(BASE_URL + "/", json=valid_user)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIn("id", data)
        self.user_id = data["id"]

    def test_02_duplicate_email(self):
        email = f"testuser+{uuid.uuid4().hex}@example.com"
        user = {
            "first_name": "Test",
            "last_name": "User",
            "email": email
        }
        requests.post(BASE_URL + "/", json=user)
        res = requests.post(BASE_URL + "/", json=user)
        self.assertEqual(res.status_code, 400)
        self.assertIn("email", res.text.lower())

    def test_03_invalid_user_creation(self):
        invalid_user = {
            "first_name": "",
            "last_name": "X",
            "email": "invalidemail"
        }
        res = requests.post(BASE_URL + "/", json=invalid_user)
        self.assertEqual(res.status_code, 400)
        self.assertIn("email", res.text.lower())

    def test_04_get_user_by_valid_id(self):
        email = f"testuser+{uuid.uuid4().hex}@example.com"
        user = {
            "first_name": "Test",
            "last_name": "User",
            "email": email
        }
        res = requests.post(BASE_URL + "/", json=user)
        user_id = res.json()["id"]
        res = requests.get(f"{BASE_URL}/{user_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["email"], email)

    def test_05_get_user_by_invalid_id(self):
        res = requests.get(f"{BASE_URL}/invalid-id")
        self.assertEqual(res.status_code, 404)
        self.assertIn("not found", res.text.lower())

    def test_06_get_all_users(self):
        res = requests.get(BASE_URL + "/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_07_update_valid_user(self):
        email = f"testuser+{uuid.uuid4().hex}@example.com"
        user = {
            "first_name": "Test",
            "last_name": "User",
            "email": email
        }
        res = requests.post(BASE_URL + "/", json=user)
        user_id = res.json()["id"]
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": f"updated+{uuid.uuid4().hex}@example.com"
        }
        res = requests.put(f"{BASE_URL}/{user_id}", json=update_data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["first_name"], "Updated")

    def test_08_update_invalid_data(self):
        email = f"testuser+{uuid.uuid4().hex}@example.com"
        user = {
            "first_name": "Test",
            "last_name": "User",
            "email": email
        }
        res = requests.post(BASE_URL + "/", json=user)
        user_id = res.json()["id"]
        update_data = {"email": "invalid"}
        res = requests.put(f"{BASE_URL}/{user_id}", json=update_data)
        self.assertEqual(res.status_code, 400)
        self.assertIn("email", res.text.lower())

    def test_09_update_invalid_id(self):
        update_data = {"email": f"valid+{uuid.uuid4().hex}@example.com"}
        res = requests.put(BASE_URL + "/nonexistent", json=update_data)
        self.assertEqual(res.status_code, 404)
        self.assertIn("not found", res.text.lower())



if __name__ == "__main__":
    unittest.main()
