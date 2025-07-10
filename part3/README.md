# HBnB - Part 3 : Auth & DB

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-blue.svg)
![Holberton](https://img.shields.io/badge/Holberton-Project-red.svg)


##  Overview

This repository contains the backend for the **HBnB project - Part 3**.  
It’s a complete RESTful API for a booking platform (like AirBnB), using **Flask**, **SQLAlchemy**, **JWT**, **Pydantic** for validation, and secure password hashing (Argon2).

The project is designed with **clean architecture**: separate models, schemas, repository, business (service) layer, and API resources.  
You will find all CRUD endpoints, authentication/authorization, and a full SQL schema—plus scripts and test coverage.


##  Project Structure

```
part3/hbnb/
├── README.md
├── config.py
├── requirements.txt
├── run.py
├── create_tables.py
├── hbnb.sql
├── test_config.py
├── instance/
│   └── hbnb.dev.db
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── amenity.py
│   │   └── review.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── sqlalchemy_repository.py
│   │   ├── user_repository.py
│   │   ├── place_repository.py
│   │   ├── amenity_repository.py
│   │   └── review_repository.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── amenity.py
│   │   └── review.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   │   ├── amenity_service.py
│   │   └── review_service.py
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── amenities.py
│   │       ├── reviews.py
│   │       └── auth.py
│   └── tests/
│       ├── __init__.py
│       ├── init_admin.py
│       ├── test_access_control.py
│       ├── test_entities_crud.py
│       ├── test_login.py
│       ├── test_relations.py
│       ├── test_relationships.py
│       ├── test_sqlalchemy_repository.py
│       └── test_user_repository.py
├── scriptSQL/
│   └── hbnb.sql


```



# Installation Guide
To get started with the project, follow these simple steps:

**Clone the repository**

First, clone the project and navigate into the correct directory:

```
git clone https://github.com/IvaneHo/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3/hbnb
```


**Set up a virtual environment**

Create a new virtual environment (recommended to avoid dependency issues):

```
python3 -m venv venv
```

Then activate it:

```
source venv/bin/activate
```

**Install the required packages**

Once the virtual environment is active, install the dependencies with:

```
pip install -r requirements.txt
```

**Initialize the database**

Create the instance directory if it doesn’t exist
```
mkdir -p instance
```
Load the schema and initial data from hbnb.sql into the development database
```
sqlite3 instance/hbnb.dev.db < app/scriptSQL/hbnb.sql
```

This will create tables (users, places, amenities, reviews, place_amenity, etc) and insert any provided seed data.

**The instance/ Folder**

This folder is where SQLite databases are stored (e.g., hbnb.dev.db)
To reset your local database, just delete the file and re-import the schema

```
rm instance/hbnb.dev.db
sqlite3 instance/hbnb.dev.db < app/scriptSQL/hbnb.sql
```

**Run the application**

Finally, from within the hbnb directory, you can launch the app by running:

```
python run.py
```

By default, the Flask app listens on http://127.0.0.1:5000/. The API root is typically at http://127.0.0.1:5000/api/v1/



# API Usage

HBnB’s API is accessed under the /api/v1/ prefix. Important endpoints include:

    Authentication:

        POST /api/v1/auth/login – Log in with JSON credentials {"email": "...", "password": "..."}. Returns an access_token (JWT) if successful.

    Users:

        GET /api/v1/users/ – List all users (admin-only).

        POST /api/v1/users/ – Create a new user (admin-only). Supply JSON { "email": "", "password": "", "first_name": "", "last_name": "" }.

        GET /api/v1/users/<id> – Retrieve a specific user.

        PUT /api/v1/users/<id> – Update user fields (only the owner or an admin). Email and password typically cannot be changed via API for security.

        DELETE /api/v1/users/<id> – Delete a user (owner or admin).

    Places:

        GET /api/v1/places/ – List all places.

        POST /api/v1/places/ – Create a new place (authenticated user). JSON should include "title", "description", "price", "latitude", "longitude", etc.

        GET /api/v1/places/<id> – Retrieve a specific place.

        PUT /api/v1/places/<id> – Update a place (only the owner or admin).

        

    Amenities:

        GET /api/v1/amenities/ – List all amenities.

        POST /api/v1/amenities/ – Create a new amenity (admin-only). JSON: { "name": "", "description": "" }.

        GET /api/v1/amenities/<id> – Retrieve a specific amenity.

        PUT /api/v1/amenities/<id> – Update an amenity (admin-only).

       

    Reviews:

        GET /api/v1/reviews/ – List all reviews.

        POST /api/v1/reviews/ – Create a review (authenticated user). JSON: { "text": "", "rating": <int>, "place_id": <id> }. Note: users cannot review their own places, and cannot review the same place twice.

        GET /api/v1/reviews/<id> – Retrieve a specific review.

        PUT /api/v1/reviews/<id> – Update a review (only the review’s author or admin).

        DELETE /api/v1/reviews/<id> – Delete a review (author or admin).






 **Test Files**

You’ll find all test scripts inside the app/tests/ directory:

    test_access_control.py

    test_entities_crud.py

    test_hbnb.sql

    test_login.py

    test_realations.py

    test_relationships.py

    test_sqlalchemy_repository.py

    test_user_repository.py


**Running Tests**

Each test file can be executed individually using the following commands:

```python
python app/tests/test_access_control.py
python app/tests/test_entities_crud.py
python app/tests/test_login.py
python app/tests/test_realations.py
python app/tests/test_relationships.py
python app/tests/test_sqlalchemy_repository.py
python app/tests/test_user_repository.py
```



## Authentication


Log in as admin to get a token
```
curl -X POST -H "Content-Type: application/json" \
     -d '{"email":"admin@hbnb.fr","password":"12345678"}' \
     http://127.0.0.1:5000/api/v1/auth/login

```


Use the token to create an amenity (admin-only)
```
curl -X POST -H "Authorization: Bearer <JWT_TOKEN>" -H "Content-Type: application/json" \
     -d '{"name": "WiFi", "description": "High-speed internet"}' \
     http://127.0.0.1:5000/api/v1/amenities

```
Password hashing (Argon2): User passwords are never stored in plain text. The app uses Argon2 (via Flask-Argon2) to hash passwords with a random salt. Argon2 is a memory-hard function and is considered very secure against attacks.





# How to Log in as Admin in Swagger

To test protected endpoints (admin/user only), follow these steps directly in the Swagger UI:

**1. Obtain a JWT Token via Login**

Scroll down to the auth section.

Click on the POST /api/v1/auth/login endpoint.

Click Try it out and provide :


```
{
  "email": "admin@hbnb.fr",
  "password": "12345678"
}
```

Click Execute.

Copy the returned access_token value from the response.

**2. Authorize with the Token**

Click on the green Authorize button at the top right of the Swagger UI.

In the popup, paste :

Bearer <your_access_token_here>

Click Authorize.

**3. Test Protected Routes**

You are now authenticated as admin in the Swagger UI.

All endpoints that require authentication (and admin rights) will use your JWT automatically.

Try to create an amenity or view all users—admin-only operations.

Note: You can log out by clicking Logout in the same Authorize popup.






![Diagramme Mermaid](mermaid-diagram-2025-07-03-113340.svg)



## Full requirements.txt (copy-paste-ready)

```
Flask>=2.3.0,<3.0
Flask-RESTX>=1.1.0,<2.0
Flask-SQLAlchemy>=3.1.1,<4.0
SQLAlchemy>=2.0.0,<3.0
Flask-JWT-Extended>=4.7.1,<5.0
argon2-cffi==23.1.0
pydantic[email]>=2.6.0,<3.0
Werkzeug>=2.3.0
pytest>=7.0.0,<8.0
```




---

## 👤 Authors

* Hamza Hammadi - https://github.com/Hamza-coder3011 
* Ivane Bagashvili - https://github.com/IvaneHo
* [Holberton School Dijon]  
* Part 3: Auth & DB 
* Date: 26 june to 11 July 2025  

---
