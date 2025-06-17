
# 📘 HBnB Evolution – Customized Technical Documentation

Welcome to the documentation for the **HBnB Evolution** project, a simplified system inspired by AirBnB. This project models the management of users, places, reviews, and associated amenities.

---

## 📁 Document Organization

### 1. `task-0.md`: Package Diagram (High-Level Architecture)
- Visualization of the 3 main software layers: presentation, business logic, persistence  
- Overview of relationships between core system components  
- Use of the **facade pattern** to simplify inter-layer communication  

### 2. `task-1.md`: Business Logic Class Diagram
- UML modeling of core classes: `User`, `Place`, `Review`, `Amenity`  
- Attributes, methods, and relationships (associations, cardinalities)  
- Logical interactions between business entities  

### 3. `task-2.md`: API Sequence Diagrams
- Use case scenarios illustrating how requests are processed from user to database:
  - User registration  
  - Place creation  
  - Review submission  
  - Fetching listings with filters (e.g., by `price`)  

### 4. `task-3.md`: Final Documentation Compilation
- Summary of design choices and all UML diagrams  
- Implementation guidance and architecture consistency  

---

## ⚙️ Core Functionalities

- **Users**: create, update, delete, authenticate  
- **Places**: publish, edit, delete, manage amenities  
- **Reviews**: post reviews tied to users and places  
- **Amenities**: features associated with a place (Wi-Fi, A/C, etc.)  

---

## 🧱 Project Architecture

The system follows a **three-layer architecture**:

- 🎯 **Presentation Layer**: handles user-facing services and REST API  
- 🧠 **Business Logic Layer**: enforces domain rules and object interactions  
- 💾 **Persistence Layer**: handles database access and data storage  

---

## ℹ️ Notes

- All diagrams conform to **UML standards**  
- This repository contains **only the technical documentation** (no source code)  
- Each `.md` file corresponds to a project task with its related diagram and explanation  
