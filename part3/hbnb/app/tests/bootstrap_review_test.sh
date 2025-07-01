#!/bin/bash

BASE_URL="http://localhost:5000/api/v1"

echo "📌 Creating a user..."
USER_RES=$(curl -s -X POST "$BASE_URL/users/" \
    -H "Content-Type: application/json" \
    -d '{"email": "review_test@example.com", "first_name": "Test", "last_name": "User"}')

USER_ID=$(echo "$USER_RES" | grep -o '"id": *"[^"]*"' | cut -d'"' -f4)
echo "✅ User ID: $USER_ID"

echo "📌 Creating an amenity..."
AMENITY_RES=$(curl -s -X POST "$BASE_URL/amenities/" \
    -H "Content-Type: application/json" \
    -d '{"name": "WiFi"}')

AMENITY_ID=$(echo "$AMENITY_RES" | grep -o '"id": *"[^"]*"' | cut -d'"' -f4)
echo "✅ Amenity ID: $AMENITY_ID"

echo "📌 Creating a place..."
PLACE_RES=$(curl -s -X POST "$BASE_URL/places/" \
    -H "Content-Type: application/json" \
    -d '{
        "title": "Review Palace",
        "description": "For testing reviews",
        "price": 123,
        "latitude": 48.0,
        "longitude": 2.0,
        "owner_id": "'"$USER_ID"'",
        "amenities": ["'"$AMENITY_ID"'"]
    }')

PLACE_ID=$(echo "$PLACE_RES" | grep -o '"id": *"[^"]*"' | cut -d'"' -f4)
echo "✅ Place ID: $PLACE_ID"

echo "📌 Creating a review..."
REVIEW_RES=$(curl -s -X POST "$BASE_URL/reviews/" \
    -H "Content-Type: application/json" \
    -d '{
        "text": "Excellent stay!",
        "rating": 5,
        "user_id": "'"$USER_ID"'",
        "place_id": "'"$PLACE_ID"'"
    }')

echo "✅ Review creation response:"
echo "$REVIEW_RES"
REVIEW_ID=$(echo "$REVIEW_RES" | grep -o '"id": *"[^"]*"' | cut -d'"' -f4)

echo "📌 Getting review by ID..."
curl -s "$BASE_URL/reviews/$REVIEW_ID"
echo

echo "📌 Updating review..."
curl -s -X PUT "$BASE_URL/reviews/$REVIEW_ID" \
    -H "Content-Type: application/json" \
    -d '{
        "text": "Updated review text",
        "rating": 4,
        "user_id": "'"$USER_ID"'",
        "place_id": "'"$PLACE_ID"'"
    }'
echo

echo "📌 Deleting review..."
curl -s -X DELETE "$BASE_URL/reviews/$REVIEW_ID"
echo
echo "✅ Deleted."

echo "📌 Checking if review was deleted..."
curl -s "$BASE_URL/reviews/$REVIEW_ID"
echo
