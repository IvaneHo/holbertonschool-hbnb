# HBnB - Part 2: RESTful API & Business Logic
## Description

This project is the second part of the AirBnB platform clone.
It focuses on designing a RESTful API using Flask, combined with a clean business architecture featuring validation, service layers (facade), and in-memory persistence.

 ## Architecture

    - **Flask-RESTx** for creating endpoints.

    - **Pydantic** for data validation.

    - **Repositories** to simulate the data layer (InMemory).

    - **Façade** to encapsulate all business logic.

📁 Project Structure

```plaintext
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py
│   ├── tests/
│   │   ├── test_users.py
│   │   ├── test_places.py
│   │   ├── test_reviews.py
│   │   ├── test_amenities.py
├── run.py
├── config.py
├── requirements.txt
├── README.md

```



# Installation Guide
To get started with the project, follow these simple steps:

**Clone the repository**

First, clone the project and navigate into the correct directory:

```python
git clone https://github.com/IvaneHo/holbertonschool-hbnb.git
```


**Set up a virtual environment**

Create a new virtual environment (recommended to avoid dependency issues):

```python
python3 -m venv venv
```

Then activate it:

```python
source venv/bin/activate
```

**Install the required packages**

Once the virtual environment is active, install the dependencies with:

```python
pip install -r requirements.txt
```


**Run the application**

Finally, from within the hbnb directory, you can launch the app by running:

```python
python run.py
```




# Unit Tests

All main entities of the API — User, Place, Amenity, and Review — have been thoroughly tested using Python’s built-in unittest framework.

The tests cover both standard use cases (such as creating, retrieving, updating, and deleting resources) and edge cases, including missing fields, non-existent IDs, and invalid input formats.

 **Test Files**

You’ll find all test scripts inside the app/tests/ directory:

    test_users.py

    test_places.py

    test_reviews.py

    test_amenities.py


**Running Tests**

Each test file can be executed individually using the following commands:

```python
python app/tests/test_users.py
python app/tests/test_places.py
python app/tests/test_reviews.py
python app/tests/test_amenities.py  
```  

**Test Report**

A *test_report.md* file is available at the root of the project.
It provides a summary of the failed test cases (including the encountered errors) along with suggestions for fixing them.

---

## 👤 Authors

* Hamza Hammadi - https://github.com/Hamza-coder3011 
* Ivane Bagashvili - https://github.com/IvaneHo
* [Holberton School Dijon]  
* Part 2: BL and API 
* Date: 12 june to 20 June 2025  

---