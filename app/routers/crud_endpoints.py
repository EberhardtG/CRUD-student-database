from fastapi import (
    APIRouter,
    Depends,
    BackgroundTasks,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.schemas.studentcreate import StudentCreate
from app.schemas.studentupdate import StudentUpdate
from app.schemas.studentpatch import StudentPatch
from app.schemas.studentresponse import StudentResponse
from app.exceptions import NotFoundError, DuplicateError

from app.utils.notifications import (
    log_activity,
    send_notification,
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# ---------------------------------------------------------
# Helper Function
# ---------------------------------------------------------
def get_student_or_404(
    student_id: int,
    db: Session
) -> Student:

    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        raise NotFoundError(
            "Student not found."
        )

    return student


# ---------------------------------------------------------
# POST /students
# Create Student
# ---------------------------------------------------------
@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    existing = (
        db.query(Student)
        .filter(Student.email == student.email)
        .first()
    )

    if existing:
        raise DuplicateError(
            "A student with this email already exists."
        )

    db_student = Student(
        **student.model_dump()
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    # Background Tasks
    background_tasks.add_task(
        log_activity,
        f"Student created: {db_student.name}"
    )

    background_tasks.add_task(
        send_notification,
        f"Welcome {db_student.name}"
    )

    return db_student


# ---------------------------------------------------------
# GET /students
# List Students with Filters
# ---------------------------------------------------------
@router.get(
    "",
    response_model=list[StudentResponse]
)
def list_students(
    major: str | None = None,
    min_gpa: float | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Student)

    if major is not None:
        query = query.filter(
            Student.major == major
        )

    if min_gpa is not None:
        query = query.filter(
            Student.gpa >= min_gpa
        )

    return (
        query
        .order_by(Student.id.asc())
        .all()
    )


# ---------------------------------------------------------
# GET /students/{id}
# Retrieve One Student
# ---------------------------------------------------------
@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    return get_student_or_404(
        student_id,
        db
    )


# ---------------------------------------------------------
# PUT /students/{id}
# Full Replacement
# ---------------------------------------------------------
@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    update: StudentUpdate,
    db: Session = Depends(get_db)
):

    student = get_student_or_404(
        student_id,
        db
    )

    existing = (
        db.query(Student)
        .filter(Student.email == update.email)
        .first()
    )

    if existing and existing.id != student.id:
        raise DuplicateError(
            "A student with this email already exists."
        )

    for field, value in update.model_dump().items():
        setattr(
            student,
            field,
            value
        )

    db.commit()
    db.refresh(student)

    return student


# ---------------------------------------------------------
# PATCH /students/{id}
# Partial Update
# ---------------------------------------------------------
@router.patch(
    "/{student_id}",
    response_model=StudentResponse
)
def patch_student(
    student_id: int,
    patch: StudentPatch,
    db: Session = Depends(get_db)
):

    student = get_student_or_404(
        student_id,
        db
    )

    patch_data = patch.model_dump(
        exclude_unset=True
    )

    if "email" in patch_data:

        existing = (
            db.query(Student)
            .filter(
                Student.email == patch_data["email"]
            )
            .first()
        )

        if (
            existing
            and existing.id != student.id
        ):
            raise DuplicateError(
                "A student with this email already exists."
            )

    for field, value in patch_data.items():
        setattr(
            student,
            field,
            value
        )

    db.commit()
    db.refresh(student)

    return student


# ---------------------------------------------------------
# DELETE /students/{id}
# Delete Student
# ---------------------------------------------------------
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    student = get_student_or_404(
        student_id,
        db
    )

    background_tasks.add_task(
        log_activity,
        f"Student deleted: {student.name}"
    )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully",
        "id": student_id
    }