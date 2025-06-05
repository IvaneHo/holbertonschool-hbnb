
# Task 1 – Business Logic Class Diagram

## Introduction

This document describes the main structure of the “Business Logic” layer of our HBnB project.  
Here, we define the key entities of the application (`User`, `Place`, `Review`, and `Amenity`) with their attributes, methods, and how they relate to each other.

The goal is to have a clear foundation for implementing features like place creation, leaving reviews, and managing users.

---
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




