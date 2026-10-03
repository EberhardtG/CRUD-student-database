

# **Student CRUD API – Updated README (with Authentication, Background Tasks & Custom Exceptions)**

## **Overview**
The **Student CRUD API** is a modular FastAPI application that provides:

- Full CRUD operations for student records  
- A secure authentication system using hashed passwords and JWT tokens  
- Simulated background processing for report generation and notifications  
- Centralized custom exception handling  
- Clean separation of routers and subsystems  

The project demonstrates modern FastAPI design patterns using:

- **FastAPI**  
- **SQLAlchemy 2.0 typed ORM**  
- **Pydantic v2**  
- **SQLite**  
- **JWT authentication**  
- **BackgroundTasks** for asynchronous simulation  

---

## **Assignment Requirements**
This project satisfies all assignment requirements, including:

### **Student CRUD**
- Full CRUD operations  
- Filtering by major and minimum GPA  
- Duplicate email protection  
- PATCH using `model_dump(exclude_unset=True)`  
- 404 handling for missing students  
- Clean schema separation (Create, Update, Patch, Response)

### **Authentication**
- Registration  
- Login  
- JWT token issuance  
- Protected routes  
- Password hashing using `pbkdf2_sha256`

### **Custom Exceptions**
- Centralized error classes  
- Consistent JSON error responses  
- Cleaner router logic

### **Background Tasks**
- Asynchronous report generation  
- Status transitions (pending → processing → complete)  
- Notification scheduling  
- In‑memory logging of notifications  

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
Uses:

```
pbkdf2_sha256
```

instead of bcrypt to avoid Windows C‑extension issues.

### **JWT Tokens**
- Signed using HS256  
- Include expiration  
- Store user ID in `sub` claim  
- Used via `Authorization: Bearer <token>`  

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
- `ReportRequest` (for background tasks)

Schemas use Pydantic v2 features such as:

- `model_dump(exclude_unset=True)`  
- `from_attributes=True`  

---

## **CRUD Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students` | Create a student |
| GET | `/students` | List students with filters |
| GET | `/students/{id}` | Retrieve one student |
| PUT | `/students/{id}` | Full replacement update |
| PATCH | `/students/{id}` | Partial update |
| DELETE | `/students/{id}` | Delete student |

---

## **Background Task System (`reports.py`)**
The `reports.py` module provides simulated asynchronous processing using FastAPI’s `BackgroundTasks`.

### **Features**
- In‑memory `reports` store  
- In‑memory `notification_log`  
- Artificial delays using `time.sleep()`  
- Status transitions for reports  
- Notification scheduling  
- JSON request body via `ReportRequest`  

### **Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/reports` | Start report generation (async) |
| GET | `/reports/{id}` | Retrieve report status |
| POST | `/reports/notifications` | Schedule a notification |
| GET | `/reports/notifications/log` | View notification history |

### **Report Lifecycle**
1. `pending`  
2. `processing`  
3. `complete`  

A text file is written to disk to simulate a generated report artifact.

---

## **Custom Exceptions (`exceptions.py`)**
Centralized error classes:

- `NotFoundError` → 404  
- `DuplicateError` → 409  
- `AppValidationError` → 422  
- `AppException` → Base class  

Handled in `main.py` for consistent JSON formatting.

---

## **Updated Project Structure**

```
project/
│
├── app/
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   └── student.py
│   │
│   ├── routers/
│   │   ├── students.py
│   │   ├── auth.py
│   │   └── reports.py
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
└── students2.db
```

---

## **Updated `main.py` Wiring**
Routers are mounted cleanly:

```python
app.include_router(student_router)
app.include_router(auth_router)
app.include_router(reports_router, prefix="/reports", tags=["Reports"])
```

This ensures:

- Student endpoints → `/students/...`  
- Auth endpoints → `/auth/...`  
- Report endpoints → `/reports/...`  

---

## **Installation**

### Clone the repository
```
git clone <repo-url>
cd student-api
```

### Create a virtual environment
```
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies
```
pip install -r requirements.txt
```

---

## **Running the Application**
```
uvicorn app.main:app --reload
```

- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

## **Testing**
All endpoints tested via Swagger UI:

- Authentication flow  
- Protected routes  
- Student CRUD  
- Filtering  
- PATCH behavior  
- Custom exceptions  
- Background report generation  
- Notification scheduling  
- Notification log retrieval  

---

## **Key Design Decisions**
- Centralized exception handling  
- SQLAlchemy 2.0 typed ORM  
- Clean schema separation  
- BackgroundTasks for async simulation  
- In‑memory stores for easy testing  
- Modular router organization  
- JWT authentication for secure access  

---

## **Author**
**Grant Eberhardt**

