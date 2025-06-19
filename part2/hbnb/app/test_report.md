
ERREURS dans: test_users.py



✗ test_05_get_user_by_invalid_id
Erreur :

AssertionError: 'not found' not found in '{ "id": null, "created_at": null, ... }'

💡 Cause :

On fait une requête avec un user_id invalide, mais au lieu d’un message d’erreur ("User not found" ou code 404), l’API retourne un objet utilisateur vide avec tous les champs à null.
✓ Ce qu’il faudrait :

Notre endpoint /users/<user_id> devrait :

    retourner un code 404,

    et un message clair du type : { "error": "User not found" }

✗ test_09_update_invalid_id
Erreur :

AssertionError: 'not found' not found in '{ "id": null, "created_at": null, ... }'

💡 Cause :

Même problème : une tentative de mise à jour (PUT) avec un user_id invalide renvoie un "faux utilisateur" rempli de null.
✓ À faire :

    La façade ou le contrôleur devrait détecter que l’id est inconnu,

    et retourner une erreur 404 avec un message explicite (pas un objet vide).





 ERREURS dans: test_amenities.py




✓ 1. test_01_create_amenity_valid

✗ Erreur :

AssertionError: 500 != 201

💡 Cause :

    Le endpoint POST /amenities/ lève une erreur 500 ⇒ cela signifie une exception non gérée dans notre logique métier ou schéma.

    C’est probablement un KeyError ou une ValidationError mal capturée.

✓ Solution :

    Vérifier la méthode create_amenity dans HBnBFacade :

        Est-ce qu'on valides bien name ?

        On Retournes- bien le schéma avec .model_dump() et pas return amenity brut ?

    Vérifier qu'on a bien mis :

    return AmenityResponseSchema.from_amenity(new_amenity).model_dump(mode="json")

✓ 2. test_02_create_amenity_invalid

✗ Erreur :

AssertionError: 'name' not found in '{ "error": "le nom de l'amenity est requis ..." }'

💡 Cause :

    Message d’erreur est correct, mais le test cherche le mot name en anglais dans la réponse JSON.

    mais on retournes "le nom de l'amenity..." en français.

✓ Solution (au choix) :

    Soit on traduit l’erreur en anglais (pour matcher les tests) :

    { "error": "amenity name is required (max 50 characters)" }

    Soit on modifie le test pour chercher "amenity" ou "nom" si on veut laisser en français.

✓ 3. test_03_get_amenity_valid_id

✗ Erreur JSONDecodeError :

Expecting value: line 1 column 1 (char 0)

💡 Cause :

    La réponse reçue n’est pas du JSON : probablement une erreur 500 en retour du POST.

    Donc res.json() plante car le POST a échoué → et retourne une page d'erreur HTML au lieu de JSON.

✓ Solution :

    D’abord corriger le test_01_create_amenity_valid.

    Ensuite, s’assurer que le res.status_code est bien 201 avant d'appeler res.json().

✓ 4. test_05_get_all_amenities

✗ Erreur :

AssertionError: 500 != 200

💡 Cause :

    Le GET /amenities/ plante → probablement parce que la liste est vide ou mal sérialisée.

    Peut venir d’une boucle sur les amenities qui tente un .model_dump() sur des objets bruts.

✓ Solution :

    Dans facade.get_all_amenities(), avoir :

    return [AmenityResponseSchema.from_amenity(a).model_dump(mode="json") for a in amenities]

✓ 6. test_07_update_invalid_data

✗ Erreurs similaires à test_03 :

JSONDecodeError: Expecting value: line 1 column 1 (char 0)

💡 Cause commune :

    Le POST initial échoue (cf. test_01), donc res.json() appelle .json() sur une erreur HTML → plante.

✓ Solution :

    D’abord réparer la création avec test_01.

    Ensuite vérifier res.status_code == 201 avant d’utiliser .json() dans les tests suivants.



ERREURS dans: test_places.py



 ✗ 1 - test_01_create_place_valid

Erreur :

"error": "amenity 86ae11f4-da8f-4493-af0f-23dc58ae166c not found"

Correction : Avant de créer le Place, crée une Amenity valide via un appel POST, et récupère son id.

 Remplace le début du test par :

 Create a valid amenity first
amenity_res = requests.post(AMENITY_URL, json={"name": "wifi"})
amenity_id = amenity_res.json()["id"]

res = requests.post(PLACE_URL, json={
    "title": "Sunny Loft",
    "description": "Nice place in city center",
    "price": 120,
    "latitude": 45.75,
    "longitude": 4.85,
    "owner_id": self.user["id"],
    "amenity_ids": [amenity_id]
})
self.assertEqual(res.status_code, 201, msg=f"Expected 201 but got {res.status_code}, body: {res.text}")

✓ 2 - test_04_get_place_by_id

Erreur actuelle :

"error": "amenity 86ae11f4-da8f-4493-af0f-23dc58ae166c not found"

Correction : même logique : créer un Amenity avant de créer le Place.

  Modifie la partie qui crée le Place :

  Create amenity first
amenity_res = requests.post(AMENITY_URL, json={"name": "pool"})
amenity_id = amenity_res.json()["id"]

  Create a place with the valid amenity
res = requests.post(PLACE_URL, json={
    "title": "Villa",
    "description": "Private pool included",
    "price": 250,
    "latitude": 43.61,
    "longitude": 3.88,
    "owner_id": self.user["id"],
    "amenity_ids": [amenity_id]
})
self.assertEqual(res.status_code, 201, msg=res.text)
place_id = res.json()["id"]

✓ 3 - test_07_update_place_valid

Erreur actuelle :

"error": "amenity 86ae11f4-da8f-4493-af0f-23dc58ae166c not found"

Correction : même principe : injecter un amenity avant l’update.

 Ajoute avant le POST du Place :

amenity_res = requests.post(AMENITY_URL, json={"name": "parking"})
amenity_id = amenity_res.json()["id"]

Et inclue amenity_ids=[amenity_id] dans le POST de Place.
✓ 4 - test_08_update_place_invalid_data

Erreur actuelle :

"error": "amenity 86ae11f4-da8f-4493-af0f-23dc58ae166c not found"

Correction : même correction que précédemment.

 Ajouter :

amenity_res = requests.post(AMENITY_URL, json={"name": "air conditioning"})
amenity_id = amenity_res.json()["id"]

Et utiliser amenity_ids=[amenity_id] dans la création du Place.




ERREURS dans: test_reviews.py


✗ Erreur 1 – test_07_update_review_valid

KeyError: 'text'

🔎 Cause : La réponse de la requête PUT ne contenait pas la clé "text", probablement parce que la fonction create_review() retournait ReviewResponseSchema.from_review(new_review) (avec new_review non défini) ou parce que la mise à jour ne persistait pas correctement.
✗ Erreur 2 – test_06_get_reviews_by_place

AssertionError: 404 != 200

🔎 Cause : On essayait de faire :

GET /places/<place_id>/reviews

Mais cette route n’était pas encore définie ou mal définie dans notre @ns.route("/places/<string:place_id>/reviews").
✗ Erreur 3 – test_07_update_review_valid (ancien)

KeyError: 'text'

🔎 On appelait .json()["text"] sur une réponse res qui n'avait pas cette clé. Probablement que la réponse était une erreur (400) ou qu’elle ne renvoyait pas le bon schéma.
✗ Erreur 4 – test_07_update_review_valid (init)

TypeError: User.__init__() got an unexpected keyword argument 'password'

🔎 On passait "password" dans le JSON alors que la classe User (modèle ou schéma) ne l’acceptait pas. Résolu en supprimant "password" du POST /users.