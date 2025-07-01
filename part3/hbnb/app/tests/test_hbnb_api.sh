#!/bin/bash

BASE_URL="http://localhost:5000/api/v1"

echo "==> Creating user..."
user_response=$(curl -s -X POST "$BASE_URL/users/" -H "Content-Type: application/json" -d '{"email": "alice@example.com", "first_name": "Alice", "last_name": "Test"}')
user_id=$(echo "$user_response" | grep -o '"id": *"[^"]*"' | cut -d '"' -f4)
echo "User ID: $user_id"

echo "==> Creating amenity..."
amenity_response=$(curl -s -X POST "$BASE_URL/amenities/" -H "Content-Type: application/json" -d '{"name": "Wi-Fi"}')
amenity_id=$(echo "$amenity_response" | grep -o '"id": *"[^"]*"' | cut -d '"' -f4)
echo "Amenity ID: $amenity_id"

echo "==> Creating place..."
place_response=$(curl -s -X POST "$BASE_URL/places/" -H "Content-Type: application/json" -d '{
  "title": "Cosy Studio",
  "description": "Great for remote work",
  "price": 75,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "owner_id": "'"$user_id"'",
  "amenities": ["'"$amenity_id"'"]
}')
place_id=$(echo "$place_response" | grep -o '"id": *"[^"]*"' | cut -d '"' -f4)
echo "Place ID: $place_id"

echo "==> Creating review..."
review_response=$(curl -s -X POST "$BASE_URL/reviews/" -H "Content-Type: application/json" -d '{
  "text": "Amazing place!",
  "rating": 5,
  "user_id": "'"$user_id"'",
  "place_id": "'"$place_id"'"
}')
review_id=$(echo "$review_response" | grep -o '"id": *"[^"]*"' | cut -d '"' -f4)
echo "Review ID: $review_id"

echo "==> Get all users:"
curl -s "$BASE_URL/users/" ; echo

echo "==> Get all amenities:"
curl -s "$BASE_URL/amenities/" ; echo

echo "==> Get all places:"
curl -s "$BASE_URL/places/" ; echo

echo "==> Get all reviews:"
curl -s "$BASE_URL/reviews/" ; echo

echo "==> Deleting review..."
curl -s -X DELETE "$BASE_URL/reviews/$review_id" ; echo
