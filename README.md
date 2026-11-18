# Student CRUD API

## Overview

Student CRUD API is a modular FastAPI application that demonstrates modern backend development using FastAPI, SQLAlchemy 2.0, Pydantic v2, JWT authentication, and automated testing.

The project implements:

- Full Student CRUD operations
- JWT-based authentication
- Password hashing using pbkdf2_sha256
- Background task processing
- Custom exception handling
- Input validation and sanitization
- CORS protection
- Rate limiting
- Automated testing with pytest
- Swagger and ReDoc API documentation

---

## Technology Stack

- FastAPI
- SQLAlchemy 2.0
- Pydantic v2
- SQLite
- Passlib
- JWT (python-jose)
- Pytest

---

## Features

### Student CRUD

The API supports complete CRUD functionality:

| Method | Endpoint | Description |
|----------|------------|------------|
| POST | `/students` | Create student |
| GET | `/students` | Retrieve all students |
| GET | `/students/{id}` | Retrieve student by ID |
| PUT | `/students/{id}` | Full update |
| PATCH | `/students/{id}` | Partial update |
| DELETE | `/students/{id}` | Delete student |

### Filtering

Retrieve students by:

- Major
- Minimum GPA

Example:

```http
GET /students?major=Computer Science
```

```http
GET /students?min_gpa=3.5
```

---

## Student Model

| Field | Type | Description |
|---------|---------|---------|
| id | Integer | Primary Key |
| name | String(75) | Required |
| email | String(100) | Required, Unique |
| major | String(50) | Optional |
| gpa | Float | Optional (0.0–4.0) |
| hashed_password | String(255) | Used for authentication |

Database-level GPA validation is enforced using a SQLAlchemy CheckConstraint.

---

## Authentication

### Registration

```http
POST /auth/register
```

Creates a new user account.

### Login

```http
POST /auth/token
```

Returns a JWT access token.

### Current User

```http
GET /auth/me
```

Returns information about the authenticated user.

### Protected Dashboard

```http
GET /auth/dashboard
```

Example protected route requiring a valid JWT.

---

## Security Features

### Password Hashing

Passwords are hashed using:

```python
pbkdf2_sha256
```

### JWT Authentication

- HS256 signing
- User ID stored in `sub`
- Expiration included

### Duplicate Email Protection

Attempts to create a student with an existing email return:

```http
409 Conflict
```

### Input Sanitization

Student creation sanitizes:

- HTML tags
- Leading/trailing whitespace

### CORS

Only approved origins are allowed.

### Rate Limiting

Custom middleware limits request volume and returns:

```http
429 Too Many Requests
```

when exceeded.

---

## Custom Exceptions

The API uses centralized exception classes:

| Exception | Status Code |
|------------|------------|
| NotFoundError | 404 |
| DuplicateError | 409 |
| AppValidationError | 422 |

All exceptions return consistent JSON responses.

---

## Background Tasks

The reporting subsystem demonstrates asynchronous processing using FastAPI BackgroundTasks.

### Endpoints

| Method | Endpoint |
|----------|------------|
| POST | `/reports` |
| GET | `/reports/{id}` |
| POST | `/reports/notifications` |
| GET | `/reports/notifications/log` |

### Features

- Report generation
- Status tracking
- Notification scheduling
- In-memory storage
- Logging support

---

## Project Structure

```text
app/
├── main.py
├── database.py
├── auth.py
├── exceptions.py
├── models/
│   └── student.py
├── routers/
│   ├── auth.py
│   ├── crud_endpoints.py
│   └── reports.py
├── schemas/
│   ├── auth.py
│   ├── studentcreate.py
│   ├── studentupdate.py
│   ├── studentpatch.py
│   └── studentresponse.py
└── tests/
    ├── conftest.py
    └── test_students.py
```

---

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## Testing

Run the test suite:

```bash
pytest -v
```

The test suite validates:

- Student creation
- Listing students
- Retrieve by ID
- Partial updates
- Delete operations
- Duplicate email protection
- Validation errors
- Exception handling

---

## Author

Grant Eberhardt

Student CRUD API Project