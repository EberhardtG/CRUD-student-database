from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student

from app.schemas.auth import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
)

from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


# ---------------------------------------------------------
# REGISTER
# ---------------------------------------------------------
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(Student)
        .filter(Student.email == user.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    new_student = Student(
        name=user.name,
        email=user.email,
        major=None,
        gpa=None,
        hashed_password=hash_password(
            user.password
        ),
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# ---------------------------------------------------------
# TOKEN (LOGIN)
# ---------------------------------------------------------
@router.post(
    "/token",
    response_model=TokenResponse,
)
def login_for_access_token(
    login: LoginRequest,
    db: Session = Depends(get_db),
):
    student = (
        db.query(Student)
        .filter(Student.email == login.email)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not verify_password(
        login.password,
        student.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        data={"sub": str(student.id)}
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


# ---------------------------------------------------------
# CURRENT USER PROFILE
# ---------------------------------------------------------
@router.get(
    "/me",
    response_model=UserResponse,
)
def read_current_user(
    current_user: Student = Depends(
        get_current_user
    ),
):
    return current_user


# ---------------------------------------------------------
# PROTECTED DASHBOARD
# ---------------------------------------------------------
@router.get("/dashboard")
def dashboard(
    current_user: Student = Depends(
        get_current_user
    ),
):
    return {
        "message": (
            f"Welcome to your dashboard, "
            f"{current_user.name}!"
        ),
        "user_id": current_user.id,
    }