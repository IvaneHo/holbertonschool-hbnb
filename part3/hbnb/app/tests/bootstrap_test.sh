#!/bin/bash

BASE_URL="http://localhost:5000/api/v1"

echo "📌 Création d’un utilisateur..."
USER_RESPONSE=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "first_name": "Test", "last_name": "User"}')

USER_ID=$(echo "$USER_RESPONSE" | grep -oP '"id"\s*:\s*"\K[^"]+')
echo "✅ Utilisateur ID : $USER_ID"

echo "📌 Création d’un amenity..."
AMENITY_RESPONSE=$(curl -s -X POST "$BASE_URL/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Wifi"}')

AMENITY_ID=$(echo "$AMENITY_RESPONSE" | grep -oP '"id"\s*:\s*"\K[^"]+')
echo "✅ Amenity ID : $AMENITY_ID"

echo "📌 Création d’un place..."
PLACE_RESPONSE=$(curl -s -X POST "$BASE_URL/places/" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Test Place\",
    \"price\": 100,
    \"latitude\": 45.0,
    \"longitude\": 5.0,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": [\"$AMENITY_ID\"]
  }")

echo "$PLACE_RESPONSE"
