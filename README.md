
Student CRUD API
Overview

The Student CRUD API is a RESTful web application built with FastAPI, SQLAlchemy 2.0, Pydantic v2, and SQLite. The project provides a complete CRUD (Create, Read, Update, Delete) interface for managing student records while enforcing data validation, database integrity, and REST API best practices.

The application was developed as a course assignment to demonstrate:

FastAPI endpoint development
SQLAlchemy ORM integration
SQLite database management
Pydantic schema validation
CRUD operations
HTTP status code handling
Swagger UI testing
Assignment Requirements

This project satisfies all assignment requirements:

Student Model

The Student SQLAlchemy model contains:

Field	Type	Descriptionid	Integer	Primary Key
name	String	Required
email	String	Required, Unique
major	String	Optional
gpa	Float	Optional, Range 0.0–4.0
Pydantic Schemas

Implemented schemas:

StudentCreate
StudentUpdate
StudentPatch
StudentResponse
CRUD Endpoints

Implemented all required endpoints:

Method	Endpoint	DescriptionPOST	/students	Create a student
GET	/students	List students with filters
GET	/students/{id}	Retrieve one student
PUT	/students/{id}	Full replacement update
PATCH	/students/{id}	Partial update
DELETE	/students/{id}	Delete student
Additional Requirements

✅ Duplicate email handling (409 Conflict)

✅ Filtering by major

✅ Filtering by minimum GPA

✅ 404 handling for missing students

✅ PATCH implementation using:

model_dump(exclude_unset=True)


✅ Delete endpoint returning a success message dictionary

✅ Complete CRUD cycle tested in Swagger UI

Technologies Used
Python 3.x
FastAPI
SQLAlchemy 2.0
SQLite
Pydantic v2
Uvicorn
Swagger UI/OpenAPI
Project Structure
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
│   └── schemas/
│       ├── studentcreate.py
│       ├── studentupdate.py
│       ├── studentpatch.py
│       └── studentresponse.py
│
├── main.py
├── requirements.txt
└── students.db

Installation
Clone the repository
git clone <repository-url>
cd student-api

Create a virtual environment

Windows:

python -m venv .venv


Activate:

.venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Running the Application

Start the FastAPI server:

uvicorn main:app --reload


Server:

http://127.0.0.1:8000


Swagger UI:

http://127.0.0.1:8000/docs


ReDoc Documentation:

http://127.0.0.1:8000/redoc

Database Design

The application uses SQLite for persistent storage.

Student Table
students

Column	Type	Constraintsid	Integer	Primary Key
name	String(75)	Required
email	String(100)	Unique, Required
major	String(50)	Optional
gpa	Float	Optional
gpa_range	CheckConstraint	0.0 ≤ GPA ≤ 4.0

The GPA range is enforced at both:

Pydantic validation layer
Database constraint layer

This provides defense-in-depth validation.

API Endpoints
Create Student

POST /students

Request:

{
  "name": "John Doe",
  "email": "john@example.com",
  "major": "Computer Science",
  "gpa": 3.8
}


Success:

201 Created


Duplicate email:

409 Conflict


Response:

{
  "detail": "A student with this email already exists."
}

List Students

GET /students

Returns all students.

Example:

GET /students

Filter By Major
GET /students?major=Computer Science

Filter By Minimum GPA
GET /students?min_gpa=3.5

Combined Filters
GET /students?major=Computer Science&min_gpa=3.5

Retrieve Student

GET /students/{id}

Example:

GET /students/1


Success:

200 OK


Missing student:

404 Not Found


Response:

{
  "detail": "Student not found."
}

Full Update

PUT /students/{id}

Example:

{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "major": "Mathematics",
  "gpa": 3.7
}


Success:

200 OK


Possible errors:

404 Not Found

409 Conflict

Partial Update

PATCH /students/{id}

Example:

{
  "gpa": 3.9
}


Only supplied fields are updated.

Implementation uses:

model_dump(exclude_unset=True)


to preserve existing values for omitted fields.

Delete Student

DELETE /students/{id}

Success:

{
  "message": "Student deleted successfully",
  "id": 1
}


Missing student:

{
  "detail": "Student not found."
}

Validation and Error Handling
HTTP Status Codes
Code	Meaning200	Successful Request
201	Student Created
404	Student Not Found
409	Duplicate Email
422	Validation Error
Validation Rules

Name:

1-75 characters


Email:

Required
Unique
3-100 characters


Major:

Optional
Maximum 50 characters


GPA:

0.0 - 4.0

Testing

All endpoints were tested using FastAPI Swagger UI.

CRUD workflow tested:

Create student
Retrieve student
List students
Filter students
Update student using PUT
Update student using PATCH
Delete student
Verify deletion
Verify error handling
Key Design Decisions
SQLAlchemy 2.0 Typed ORM

The Student model uses modern SQLAlchemy 2.0 typing:

Mapped[str]
mapped_column()


for improved readability and maintainability.

Schema Separation

Separate schemas were created for:

Create operations
Full updates
Partial updates
Responses

This ensures each operation receives only the fields it requires.

Duplicate Email Protection

Email uniqueness is validated before database operations:

409 Conflict


is returned instead of allowing a database exception to occur.

PATCH Support

PATCH requests update only supplied fields, preserving existing values and aligning with REST semantics.

Author

Grant Eberhardt

Student CRUD API Assignment

Built with FastAPI, SQLAlchemy 2.0, Pydantic v2, and SQLite.
