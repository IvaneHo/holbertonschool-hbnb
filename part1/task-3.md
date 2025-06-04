# 📘 HBnB Evolution – Comprehensive Technical Documentation

---

## 📝 Introduction

This document serves as the comprehensive technical blueprint for the **HBnB Evolution** project, an AirBnB-inspired simplified system. It consolidates all technical diagrams and explanatory notes created in previous tasks to clearly guide the implementation and development phases of the application.

The document provides a structured overview of the application’s architecture, business logic, and API interactions, ensuring maintainability and clarity for developers and stakeholders.

---

## 📦 High-Level Architecture

### 🗺️ Package Diagram

![Diagramme de haut lvl exo 0 drawio](https://github.com/user-attachments/assets/253c9356-c659-48c0-a1f4-87212ed850df)

The application follows a clear three-layer architecture:

- **🎯 Presentation Layer**:
  - Handles HTTP requests/responses.
  - Validates user inputs and formats outputs.
  - Communicates exclusively via `HBnBFacade`.

- **🧠 Business Logic Layer**:
  - Contains domain entities (`User`, `Place`, `Review`, `Amenity`) and core logic.
  - Implements business rules and processes requests.
  - Delegates data management to the persistence layer.

- **💾 Persistence Layer**:
  - Manages database operations (CRUD).
  - Abstracts database interactions through repositories.
  - Ensures data integrity and isolation from business logic.

### 🔄 Communication via Facade Pattern (`HBnBFacade`)

The **Facade Pattern** (`HBnBFacade`) centralizes business logic interactions, simplifying the communication from the Presentation Layer to the Business Logic Layer. It ensures:
- Clear separation of concerns.
- Simplified maintenance and testing.
- Unified access to business operations.

---

## 🧩 Business Logic Layer – Class Diagram

![Diagramme de classe Exo 1 drawio](https://github.com/user-attachments/assets/56d98539-aa47-4a79-accd-0112bc6d7b12)

### 🧑 `User`
- **Attributes**: `id`, `first_name`, `last_name`, `email`, `password`, `is_admin`, `created_at`, `updated_at`
- **Methods**:
  - `register()`
  - `update()`
  - `delete()`

### 🏠 `Place`
- **Attributes**: `id`, `title`, `description`, `price`, `latitude`, `longitude`, `user_id`, `created_at`, `updated_at`
- **Methods**:
  - `create()`
  - `update()`
  - `delete()`
  - `listAmenities()`

### 📝 `Review`
- **Attributes**: `id`, `user_id`, `place_id`, `rating`, `comment`, `created_at`, `updated_at`
- **Methods**:
  - `create()`
  - `update()`
  - `delete()`
  - `listByPlace(place_id)`

### ⚙️ `Amenity`
- **Attributes**: `id`, `name`, `description`, `created_at`, `updated_at`
- **Methods**:
  - `create()`
  - `update()`
  - `delete()`

### 🔗 Relationships
- **User – Place**: One-to-many (a user can own many places).
- **Place – Amenity**: Many-to-many (places can have multiple amenities).
- **Place – Review**: One-to-many (a place can have many reviews).
- **User – Review**: One-to-many (a user can create many reviews).

These relationships clearly define interactions and ensure business logic consistency.

---

## 🚦 API Interaction Flow – Sequence Diagrams

The following sequence diagrams illustrate interactions across the system layers for major API calls.

### 🟢 User Registration

![Diagramme de sequence User Regestration exo 2 part1](https://github.com/user-attachments/assets/4a9dda9d-ee52-463c-8753-2a4a413dc4c6)

**Key Steps**:
- User submits registration data.
- `HBnBFacade` delegates to `UserManager` for validation.
- `UserRepository` saves validated data.
- Confirmation returned to user.

---

### 🟡 Place Creation

![Diagramme de sequence Place Creation exo 2 part 2](https://github.com/user-attachments/assets/1a9113cc-4e77-4a75-92e0-cef352c89dd9)

**Key Steps**:
- User submits place details.
- `HBnBFacade` delegates validation and processing to `PlaceManager`.
- `PlaceRepository` saves the new place data.
- Confirmation returned with place details.

---

### 🟠 Review Submission

![Diagramme de sequence Review Submission exo 2 part 3](https://github.com/user-attachments/assets/f7c8d85f-d265-49ca-9cce-eca7afe6679f)

**Key Steps**:
- User submits a review for a specific place.
- `HBnBFacade` delegates validation to `ReviewManager`.
- `ReviewRepository` inserts the review into the database.
- User receives a confirmation.

---

### 🔵 Fetching Places (filtered by criteria)

![Diagramme de sequence Fetching Places exo 2 part 4](https://github.com/user-attachments/assets/62f0f07c-34cd-4a9f-8ce2-5cf1cc72180e)

**Key Steps**:
- User requests list of places based on criteria (`price`, etc.).
- `HBnBFacade` delegates query handling to `PlaceManager`.
- `PlaceRepository` retrieves matching data from database.
- Results are formatted and returned to the user.

---

## 👤 Authors

* Hamza Hammadi - https://github.com/Hamza-coder3011 
* Ivane Bagashvili - https://github.com/IvaneHo
* [Holberton School Dijon]  
* Part 1: HBnB UML 
* Date: 26 may to 6 June 2025  

---