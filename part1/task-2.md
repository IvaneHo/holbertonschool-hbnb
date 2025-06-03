# 🧾 task-2.md – API Sequence Diagrams

## 🧭 Overview

This document presents **four sequence diagrams** representing how the HBnB Evolution application handles major user interactions. Each flow demonstrates communication from the **Presentation Layer**, through the **HBnBFacade**, down to the **Persistence Layer** via manager and repository components.

All interactions follow this common flow:

**Service → HBnBFacade → Manager → Repository → Database**

---

## 1️⃣ User Registration

A new user sends a POST request to create an account.

**Flow steps:**
- `UserService` receives the request and validates the input
- Delegates to `HBnBFacade` → `UserManager`
- `UserManager` creates a `User` instance
- `UserRepository` saves it to the database

![User Registration](https://github.com/user-attachments/assets/YOUR_ID/Diagramme%20de%20sequence%20User%20Regestration%20exo%202%20part1.png)

---

## 2️⃣ Place Creation

An authenticated user submits a new place.

**Flow steps:**
- `PlaceService` validates the data and forwards it to `HBnBFacade`
- The Facade invokes `PlaceManager` to instantiate the new place
- The place is saved through the `PlaceRepository`

![Place Creation](https://github.com/user-attachments/assets/YOUR_ID/Diagramme%20de%20sequence%20Place%20Creation%20exo%202%20part%202.png)

---

## 3️⃣ Review Submission

A user submits a review for a place they've visited.

**Flow steps:**
- `ReviewService` captures the POST data
- `HBnBFacade` passes it to `ReviewManager`
- `ReviewManager` ensures the user visited the place
- If valid, it stores the review using `ReviewRepository`

![Review Submission](https://github.com/user-attachments/assets/YOUR_ID/Diagramme%20de%20sequence%20Review%20Submission%20exo%202%20part%203.png)

---

## 4️⃣ Fetching Places (with Filter)

A client fetches places filtered by a maximum price.

**Flow steps:**
- `PlaceService` receives a GET request with filters
- It calls `HBnBFacade`, which forwards to `PlaceManager`
- `PlaceManager` queries the repository with appropriate criteria
- A list of places is returned

![Fetching Places](https://github.com/user-attachments/assets/YOUR_ID/Diagramme%20de%20sequence%20Fetching%20Places%20exo%202%20part%204.png)

---

## ✅ Summary

These diagrams illustrate the structured flow across all layers of the system using the **Facade Pattern**. They:
- Maintain a **clean separation of concerns**
- **Centralize business rules** via `HBnBFacade`
- Ensure modular, scalable interaction flows
