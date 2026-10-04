
# **Student CRUD API – Final Updated README**

## **Overview**
The **Student CRUD API** is a modular FastAPI application that provides:

- Full CRUD operations for student records  
- A secure authentication system using hashed passwords and JWT tokens  
- Background task simulation for report generation and notifications  
- Centralized custom exception handling  
- Security enhancements including CORS hardening, rate limiting, and input sanitization  
- Clean separation of routers, schemas, models, and subsystems  

The project demonstrates modern FastAPI design patterns using:

- **FastAPI**  
- **SQLAlchemy 2.0 typed ORM**  
- **Pydantic v2**  
- **SQLite**  
- **JWT authentication**  
- **BackgroundTasks** for asynchronous simulation  

---

## **Assignment Requirements**

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

### **Security Enhancements**
- Strict CORS configuration  
- Custom rate‑limiting middleware  
- Input sanitization to prevent stored XSS  

---

# **Security Enhancements**

## **CORS Hardening**
Strict CORS configuration restricts API usage to trusted frontends:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## **Rate‑Limiting Middleware**
A simple global rate limiter:

- Allows **10 requests per minute per IP**
- Returns **429 Too Many Requests** when exceeded

## **Input Sanitization**
The `StudentCreate` schema strips HTML tags and whitespace from:

- `username`
- `major`

This prevents stored XSS and ensures clean data.

---

# **Student Model**

| Field     | Type         | Description |
|-----------|--------------|-------------|
| id        | Integer      | Primary Key |
| username  | String(75)   | Required, Unique |
| email     | String(100)  | Required, Unique |
| major     | String(50)   | Optional |
| gpa       | Float        | Optional, Range 0.0–4.0 |

A `CheckConstraint` ensures GPA values remain valid.

---

# **Authentication System**

### **Endpoints**
| Method | Endpoint        | Description |
|--------|------------------|-------------|
| POST   | `/auth/register` | Create a new user |
| POST   | `/auth/token`    | Log in and receive a JWT |
| GET    | `/auth/me`       | Retrieve authenticated user |
| GET    | `/auth/dashboard`| Example protected route |

### **Password Hashing**
Uses `pbkdf2_sha256` for cross‑platform compatibility.

### **JWT Tokens**
- HS256 signing  
- Expiration included  
- User ID stored in `sub` claim  

---

# **Pydantic Schemas**

Implemented schemas:

- `StudentCreate`  
- `StudentUpdate`  
- `StudentPatch`  
- `StudentResponse`  
- `UserCreate`  
- `LoginRequest`  
- `UserResponse`  
- `TokenResponse`  
- `ReportRequest`  

Schemas use Pydantic v2 features:

- `model_dump(exclude_unset=True)`  
- `from_attributes=True`  

---

# **CRUD Endpoints**

| Method | Endpoint              | Description |
|--------|------------------------|-------------|
| POST   | `/students`           | Create a student |
| GET    | `/students`           | List students with filters |
| GET    | `/students/{id}`      | Retrieve one student |
| PUT    | `/students/{id}`      | Full update |
| PATCH  | `/students/{id}`      | Partial update |
| DELETE | `/students/{id}`      | Delete student |

---

# **Background Task System**

### **Features**
- In‑memory report store  
- In‑memory notification log  
- Artificial delays using `time.sleep()`  
- Status transitions  
- Notification scheduling  

### **Endpoints**
| Method | Endpoint                         | Description |
|--------|-----------------------------------|-------------|
| POST   | `/reports`                        | Start report generation |
| GET    | `/reports/{id}`                   | Retrieve report status |
| POST   | `/reports/notifications`          | Schedule a notification |
| GET    | `/reports/notifications/log`      | View notification history |

---

# **Custom Exceptions**

Centralized error classes:

- `NotFoundError` → 404  
- `DuplicateError` → 409  
- `AppValidationError` → 422  
- `AppException` → Base class  

Handled globally for consistent JSON formatting.

---

# **Project Structure**

```
project/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── exceptions.py
│   └── auth.py
│
├── app/tests/
│   ├── conftest.py
│   └── test_students.py
│
├── requirements.txt
└── students.db
```

---

# **Running the Application**

```
uvicorn app.main:app --reload
```

Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

# **Testing Suite**

The project includes a full pytest suite validating Student CRUD behavior, error handling, and input validation. Tests run against an isolated SQLite test database using FastAPI’s dependency‑override system.

### **Coverage**
- Creating students (valid + invalid)  
- Listing students  
- Fetching by ID (valid + nonexistent)  
- Partial updates (PATCH)  
- Deleting students  
- Duplicate email protection  
- Validation errors (422)  

### **Test Isolation**
- Dedicated SQLite test DB  
- Overridden `get_db` dependency  
- Automatic table creation/teardown  
- Rate‑limiting middleware disabled during tests  

### **Run Tests**

```
pytest -v
```

Expected:

```
8 passed
```

---

# **Key Design Decisions**

- Centralized exception handling  
- SQLAlchemy 2.0 typed ORM  
- Clean schema separation  
- BackgroundTasks for async simulation  
- In‑memory stores for easy testing  
- Modular router organization  
- JWT authentication  
- CORS hardening  
- Custom rate limiting  
- Input sanitization  
- Full pytest suite for CRUD validation  

---

# **Author**
**Grant Eberhardt**
