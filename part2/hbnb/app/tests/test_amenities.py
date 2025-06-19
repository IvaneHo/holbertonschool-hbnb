
import unittest
import requests
import uuid

BASE_URL = "http://localhost:5000/api/v1/amenities"

class TestAmenityEndpoints(unittest.TestCase):

    def test_01_create_amenity_valid(self):
        name = f"Amenity-{uuid.uuid4().hex[:6]}"
        res = requests.post(BASE_URL + "/", json={"name": name})
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], name)
        self.amenity_id = data["id"]

    def test_02_create_amenity_invalid(self):
        res = requests.post(BASE_URL + "/", json={"name": ""})
        self.assertEqual(res.status_code, 400)
        self.assertIn("error", res.json())
        self.assertTrue("requis" in res.json()["error"].lower())


    def test_03_get_amenity_valid_id(self):
        name = f"Amenity-{uuid.uuid4().hex[:6]}"
        res = requests.post(BASE_URL + "/", json={"name": name})
        amenity_id = res.json()["id"]
        res = requests.get(f"{BASE_URL}/{amenity_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["name"], name)

    def test_04_get_amenity_invalid_id(self):
        res = requests.get(BASE_URL + "/invalid-id")
        self.assertEqual(res.status_code, 404)
        self.assertIn("not found", res.text.lower())

    def test_05_get_all_amenities(self):
        res = requests.get(BASE_URL + "/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_06_update_valid_amenity(self):
        name = f"Amenity-{uuid.uuid4().hex[:6]}"
        res = requests.post(BASE_URL + "/", json={"name": name})
        amenity_id = res.json()["id"]
        updated_name = f"Updated-{uuid.uuid4().hex[:6]}"
        res = requests.put(f"{BASE_URL}/{amenity_id}", json={"name": updated_name})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["name"], updated_name)

    def test_07_update_invalid_data(self):
        name = f"Amenity-{uuid.uuid4().hex[:6]}"
        res = requests.post(BASE_URL + "/", json={"name": name})
        amenity_id = res.json()["id"]
        res = requests.put(f"{BASE_URL}/{amenity_id}", json={"name": ""})
        self.assertEqual(res.status_code, 400)
        self.assertIn("name", res.text.lower())

    def test_08_update_invalid_id(self):
        res = requests.put(BASE_URL + "/invalid-id", json={"name": "Valid"})
        self.assertEqual(res.status_code, 404)
        self.assertIn("not found", res.text.lower())

    

if __name__ == "__main__":
    unittest.main()
