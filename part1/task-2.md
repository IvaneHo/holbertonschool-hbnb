
# task-2.md – API Sequence Diagrams

## Overview

This document describes four key user interactions in the HBnB Evolution system, using sequence diagrams to illustrate the internal flow. These flows cover the registration, creation, review, and filtering functionalities. The architecture follows a three-layer pattern: Presentation → Business → Persistence.

Each use case shares a common logic path:

Service → HBnBFacade → Manager → Repository → Database

---

## 1. User Registration

The process for registering a new user.

### Steps
- `UserService` receives the registration request and validates inputs.
- It forwards the call to `HBnBFacade`, which delegates to `UserManager`.
- `UserManager` creates a new user.
- `UserRepository` persists the user in the database.

![User Registration Sequence](https://github.com/user-attachments/assets/4a9dda9d-ee52-463c-8753-2a4a413dc4c6)

---

## 2. Place Creation

This covers the submission of a new place by an authenticated user.

### Steps
- `PlaceService` handles the input and passes it to `HBnBFacade`.
- The Facade calls `PlaceManager`, which creates a new place object.
- The object is stored using `PlaceRepository`.

![Place Creation Sequence](https://github.com/user-attachments/assets/1a9113cc-4e77-4a75-92e0-cef352c89dd9)

---

## 3. Review Submission

A user provides feedback for a place they have visited.

### Steps
- `ReviewService` collects and validates review data.
- It calls `HBnBFacade`, which uses `ReviewManager`.
- `ReviewManager` uses `validateUserHasVisitedPlace()` to verify access.
- If confirmed, `ReviewRepository` stores the review.

![Review Submission Sequence](https://github.com/user-attachments/assets/f7c8d85f-d265-49ca-9cce-eca7afe6679f)

---

## 4. Fetching Places by Criteria

A client filters places by maximum price or other criteria.

### Steps
- `PlaceService` receives the GET request.
- It forwards the query to `HBnBFacade`, which contacts `PlaceManager`.
- `PlaceManager` filters data using `PlaceRepository`.
- Matching places are returned.

![Fetching Places Sequence](https://github.com/user-attachments/assets/62f0f07c-34cd-4a9f-8ce2-5cf1cc72180e)

---

