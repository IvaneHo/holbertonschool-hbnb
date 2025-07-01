#!/bin/bash

# Configuration
HOST="http://localhost:5000"
USER_ID="user-id-à-remplacer"
PLACE_ID="place-id-à-remplacer"

# Fonction pour afficher un titre
function header() {
  echo ""
  echo "=============================="
  echo "$1"
  echo "=============================="
}

# Créer un avis
header "1. POST /api/v1/reviews/"
REVIEW_ID=$(curl -s -X POST "$HOST/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Incroyable expérience",
    "rating": 5,
    "user_id": "'"$USER_ID"'",
    "place_id": "'"$PLACE_ID"'"
  }' | jq -r '.id')

echo "Review ID created: $REVIEW_ID"

# Lister tous les avis
header "2. GET /api/v1/reviews/"
curl -s "$HOST/api/v1/reviews/" | jq

# Afficher un avis spécifique
header "3. GET /api/v1/reviews/$REVIEW_ID"
curl -s "$HOST/api/v1/reviews/$REVIEW_ID" | jq

# Modifier un avis
header "4. PUT /api/v1/reviews/$REVIEW_ID"
curl -s -X PUT "$HOST/api/v1/reviews/$REVIEW_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Très bien mais un peu bruyant",
    "rating": 4
  }' | jq

# Vérifier la mise à jour
header "5. GET /api/v1/reviews/$REVIEW_ID (after update)"
curl -s "$HOST/api/v1/reviews/$REVIEW_ID" | jq

# Obtenir tous les avis d’un lieu
header "6. GET /api/v1/places/$PLACE_ID/reviews"
curl -s "$HOST/api/v1/places/$PLACE_ID/reviews" | jq

# Supprimer l’avis
header "7. DELETE /api/v1/reviews/$REVIEW_ID"
curl -s -X DELETE "$HOST/api/v1/reviews/$REVIEW_ID" | jq

# Vérifier suppression
header "8. GET /api/v1/reviews/$REVIEW_ID (after delete)"
curl -s "$HOST/api/v1/reviews/$REVIEW_ID" | jq
