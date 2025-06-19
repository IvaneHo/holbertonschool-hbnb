<<<<<<< HEAD

# Task 1 – Business Logic Class Diagram

## Introduction

This document describes the main structure of the “Business Logic” layer of our HBnB project.  
Here, we define the key entities of the application (`User`, `Place`, `Review`, and `Amenity`) with their attributes, methods, and how they relate to each other.

The goal is to have a clear foundation for implementing features like place creation, leaving reviews, and managing users.

---

![Diagramme de classe Exo 1 drawio](https://github.com/user-attachments/assets/56d98539-aa47-4a79-accd-0112bc6d7b12)

---
## Main Classes

### 1. User
Represents a registered user of the platform.  
Can be either a regular client or an administrator (via the `is_admin` field).

**Attributes**:
- `id`, `first_name`, `last_name`, `email`, `password`
- `is_admin` (true or false)
- `created_at`, `updated_at`

**Methods**:
- `register()`, `updateProfile()`, `deleteAccount()`

A user can:
- create places
- write reviews

---

### 2. Place
A property listed by a user (house, apartment, etc.).

**Attributes**:
- `title`, `description`, `city`, `price`, `latitude`, `longitude`
- `created_at`, `updated_at`

**Methods**:
- `create()`, `update()`, `delete()`
- `list()`, `listByPlace()`

A place can have multiple amenities and reviews.

---

### 3. Review
Feedback left by a client on a place.

**Attributes**:
- `rating` (1 to 5)
- `comment` (optional text)
- `created_at`, `updated_at`

**Methods**:
- `create()`, `update()`, `delete()`

Each review is linked to a user and a place.

---

### 4. Amenity
A feature or service available at a place (e.g., Wi-Fi, pool, AC...).

**Attributes**:
- `name`, `description`
- `created_at`, `updated_at`

**Methods**:
- `list()`

One amenity can be shared by several places, and one place can have several amenities → many-to-many relationship.

---

## Summary of Relationships

| Relationship | Explanation |
|--------------|-------------|
| One `User` → many `Places`   | A user can list multiple places |
| One `User` → many `Reviews`  | A user can write multiple reviews |
| One `Place` → many `Reviews` | A place can receive many reviews |
| `Place` ⟷ `Amenity` (many-to-many) | Places and amenities are linked both ways |

---

## Conclusion

This class diagram is the foundation for implementing the core logic of HBnB Evolution.  
We followed Holberton’s requirements (timestamps, unique IDs, user roles), and created a clean structure to make development easier and clearer.




=======
# 🧩 task-1.md – Business Logic Class Diagram

## 🧭 Overview

This document presents the **class diagram** of the HBnB Evolution application’s **Business Logic Layer**.  
It describes the structure, attributes, methods, and relationships between the main domain entities.

The diagram focuses on four core classes:
- `User`
- `Place`
- `Review`
- `Amenity`

These classes define the heart of the system's behavior, following object-oriented principles and aligned with the high-level architecture.

---

## 🧱 Class Responsibilities

### 👤 User
- Represents a registered user of the platform
- Can **own multiple places** and **write reviews**
- Core attributes include identity, contact details, role and timestamps

**Attributes**
- `UUID id`
- `string first_name`, `last_name`, `email`, `password`
- `bool is_admin`
- `datetime created_at`, `updated_at`

**Methods**
- `register()`
- `updateProfile()`
- `deleteAccount()`

### 🏠 Place
- Represents a property listed by a user
- Can be **linked to multiple amenities** and **reviewed by users**
- Contains geographical data and pricing

**Attributes**
- `UUID id`
- `string title`, `description`, `city`
- `float price`, `latitude`, `longitude`
- `datetime created_at`, `updated_at`

**Methods**
- `create()`, `update()`, `delete()`
- `list()`
- `listByPlace(place_id)`

### 🗣️ Review
- A feedback left by a user **about a place**
- Includes a score and an optional comment

**Attributes**
- `UUID id`
- `int rating`
- `string comment`
- `datetime created_at`, `updated_at`

**Methods**
- `create()`, `update()`, `delete()`

### 🛋️ Amenity
- Describes a feature or service available in a place
- Can be **shared between multiple places**

**Attributes**
- `UUID id`
- `string name`, `description`
- `datetime created_at`, `updated_at`

**Methods**
- `list()`

---

## 🔁 Class Relationships

| Relationship | Description |
|--------------|-------------|
| `User` 1 ⟶ * `Place`     | A user can own multiple places |
| `User` 1 ⟶ * `Review`    | A user can write many reviews |
| `Place` 1 ⟶ * `Review`   | A place can receive many reviews |
| `Place` * ⟷ * `Amenity`  | Many-to-many between places and amenities |

---

## 🖼️ Class Diagram

![Diagramme de classe Exo 1 drawio](https://github.com/user-attachments/assets/56d98539-aa47-4a79-accd-0112bc6d7b12)


---

## ✅ Summary

This class diagram provides a solid foundation for implementing the business logic of HBnB Evolution.  
It defines **clear responsibilities**, **data encapsulation**, and consistent relationships among entities, supporting operations like user registration, place creation, and review submission in a maintainable way.
>>>>>>> dev
