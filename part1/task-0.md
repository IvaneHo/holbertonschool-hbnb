
# task-0.md – High-Level Package Diagram

## General Overview

This document explains the overall architecture of the HBnB Evolution application.  
We chose a **three-layer structure** to clearly separate user interactions, business logic, and data storage.

## Architecture Diagram
---

![Diagramme de haut lvl exo 0 drawio](https://github.com/user-attachments/assets/253c9356-c659-48c0-a1f4-87212ed850df)



---
*(The diagram shows three main packages: PresentationLayer, BusinessLogicLayer, and PersistenceLayer, with an HBnBFacade interface connecting the first two.)*

## The Three Layers

### 1. Presentation Layer

This is where the user interacts with the system through API calls.  
It includes **services** like `UserService`, `PlaceService`, etc., which receive the requests and then call the facade.

### 2. Business Logic Layer

This layer contains the **managers** (`UserManager`, `PlaceManager`, etc.) that apply the business rules.  
Everything goes through the **`HBnBFacade`**, which acts as a single entry point to this layer.  
It also includes models like `User`, `Place`, `Review`, and `Amenity`.

### 3. Persistence Layer

This layer handles **repositories** (like `UserRepository`, etc.) which directly interact with the database.  
Only the business logic layer uses this — not the services.

## Why the HBnBFacade?

We added the facade to keep the architecture clean.  
It provides a **central interface** for accessing business logic, so the services don’t have to know the details.  
It makes the system easier to maintain and test.

## Example Flow

Let’s say a user wants to create a place. Here’s how the system handles it:

→ The **Service** receives the request  
→ It calls the **Facade**  
→ The Facade calls the relevant **Manager**  
→ The Manager uses a **Repository**  
→ The Repository interacts with the **database**

## Conclusion

This 3-layer structure, with a facade in the middle, helps keep the project well-organized, easy to maintain, and scalable in the long run.


