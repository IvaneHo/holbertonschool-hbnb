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

![Diagramme de sequence User Regestration exo 2 part1](https://github.com/user-attachments/assets/4a9dda9d-ee52-463c-8753-2a4a413dc4c6)

---

## 2️⃣ Place Creation

An authenticated user submits a new place.

**Flow steps:**
- `PlaceService` validates the data and forwards it to `HBnBFacade`
- The Facade invokes `PlaceManager` to instantiate the new place
- The place is saved through the `PlaceRepository`

![Diagramme de sequence Place Creation exo 2 part 2](https://github.com/user-attachments/assets/1a9113cc-4e77-4a75-92e0-cef352c89dd9)

---

## 3️⃣ Review Submission

A user submits a review for a place they've visited.

**Flow steps:**
- `ReviewService` captures the POST data
- `HBnBFacade` passes it to `ReviewManager`
- `ReviewManager` ensures the user visited the place
- If valid, it stores the review using `ReviewRepository`

![Diagramme de sequence Review Submission exo 2 part 3](https://github.com/user-attachments/assets/f7c8d85f-d265-49ca-9cce-eca7afe6679f)


---

## 4️⃣ Fetching Places (with Filter)

A client fetches places filtered by a maximum price.

**Flow steps:**
- `PlaceService` receives a GET request with filters
- It calls `HBnBFacade`, which forwards to `PlaceManager`
- `PlaceManager` queries the repository with appropriate criteria
- A list of places is returned

![Diagramme de sequence Fetching Places exo 2 part 4](https://github.com/user-attachments/assets/62f0f07c-34cd-4a9f-8ce2-5cf1cc72180e)
---

## ✅ Summary

These diagrams illustrate the structured flow across all layers of the system using the **Facade Pattern**. They:
- Maintain a **clean separation of concerns**
- **Centralize business rules** via `HBnBFacade`
- Ensure modular, scalable interaction flows
