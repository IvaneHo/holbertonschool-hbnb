# HBnB - Part 4 : Simple Web Client

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-blue.svg)
![Holberton](https://img.shields.io/badge/Holberton-Project-red.svg)


##  Overview

This project aims to complete and integrate a responsive front-end for the HBNB web application (an Airbnb clone), according to provided design specifications and full API connectivity.

Key deliverables:

    Login form

    List of Places (main page)

    Place Details page

    Add Review Form

##  Project Structure

```
part4/hbnb/
├── back/
│   ├── README.md
│   ├── requirements.txt
│   ├── config.py
│   ├── create_tables.py
│   ├── run.py
│   ├── test_config.py
│   ├── instance/
│   │   └── hbnb.dev.db
│   ├── app/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── amenity.py
│   │   │   ├── base_model.py
│   │   │   ├── place.py
│   │   │   ├── place_image.py
│   │   │   ├── reservation.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── amenity.py
│   │   │   ├── place.py
│   │   │   ├── reservation.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   ├── persistence/
│   │   │   ├── __init__.py
│   │   │   ├── amenity_repository.py
│   │   │   ├── place_image_repository.py
│   │   │   ├── place_repository.py
│   │   │   ├── repository.py
│   │   │   ├── reservation_repository.py
│   │   │   ├── review_repository.py
│   │   │   ├── sqlalchemy_repository.py
│   │   │   └── user_repository.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── amenity_service.py
│   │   │   ├── facade.py
│   │   │   ├── place_service.py
│   │   │   ├── reservation_service.py
│   │   │   ├── review_service.py
│   │   │   └── user_service.py
│   │   ├── api/
│   │   │   └── v1/
│   │   ├── scriptSQL/
│   │   │   └── hbnb.sql
│   │   └── tests/
│   │       ├── init_admin.py
│   │       ├── test_access_control.py
│   │       ├── test_entities_crud.py
│   │       ├── test_hbnb.sql
│   │       ├── test_login.py
│   │       ├── test_relations.py
│   │       ├── test_relationships.py
│   │       ├── test_sqlalchemy_repository.py
│   │       └── test_user_repository.py
│   └── .venv/
│       └── ... (environnement virtuel)
├── front/
│   ├── README.md
│   └── static/
│       ├── index.html
│       ├── login.html
│       ├── place.html
│       ├── profile.html
│       ├── scripts/
│       │   ├── index.js
│       │   ├── light.js
│       │   ├── login.js
│       │   ├── place.js
│       │   └── profile.js
│       ├── styles/
│       │   ├── base.css
│       │   ├── index.css
│       │   ├── login.css
│       │   ├── place.css
│       │   ├── profile.css
│       │   └── corbeille/
│       └── images/
│           ├── icon.png
│           ├── icon_bath.png
│           ├── icon_bed.png
│           ├── icon_wifi.png
│           ├── logo.png
│           ├── logo0.1.png
│           └── logo0.2.png


```

Pages to Complete

    Login (login.html):
    Login form (email/password), connects to backend, handles JWT.

    List of Places (index.html):
    Displays all places as cards, dynamic filtering by price, API-connected.

    Place Details (place.html):
    Detailed view of a place, lists amenities and reviews, shows review form if authenticated.

    Add Review:
    Review submission form for authenticated users only.

# Installation Guide
To get started with the project, follow these simple steps:

**Clone the repository**

First, clone the project and navigate into the correct directory:

```
git clone https://github.com/IvaneHo/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part4/hbnb/back
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


**Run the application**

Finally, from within the hbnb directory, you can launch the app by running:

```
python run.py
```
This command starts both the backend API and the static frontend server.
Open your browser and go to: http://127.0.0.1:5000/.

The frontend is available directly from this address (index.html, login.html, place.html, etc.)
The API endpoints are available under /api/v1/

## Authentication

**Login**

Click on Login (or go to /login.html).

Enter a valid email and password (must exist in the database).

```

  email: testuser@hbnb.fr 
  password:12345678
  
          or
  
  email: approuveur@hbnb.fr
  password:12345678


```

Click login.

On success:

    You are redirected to the main page.

    A session cookie with a JWT token is created.


On failure:

    An error message is displayed (invalid credentials).





**View List of Places**

From the homepage (/index.html or /), see the list of available places as cards.

Each card shows:

    Name of the place

    Price per night

    "View Details" button

The list is loaded dynamically via the API.

**Filter Places by Price**
Use the price filter dropdown above the list

The places list updates instantly, filtering out places over the selected price.


**View Place Details**

Click "View Details" on any place card.

This opens the place details page (/place.html?id=PLACE_ID).

The details page shows:

    Full information about the place (price, amenities, description)

    List of existing reviews

    If you are logged in, a button


**Add a Review**

On the place details page, click "Add Review" or fill out the review form (only visible if authenticated).

Write your review and submit.

On success:

    The review is added and displayed on the page.

    A success message appears.

If you are not logged in, you will be redirected to the login or index page.


**Logout**

    Click the logout button/link.

    Your session cookie is deleted, and the login link/button reappears.

**Check Authentication**

    When logged in:

        The login link is hidden, and you may see your profile or a logout link.

    When not logged in:

        The login link is shown, and features like "Add Review" are unavailable.

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
flask-cors==6.0.1
```




---

## 👤 Author

* Ivane Bagashvili - https://github.com/IvaneHo
* [Holberton School Dijon]  
* Part 4: Simple Web Client 
* Date: 17 july to 31 July 2025  

---
