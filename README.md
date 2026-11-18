# Student CRUD API

## Overview

Student CRUD API is a modular FastAPI application that demonstrates modern backend development using FastAPI, SQLAlchemy 2.0, Pydantic v2, JWT authentication, background task processing, and automated testing.

The project implements:

- Full Student CRUD operations
- JWT-based authentication
- Password hashing using `pbkdf2_sha256`
- Background task processing using FastAPI `BackgroundTasks`
- Student activity logging
- Notification scheduling
- Report generation and tracking
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
- Python-JOSE (JWT)
- Pytest
- BackgroundTasks
- Python Logging

---

## Features

### Student CRUD

The API supports complete CRUD functionality.

| Method | Endpoint | Description |
|----------|----------|-------------|
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
|---------|---------|-------------|
| id | Integer | Primary Key |
| name | String(75) | Required |
| email | String(100) | Required, Unique |
| major | String(50) | Optional |
| gpa | Float | Optional (0.0–4.0) |

Database-level GPA validation is enforced using a SQLAlchemy `CheckConstraint`.

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
- User ID stored in the `sub` claim
- Token expiration included

### Duplicate Email Protection

Attempts to create a student with an existing email return:

```http
409 Conflict
```

### Input Sanitization

Student creation sanitizes:

- HTML tags
- Leading and trailing whitespace

### CORS

Only approved origins are allowed.

### Rate Limiting

Custom middleware limits request volume and returns:

```http
429 Too Many Requests
```

when exceeded.

---

## Background Tasks

The application demonstrates FastAPI BackgroundTasks in two ways:

### Student CRUD Background Tasks

When a student is created:

- An activity log entry is written
- A notification is scheduled
- The API returns immediately without waiting for the notification to finish

When a student is deleted:

- An activity log entry is written in the background

### Student Activity Logging

Implemented using:

```python
log_activity()
```

Activity entries are written to:

```text
activity_log.txt
```

Example:

```text
2026-11-18 10:30:05 - Student created: Grant
2026-11-18 10:35:22 - Student deleted: Grant
```

### Notification Processing

Implemented using:

```python
send_notification()
```

Notifications simulate a delay using:

```python
time.sleep(2)
```

Notification entries are written to:

```text
notification_log.txt
```

Example:

```text
2026-11-18 10:30:07 - Welcome Grant
```

### Background Task Verification

The assignment requirements are demonstrated by:

- POST requests returning immediately
- Notifications continuing after the response is returned
- Creation activity being written to `activity_log.txt`
- Deletion activity being written to `activity_log.txt`
- Notifications appearing in `notification_log.txt`

---

## Reports Subsystem

The reporting subsystem demonstrates additional asynchronous processing using FastAPI BackgroundTasks.

### Endpoints

| Method | Endpoint |
|----------|----------|
| POST | `/reports` |
| GET | `/reports/{report_id}` |
| POST | `/reports/notifications` |
| GET | `/reports/notifications/log` |

### Features

- Report generation
- Status tracking
- Notification scheduling
- In-memory storage
- Logging support

### Report Status Flow

```text
pending
   ↓
processing
   ↓
complete
```

---

## Logging

The reports subsystem logs background task activity to:

```text
app.log
```

Logged events include:

- Report generation started
- Status transitions
- Report completion
- File creation
- Notification scheduling
- Notification delivery
- Background task errors

This provides visibility into asynchronous operations and simplifies debugging.

---

## Project Structure

```text
app/
├── main.py
├── auth.py
├── database.py
├── exceptions.py
│
├── models/
│   └── student.py
│
├── routers/
│   ├── auth.py
│   ├── crud_endpoints.py
│   └── reports.py
│
├── schemas/
│   ├── auth.py
│   ├── studentcreate.py
│   ├── studentupdate.py
│   ├── studentpatch.py
│   └── studentresponse.py
│
├── utils/
│   ├── __init__.py
│   └── notifications.py
│
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

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

## Testing

Run the test suite:

```bash
pytest -v
```

Expected result:

```text
8 passed
```

### Test Coverage

- Student creation
- Student retrieval
- Student updates
- Student deletion
- Duplicate email protection
- Validation errors
- HTTP 404 handling
- PATCH functionality

### Test Isolation

- Dedicated SQLite test database
- Dependency override for `get_db`
- Automatic table creation and teardown
- Rate limiting disabled during tests

---

## Key Design Decisions

- SQLAlchemy 2.0 typed ORM
- Pydantic v2 schemas
- JWT authentication
- Centralized exception handling
- BackgroundTasks for asynchronous processing
- Student activity logging
- Notification scheduling
- Report generation workflow
- Input sanitization
- Custom rate limiting
- Comprehensive automated testing
- Modular router organization

---

## Author

**Grant Eberhardt**

Student CRUD API Project