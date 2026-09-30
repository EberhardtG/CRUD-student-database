
# **Student CRUD API – Updated README (with `exceptions.py`)**

## **Overview**
The **Student CRUD API** is a RESTful web application built with **FastAPI**, **SQLAlchemy 2.0**, **Pydantic v2**, and **SQLite**. It provides a complete CRUD interface for managing student records while enforcing strong validation, database integrity, and clean REST API design.

This project was developed as a course assignment to demonstrate:

- FastAPI endpoint development  
- SQLAlchemy ORM integration  
- SQLite database management  
- Pydantic schema validation  
- CRUD operations  
- HTTP status code handling  
- Swagger UI testing  
- Custom exception handling using FastAPI exception classes  

---

## **Assignment Requirements**
This project satisfies all assignment requirements, now including centralized exception handling via `exceptions.py`.

---

## **Student Model**
The SQLAlchemy Student model includes:

| Field | Type | Description |
|-------|-------|-------------|
| id | Integer | Primary Key |
| name | String | Required |
| email | String | Required, Unique |
| major | String | Optional |
| gpa | Float | Optional, Range 0.0–4.0 |

---

## **Pydantic Schemas**
Implemented schemas:

- `StudentCreate`
- `StudentUpdate`
- `StudentPatch`
- `StudentResponse`

---

## **CRUD Endpoints**
All required endpoints are implemented:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students` | Create a student |
| GET | `/students` | List students with filters |
| GET | `/students/{id}` | Retrieve one student |
| PUT | `/students/{id}` | Full replacement update |
| PATCH | `/students/{id}` | Partial update |
| DELETE | `/students/{id}` | Delete student |

---

## **Additional Requirements**
All assignment requirements are met:

- ✅ Duplicate email handling (409 Conflict)  
- ✅ Filtering by major  
- ✅ Filtering by minimum GPA  
- ✅ 404 handling for missing students  
- ✅ PATCH using `model_dump(exclude_unset=True)`  
- ✅ Delete endpoint returns a success message  
- ✅ Complete CRUD cycle tested in Swagger UI  
- ✅ **Centralized custom exception handling via `exceptions.py`**

---

## **New Module: `exceptions.py`**
A new module, **`exceptions.py`**, was added to centralize and standardize error responses across the API.

### **Purpose**
- Provide reusable exception classes  
- Improve consistency of error messages  
- Reduce duplication in CRUD endpoint logic  
- Align with FastAPI best practices  

### **Implemented Custom Exceptions**
Examples of exceptions defined in this module:

- `StudentNotFoundException` → returns **404 Not Found**
- `DuplicateEmailException` → returns **409 Conflict**
- `InvalidGPAException` → returns **422 Unprocessable Entity**

These exceptions are raised inside CRUD operations and automatically converted into structured JSON error responses.

### **Benefits**
- Cleaner router code  
- Centralized error definitions  
- More readable and maintainable project structure  

---

## **Technologies Used**
- Python 3.x  
- FastAPI  
- SQLAlchemy 2.0  
- SQLite  
- Pydantic v2  
- Uvicorn  
- Swagger UI / OpenAPI  

---

## **Project Structure (Updated)**

```
project/
│
├── app/
│   ├── database.py
│   │
│   ├── models/
│   │   └── student.py
│   │
│   ├── routers/
│   │   └── crud_endpoints.py
│   │
│   ├── schemas/
│   │   ├── studentcreate.py
│   │   ├── studentupdate.py
│   │   ├── studentpatch.py
│   │   └── studentresponse.py
│   │
│   ├── exceptions.py   ← **NEW**
│   │
│   └── main.py
│
├── requirements.txt
└── students.db
```

---

## **Installation**

### **Clone the repository**
```
git clone <repo-url>
cd student-api
```

### **Create a virtual environment**

**Windows**
```
python -m venv .venv
.venv\Scripts\activate
```

### **Install dependencies**
```
pip install -r requirements.txt
```

---

## **Running the Application**

Start the FastAPI server:

```
uvicorn main:app --reload
```

- Server: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

## **Database Design**

### **Student Table – `students`**

| Column | Type | Constraints |
|--------|-------|-------------|
| id | Integer | Primary Key |
| name | String(75) | Required |
| email | String(100) | Required, Unique |
| major | String(50) | Optional |
| gpa | Float | Optional |
| gpa_range | CheckConstraint | 0.0 ≤ gpa ≤ 4.0 |

Validation is enforced at both:

- Pydantic layer  
- Database constraint layer  

---

## **API Endpoints**

### **Create Student — POST `/students`**
Request:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "major": "Computer Science",
  "gpa": 3.8
}
```

Duplicate email → **409 Conflict**  
Handled by `DuplicateEmailException`.

---

### **List Students — GET `/students`**
Supports filters:

- `?major=Computer Science`
- `?min_gpa=3.5`
- Combined filters supported

---

### **Retrieve Student — GET `/students/{id}`**
Missing student → **404 Not Found**  
Handled by `StudentNotFoundException`.

---

### **Full Update — PUT `/students/{id}`**
Validates uniqueness and GPA range.

---

### **Partial Update — PATCH `/students/{id}`**
Uses:
```python
model_dump(exclude_unset=True)
```

---

### **Delete Student — DELETE `/students/{id}`**
Success:
```json
{ "message": "Student deleted successfully", "id": 1 }
```

Missing student → **404 Not Found**

---

## **Validation & Error Handling**

### **HTTP Status Codes**
| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 404 | Student Not Found |
| 409 | Duplicate Email |
| 422 | Validation Error |

### **Validation Rules**
- **Name:** 1–75 chars  
- **Email:** required, unique, 3–100 chars  
- **Major:** optional, max 50 chars  
- **GPA:** 0.0–4.0  

---

## **Testing**
All endpoints tested via Swagger UI:

- Create  
- Retrieve  
- List  
- Filter  
- PUT update  
- PATCH update  
- Delete  
- Error handling  
- Custom exceptions verified  

---

## **Key Design Decisions**

### **Centralized Exception Handling**
`exceptions.py` ensures consistent error responses and cleaner router logic.

### **SQLAlchemy 2.0 Typed ORM**
Uses modern typing:
```python
Mapped[str]
mapped_column()
```

### **Schema Separation**
Different schemas for create, update, patch, and response.

### **Duplicate Email Protection**
Handled before DB commit using custom exception.

### **PATCH Support**
Only updates provided fields.

---

## **Author**
**Grant Eberhardt**

---
