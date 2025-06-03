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

![Class Diagram – Task 1](https://github.com/user-attachments/assets/253c9356-c659-48c0-a1f4-87212ed850df)

---

## ✅ Summary

This class diagram provides a solid foundation for implementing the business logic of HBnB Evolution.  
It defines **clear responsibilities**, **data encapsulation**, and consistent relationships among entities, supporting operations like user registration, place creation, and review submission in a maintainable way.
