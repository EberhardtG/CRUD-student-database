
# **Student CRUD API – Updated README (Logging‑Enhanced Version)**

## **Overview**
The **Student CRUD API** is a modular FastAPI application that provides:

- Full CRUD operations for student records  
- A secure authentication system using hashed passwords and JWT tokens  
- Background task simulation for report generation and notifications  
- Centralized custom exception handling  
- Security enhancements including CORS hardening, rate limiting, and input sanitization  
- **Full logging support for background tasks and API activity**  
- Professional API documentation using summaries, Markdown docstrings, and schema examples  
- Clean separation of routers, schemas, models, and subsystems  

The project demonstrates modern FastAPI design patterns using:

- **FastAPI**  
- **SQLAlchemy 2.0 typed ORM**  
- **Pydantic v2**  
- **SQLite**  
- **JWT authentication**  
- **BackgroundTasks**  
- **Python logging module**  

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
- Status transitions  
- Notification scheduling  
- In‑memory logging  
- **Full logging of task lifecycle events**  

### **Security Enhancements**
- Strict CORS configuration  
- Custom rate‑limiting middleware  
- Input sanitization  

### **Documentation Enhancements**
- App‑level metadata (title, description, version)  
- Tag descriptions for routers  
- Markdown docstrings for all endpoints  
- Summaries for major endpoints  
- Documented error responses (404, 409, 422, 401, 429)  
- `json_schema_extra` examples for all response models  

---

# **Security Enhancements**

## **CORS Hardening**
Restricts API usage to trusted frontends:

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
- Allows **10 requests per minute per IP**  
- Returns **429 Too Many Requests** when exceeded  

## **Input Sanitization**
`StudentCreate` removes:

- HTML tags  
- Leading/trailing whitespace  

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

Includes a GPA `CheckConstraint`.

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
Uses `pbkdf2_sha256` for Windows compatibility.

### **JWT Tokens**
- HS256 signing  
- Expiration included  
- User ID stored in `sub` claim  

---

# **Pydantic Schemas (v2)**

Implemented schemas:

- `StudentCreate`  
- `StudentUpdate`  
- `StudentPatch`  
- `StudentResponse`  
- `UserCreate`  
- `LoginRequest`  
- `UserResponse`  
- `TokenResponse`  
- `TokenData`  
- `ReportRequest`  

Schemas use:

- `model_dump(exclude_unset=True)`  
- `from_attributes=True`  
- `json_schema_extra` examples  

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

All endpoints include:

- Markdown docstrings  
- Summaries  
- Documented error responses  

---

# **Background Task System**

### **Features**
- In‑memory report store  
- In‑memory notification log  
- Artificial delays  
- Status transitions  
- Notification scheduling  
- **Full logging of background task lifecycle**  
- **Error logging for failed tasks**  

### **Logging Behavior**
The `reports.py` module initializes a logger:

```python
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
```

All background tasks log:

- Task start  
- Status transitions  
- Completion  
- File creation  
- Notification delivery  
- Errors  

This makes background processing fully traceable and debuggable.

### **Endpoints**
| Method | Endpoint                         | Description |
|--------|-----------------------------------|-------------|
| POST   | `/reports`                        | Start report generation |
| GET    | `/reports/{id}`                   | Retrieve report status |
| POST   | `/reports/notifications`          | Schedule a notification |
| GET    | `/reports/notifications/log`      | View notification history |

---

# **Custom Exceptions**

- `NotFoundError` → 404  
- `DuplicateError` → 409  
- `AppValidationError` → 422  
- `AppException` → Base class  

Handled globally for consistent JSON formatting.

---

# **Logging System**

### **Log File**
All logs are written to:

```
app.log
```

### **Logged Events**
- Report creation  
- Report status transitions  
- Report completion  
- File generation  
- Notification scheduling  
- Notification delivery  
- Errors in background tasks  
- Errors in API endpoints  

This provides full visibility into asynchronous behavior and makes debugging straightforward.

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
│   │   ├── students.py
│   │   ├── auth.py
│   │   └── reports.py   <-- logging added here
│   ├── schemas/
│   ├── exceptions.py
│   └── app.log          <-- log file generated at runtime
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

The project includes a full pytest suite validating Student CRUD behavior, error handling, and input validation.

### **Coverage**
- Creating students (valid + invalid)  
- Listing students  
- Fetching by ID  
- Partial updates  
- Deleting students  
- Duplicate email protection  
- Validation errors  

### **Test Isolation**
- Dedicated SQLite test DB  
- Overridden `get_db` dependency  
- Automatic table creation/teardown  
- Rate‑limiting disabled during tests  

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
- **Full logging system for background tasks and API activity**  
- In‑memory stores for easy testing  
- Modular router organization  
- JWT authentication  
- CORS hardening  
- Custom rate limiting  
- Input sanitization  
- Full pytest suite  
- Professional API documentation  

---

# **Author**
**Grant Eberhardt**



Just tell me.
