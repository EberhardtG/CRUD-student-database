"""
WHY:
The Student router provides the complete CRUD interface for managing student
records in the API. It connects validated Pydantic schemas with the SQLAlchemy
Student model and ensures that all operations follow REST conventions, enforce
data integrity, and return predictable, well‑structured responses. Each endpoint
is designed to be explicit, safe, and easy to test through Swagger UI.

DESIGN:
1. The POST /students endpoint creates new student records using the
   StudentCreate schema. It includes a required duplicate‑email check, returning
   a 409 Conflict when an email already exists. This prevents accidental
   duplication and enforces the unique constraint at the API layer before the
   database rejects the insert.

2. The GET /students endpoint supports optional filtering by major and minimum
   GPA. These filters allow clients to retrieve targeted subsets of students
   without needing additional endpoints. The query is built incrementally,
   ensuring that filters are applied only when provided.

3. The GET /students/{id} endpoint retrieves a single student by primary key.
   It returns a clear 404 Not Found when the student does not exist, ensuring
   predictable lookup behavior and preventing ambiguous responses.

4. The PUT /students/{id} endpoint performs a full replacement update using the
   StudentUpdate schema. Required fields (name and email) must always be present.
   The endpoint also checks for duplicate emails when the email is changed,
   returning a 409 Conflict when necessary. All fields are overwritten to match
   REST semantics for PUT.

5. The PATCH /students/{id} endpoint supports partial updates using the
   StudentPatch schema. Only fields explicitly provided by the client are
   updated, using model_dump(exclude_unset=True) to avoid overwriting existing
   values. A duplicate‑email check is performed only when the email field is
   included in the patch. This design ensures flexible updates while preserving
   data integrity.

6. The DELETE /students/{id} endpoint removes a student record and returns a
   success message dictionary instead of an empty response. This provides clear
   feedback to clients and aligns with the assignment requirement for a
   descriptive deletion response.

Overall, this router provides a complete, validated, and database‑backed CRUD
interface for student management. It demonstrates proper FastAPI patterns,
strong schema integration, SQLAlchemy 2.0 typed‑ORM usage, and reliable error
handling across all endpoints.
"""




from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.schemas.studentcreate import StudentCreate
from app.schemas.studentupdate import StudentUpdate
from app.schemas.studentpatch import StudentPatch
from app.schemas.studentresponse import StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])


# ---------------------------------------------------------
# POST /students — Create student (with duplicate email check)
# ---------------------------------------------------------
@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Duplicate email check
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists."
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )
    return student


# ---------------------------------------------------------
# PUT /students/{id} — Full replacement update
# ---------------------------------------------------------
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, update: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )

    # Duplicate email check (only if changed)
    if update.email != student.email:
        existing = db.query(Student).filter(Student.email == update.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A student with this email already exists."
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )

    patch_data = patch.model_dump(exclude_unset=True)

    # Duplicate email check (only if email is being patched)
    if "email" in patch_data:
        existing = db.query(Student).filter(Student.email == patch_data["email"]).first()
        if existing and existing.id != student.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A student with this email already exists."
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully", "id": student_id}
