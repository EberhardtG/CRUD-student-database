

# **Student CRUD API – Updated README (with Authentication & Custom Exceptions)**

## **Overview**
The **Student CRUD API** is a RESTful web application built with **FastAPI**, **SQLAlchemy 2.0**, **Pydantic v2**, and **SQLite**. It provides a complete CRUD interface for managing student records, along with a secure authentication system using hashed passwords and JWT access tokens.

This project was developed as a course assignment to demonstrate:

- FastAPI endpoint development  
- SQLAlchemy 2.0 typed ORM modeling  
- SQLite database integration  
- Pydantic v2 schema validation  
- JWT authentication  
- Protected routes using FastAPI dependencies  
- Custom exception handling  
- Clean modular application structure  

---

## **Assignment Requirements**
This project satisfies all assignment requirements, including:

- Full CRUD operations  
- Proper schema separation (Create, Update, Patch, Response)  
- Filtering by major and minimum GPA  
- Duplicate email protection  
- 404 handling for missing students  
- PATCH using `model_dump(exclude_unset=True)`  
- Centralized custom exceptions  
- Authentication system with registration, login, and protected endpoints  

---

## **Student Model**
The SQLAlchemy Student model uses typed ORM fields and enforces database‑level constraints.

| Field | Type | Description |
|-------|-------|-------------|
| id | Integer | Primary Key |
| username | String(75) | Required, Unique |
| email | String(100) | Required, Unique |
| hashed_password | String | Required |
| major | String(50) | Optional |
| gpa | Float | Optional, Range 0.0–4.0 |

A `CheckConstraint` ensures GPA values remain within the valid academic range.

---

## **Authentication System**
The API includes a complete authentication flow using JWT tokens.

### **Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/token` | Log in and receive a JWT |
| GET | `/auth/me` | Retrieve the authenticated user |
| GET | `/auth/dashboard` | Example protected endpoint |

### **Password Hashing**
The API uses:

```
pbkdf2_sha256
```

instead of bcrypt due to Windows runtime instability with bcrypt’s native C extensions.  
This ensures secure, stable hashing across all environments.

### **JWT Tokens**
- Signed using HS256  
- Include an expiration timestamp  
- Store the user ID in the `sub` claim  
- Used via the `Authorization: Bearer <token>` header  

Protected endpoints rely on `get_current_user` to validate and decode tokens.

---

## **Pydantic Schemas**
Implemented schemas:

- `StudentCreate`  
- `StudentUpdate`  
- `StudentPatch`  
- `StudentResponse`  
- `UserCreate`  
- `LoginRequest`  
- `UserResponse`  
- `TokenResponse`  

Schemas use Pydantic v2 features such as `model_dump(exclude_unset=True)` and `from_attributes=True`.

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

- ✔ Duplicate email handling (409 Conflict)  
- ✔ Filtering by major  
- ✔ Filtering by minimum GPA  
- ✔ 404 handling for missing students  
- ✔ PATCH using `model_dump(exclude_unset=True)`  
- ✔ Delete endpoint returns a success message  
- ✔ Complete CRUD cycle tested in Swagger UI  
- ✔ **Centralized custom exception handling via `exceptions.py`**  
- ✔ **JWT authentication with protected routes**  

---

## **Custom Exceptions (`exceptions.py`)**
The `exceptions.py` module centralizes reusable error classes:

- `NotFoundError` → **404 Not Found**  
- `DuplicateError` → **409 Conflict**  
- `AppValidationError` → **422 Unprocessable Entity**  
- `AppException` → Base class  

These exceptions are raised inside routers and converted into structured JSON responses by handlers in `main.py`.

### **Benefits**
- Cleaner router code  
- Consistent error formatting  
- Centralized error definitions  
- Better maintainability  

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
│   │   ├── students.py
│   │   └── auth.py
│   │
│   ├── schemas/
│   │   ├── studentcreate.py
│   │   ├── studentupdate.py
│   │   ├── studentpatch.py
│   │   ├── studentresponse.py
│   │   └── auth.py
│   │
│   ├── exceptions.py
│   └── auth.py
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
uvicorn app.main:app --reload
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
| username | String(75) | Required, Unique |
| email | String(100) | Required, Unique |
| hashed_password | String | Required |
| major | String(50) | Optional |
| gpa | Float | Optional |
| gpa_range | CheckConstraint | 0.0 ≤ gpa ≤ 4.0 |

Validation is enforced at both:

- Pydantic layer  
- Database constraint layer  

---

## **API Endpoints**

### **Create Student — POST `/students`**
Duplicate email → **409 Conflict**  
Handled by `DuplicateError`.

---

### **List Students — GET `/students`**
Supports filters:

- `?major=Computer Science`
- `?min_gpa=3.5`

---

### **Retrieve Student — GET `/students/{id}`**
Missing student → **404 Not Found**  
Handled by `NotFoundError`.

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
Returns:

```json
{ "message": "Student deleted successfully", "id": 1 }
```

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
- **Username:** 1–75 chars, unique  
- **Email:** required, unique, 3–100 chars  
- **Major:** optional, max 50 chars  
- **GPA:** 0.0–4.0  

---

## **Testing**
All endpoints tested via Swagger UI:

- Register user  
- Log in  
- Authorize with JWT  
- Access protected endpoints  
- Create student  
- Retrieve student  
- List students  
- Filter students  
- PUT update  
- PATCH update  
- Delete student  
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
Handled before DB commit using custom exceptions.

### **PATCH Support**
Only updates provided fields.

### **JWT Authentication**
Secure login and protected routes using `get_current_user`.

---

## **Author**
**Grant Eberhardt**

---

