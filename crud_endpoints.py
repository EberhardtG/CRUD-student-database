"""
WHY:
This router implements all student‑related CRUD functionality for the API,
providing validated, database‑backed operations while integrating the security
and data‑sanitization requirements defined in the assignment. Input validation
occurs in the Pydantic schemas, SQL‑injection awareness is demonstrated through
clear examples, and custom exceptions ensure consistent error formatting.
Global rate‑limit enforcement (implemented in main.py) applies automatically to
all endpoints, keeping the student subsystem predictable, safe, and easy to
maintain.

DESIGN:
1. The StudentCreate schema sanitizes user input through field validators that
   strip whitespace and remove HTML tags. This prevents stored XSS attacks and
   ensures all incoming data is clean before reaching the database layer.

2. The POST /students endpoint creates new student records using sanitized
   input and enforces email uniqueness by raising DuplicateError when a
   conflict is detected. The ORM model is populated using model_dump(), ensuring
   only validated fields are passed to SQLAlchemy.

3. The GET /students endpoint supports filtering by major and minimum GPA.
   It includes an instructional comment demonstrating how parameterized queries
   prevent SQL injection, contrasting a vulnerable string‑formatted query with
   a safe parameterized version. SQLAlchemy’s ORM automatically parameterizes
   queries, ensuring safe execution.

4. The GET /students/{id} endpoint retrieves a single student record and raises
   NotFoundError when the requested student does not exist. This provides
   consistent, structured error responses across the API.

5. The PUT /students/{id} endpoint performs full replacement updates using the
   StudentUpdate schema. It validates email uniqueness when the email changes
   and updates all fields atomically using model_dump().

6. The PATCH /students/{id} endpoint supports partial updates using
   model_dump(exclude_unset=True), ensuring only provided fields are modified.
   Email uniqueness is checked only when the email field is included in the
   patch payload.

7. The DELETE /students/{id} endpoint removes a student record and returns a
   simple confirmation message. NotFoundError is raised if the student does not
   exist, maintaining consistent error behavior.

8. All endpoints automatically participate in the global rate‑limiting
   middleware defined in main.py. Clients exceeding 10 requests per minute
   receive a 429 Too Many Requests response, ensuring fair usage and preventing
   abuse without requiring per‑endpoint decorators.

Together, these design choices create a secure, modular, and fully compliant
student management router that satisfies all assignment requirements while
remaining clean, predictable, and easy to extend.
"""




import datetime
from turtle import back

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.student import Student
from app.schemas.studentcreate import StudentCreate
from app.schemas.studentupdate import StudentUpdate
from app.schemas.studentpatch import StudentPatch
from app.schemas.studentresponse import StudentResponse
from app.exceptions import AppException, NotFoundError,DuplicateError,AppValidationError
from app.routers.reports import generate_report, reports, send_notification, notification_log, ReportRequest

router = APIRouter(prefix="/students", tags=["Students"])


# ---------------------------------------------------------
# POST /students — Create student (with duplicate email check)
# ---------------------------------------------------------
@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
     # student.username and student.major are already sanitized by field_validator
    # Duplicate email check
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise DuplicateError(
           "A student with this email already exists."
        )

    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# ---------------------------------------------------------
# GET /students — List students with major + min_gpa filters
# ---------------------------------------------------------
@router.get("", response_model=list[StudentResponse])
def list_students(
    major: str | None = None,
    min_gpa: float | None = None,
    db: Session = Depends(get_db),
):
    """
    WHY PARAMETERIZED QUERIES PREVENT SQL INJECTION:

    ❌ Vulnerable example (DO NOT USE):
        db.execute(f"SELECT * FROM students WHERE major = '{major}'")

    If major = "'; DROP TABLE students; --"
    the attacker can inject SQL.

    ✔ Safe example (parameterized):
        db.execute(text("SELECT * FROM students WHERE major = :major"), {"major": major})

    SQLAlchemy automatically escapes dangerous characters, preventing attackers
    from injecting additional SQL commands.
    """

    query = db.query(Student)

    if major is not None:
        query = query.filter(Student.major == major)

    if min_gpa is not None:
        query = query.filter(Student.gpa >= min_gpa)

    return query.order_by(Student.id.asc()).all()


# ---------------------------------------------------------
# GET /students/{id} — Retrieve student with 404 handling
# ---------------------------------------------------------
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise NotFoundError(
            "Student not found."
        )
    return student


# ---------------------------------------------------------
# PUT /students/{id} — Full replacement update
# ---------------------------------------------------------
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, update: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
       raise NotFoundError(
        "Student not found."
    )

    # Duplicate email check (only if changed)
    if update.email != student.email:
        existing = db.query(Student).filter(Student.email == update.email).first()
        if existing:
            raise DuplicateError(
            "A student with this email already exists."
)

    for field, value in update.model_dump().items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return student


# ---------------------------------------------------------
# PATCH /students/{id} — Partial update
# ---------------------------------------------------------
@router.patch("/{student_id}", response_model=StudentResponse)
def patch_student(student_id: int, patch: StudentPatch, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
           raise NotFoundError(
            "Student not found."
        )

    patch_data = patch.model_dump(exclude_unset=True)

    # Duplicate email check (only if email is being patched)
    if "email" in patch_data:
        existing = db.query(Student).filter(Student.email == patch_data["email"]).first()
        if existing:
            raise DuplicateError(
                "A student with this email already exists."
        )

    for field, value in patch_data.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return student


# ---------------------------------------------------------
# DELETE /students/{id} — Returns success message dict
# ---------------------------------------------------------
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
           raise NotFoundError(
            "Student not found."
        )

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully", "id": student_id}


