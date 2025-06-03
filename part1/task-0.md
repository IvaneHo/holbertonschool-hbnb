# 📦 task-0.md – High-Level Package Diagram

## 🧭 Overview

This document describes the **high-level architecture** of the HBnB Evolution application, which is based on a **simplified three-layer model**. The system separates user interactions, business logic, and data persistence into distinct packages, improving **maintainability** and **scalability**.

---

## 🗂️ Architecture Diagram

```
```

---

## 🧱 Layer Responsibilities

### 🎯 1. **Presentation Layer**
- Handles **HTTP requests** and **responses**
- Performs **input validation** and **output formatting**
- Delegates all calls to business logic through the `HBnBFacade`

### 🧠 2. **Business Logic Layer**
- Contains **core domain logic** and business rules
- Manages entities like `User`, `Place`, `Review`, and `Amenity`
- Delegates data access to repositories in the persistence layer

### 💾 3. **Persistence Layer**
- Manages **database operations**
- Implements repository classes that **abstract CRUD logic**
- Ensures **data integrity** and clean separation from domain logic

---

## 🔁 Communication Flow

Each major interaction (e.g. user registration, place creation, or review submission)  
follows a **consistent and modular flow**:

**Service → HBnBFacade → Business Logic → Repository → Database**

This structure:
- ✅ Promotes **separation of concerns**
- 🧪 Improves **testability**
- 🧩 Centralizes logic access via `HBnBFacade`

---

## ✅ Summary

This three-layer architecture, enhanced by the **Facade Pattern**, provides a **clean and unified interface** (`HBnBFacade`) for interacting with business operations. It reinforces the application’s **modularity**, **maintainability**, and supports future **feature expansion** with minimal coupling.