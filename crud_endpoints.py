"""
WHY:
The Student router provides the complete CRUD interface for managing student
records. It connects FastAPI routes, Pydantic schemas, and the SQLAlchemy
Student model to deliver validated, database-backed operations while ensuring
consistent error handling through custom application exceptions.

DESIGN:
1. The POST endpoint creates student records and prevents duplicate email
   addresses by raising DuplicateError when a conflict is detected.

2. The GET endpoints support student retrieval, filtering, and lookup by ID,
   raising NotFoundError when a requested student does not exist.

3. The PUT endpoint performs full replacement updates using the StudentUpdate
   schema and validates email uniqueness before applying changes.

4. The PATCH endpoint supports partial updates using
   model_dump(exclude_unset=True), ensuring that only supplied fields are
   modified.

5. The DELETE endpoint removes student records and returns a confirmation
   message upon successful deletion.

6. Custom exceptions replace direct HTTPException usage, allowing all error
   responses to be handled consistently through centralized exception handlers.


"""




from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.student import Student
from app.schemas.studentcreate import StudentCreate
from app.schemas.studentupdate import StudentUpdate
from app.schemas.studentpatch import StudentPatch
from app.schemas.studentresponse import StudentResponse
from app.exceptions import AppException, NotFoundError,DuplicateError,AppValidationError

router = APIRouter(prefix="/students", tags=["Students"])


# ---------------------------------------------------------
# POST /students — Create student (with duplicate email check)
# ---------------------------------------------------------
@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
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
