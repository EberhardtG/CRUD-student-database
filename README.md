
# **Student CRUD API – Final Updated README**

## **Overview**
The **Student CRUD API** is a modular FastAPI application that provides:

- Full CRUD operations for student records  
- A secure authentication system using hashed passwords and JWT tokens  
- Simulated background processing for report generation and notifications  
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

## **CORS Hardening (main.py)**

The application uses strict CORS configuration:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### **Why this matters**
- Prevents unauthorized cross‑origin access  
- Restricts API usage to trusted frontends  
- Reduces attack surface compared to wildcard CORS  

---

## **Custom Rate‑Limiting Middleware (main.py)**

A simple, assignment‑compliant rate limiter tracks request timestamps per IP:

- Allows **10 requests per minute**
- Returns **429 Too Many Requests** when exceeded
- Applies globally to all endpoints

### **Testing**
Send any endpoint (e.g., `/students`) 11 rapid requests → expect:

```json
{"detail": "Too Many Requests"}
```

---

## **Input Sanitization (StudentCreate Schema)**

The `StudentCreate` schema sanitizes:

- `username`
- `major`

Sanitization removes:

- HTML tags (including `<script>`)  
- Leading/trailing whitespace  

### **Testing**
Submit:

```json
{
  "username": "<script>alert('x')</script>  Grant",
  "email": "test@example.com",
  "major": "  <b>CS</b> "
}
```

Expect sanitized output:

```json
{
  "username": "Grant",
  "email": "test@example.com",
  "major": "CS"
}
```

---

# **Student Model**

| Field     | Type         | Description |
|-----------|--------------|-------------|
| id        | Integer      | Primary Key |
| username  | String(75)   | Required, Unique |
| email     | String(100)  | Required, Unique |
| major     | String(50)   | Optional |
| gpa       | Float        | Optional, Range 0.0–4.0 |

A `CheckConstraint` ensures GPA values remain within the valid academic range.

---

# **Authentication System**

### **Endpoints**
| Method | Endpoint        | Description |
|--------|------------------|-------------|
| POST   | `/auth/register` | Create a new user account |
| POST   | `/auth/token`    | Log in and receive a JWT |
| GET    | `/auth/me`       | Retrieve the authenticated user |
| GET    | `/auth/dashboard`| Example protected endpoint |

### **Password Hashing**
Uses:

```
pbkdf2_sha256
```

to avoid Windows bcrypt C‑extension issues.

### **JWT Tokens**
- Signed using HS256  
- Include expiration  
- Store user ID in `sub` claim  
- Used via `Authorization: Bearer <token>`  

---

# **Pydantic Schemas**

Implemented schemas:

- `StudentCreate` (sanitized input)  
- `StudentUpdate` (full replacement)  
- `StudentPatch` (partial update)  
- `StudentResponse` (ORM → Pydantic)  
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
| PUT    | `/students/{id}`      | Full replacement update |
| PATCH  | `/students/{id}`      | Partial update |
| DELETE | `/students/{id}`      | Delete student |

---

# **Background Task System (`reports.py`)**

### **Features**
- In‑memory `reports` store  
- In‑memory `notification_log`  
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

Handled in `main.py` for consistent JSON formatting.

---

# **Project Structure**

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
│   │   ├── crud_endpoints.py
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
└── students.db
```

---

# **Running the Application**

```
uvicorn app.main:app --reload
```

- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

# **Testing**

- Authentication flow  
- Protected routes  
- Student CRUD  
- Filtering  
- PATCH behavior  
- Custom exceptions  
- Background report generation  
- Notification scheduling  
- Notification log retrieval  
- Rate‑limiting behavior  
- Sanitization behavior  

---

# **Key Design Decisions**

- Centralized exception handling  
- SQLAlchemy 2.0 typed ORM  
- Clean schema separation  
- BackgroundTasks for async simulation  
- In‑memory stores for easy testing  
- Modular router organization  
- JWT authentication for secure access  
- CORS hardening  
- Custom rate limiting  
- Input sanitization  

---

# **Author**
**Grant Eberhardt**

