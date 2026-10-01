"""
WHY:
The auth router provides all authentication-related endpoints for the Student
API, including registration, login, and protected user access. By separating
authentication logic into its own router, the application maintains a clear
boundary between security concerns and business functionality. This modular
structure ensures that password hashing, token generation, and user validation
are handled consistently across the entire API. The router works together with
auth.py to enforce secure access control, allowing only authenticated users to
reach protected routes such as /me and /dashboard.

DESIGN:
1. The router is mounted under the /auth prefix, keeping all authentication
   endpoints grouped logically and making the API easier to navigate in Swagger
   UI. Tagging the router as "Auth" further improves documentation clarity.

2. POST /register accepts a UserCreate schema, hashes the incoming password,
   stores the new student in the database, and returns a safe UserResponse
   model. This ensures that sensitive fields like hashed_password are never
   exposed in API responses.

3. POST /token handles login using the LoginRequest schema. It verifies the
   provided credentials, generates a signed JWT containing the student's ID as
   the "sub" claim, and returns a TokenResponse. This token enables stateless
   authentication, allowing clients to authenticate without server-side session
   storage.

4. GET /me is protected using the get_current_user dependency. The dependency
   extracts the JWT from the Authorization header, validates it, decodes the
   "sub" claim, and retrieves the corresponding student from the database. This
   provides a reliable way to identify the currently authenticated user.

5. GET /dashboard serves as the required additional protected endpoint. It
   demonstrates how any route can be secured simply by depending on
   get_current_user, ensuring that only authenticated users can access
   privileged information or functionality.

Overall, the auth router provides a clean, secure, and modular authentication
layer for the Student API. It follows FastAPI best practices, keeps sensitive
operations isolated, and ensures consistent behavior across all protected
endpoints.
"""



from fastapi import APIRouter, Depends, HTTPException, status
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

router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------------------------------------------------------
# REGISTER
# ---------------------------------------------------------

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing = db.query(Student).filter(Student.username == user.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Create new student
    new_student = Student(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# ---------------------------------------------------------
# TOKEN (LOGIN)
# ---------------------------------------------------------

@router.post("/token", response_model=TokenResponse)
def login_for_access_token(login: LoginRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.username == login.username).first()

    if not student or not verify_password(login.password, student.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # Use student.id as JWT subject
    access_token = create_access_token(data={"sub": str(student.id)})

    return TokenResponse(access_token=access_token, token_type="bearer")


# ---------------------------------------------------------
# CURRENT USER PROFILE
# ---------------------------------------------------------

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: Student = Depends(get_current_user)):
    return current_user


# ---------------------------------------------------------
# EXTRA PROTECTED ENDPOINT (REQUIRED BY ASSIGNMENT)
# ---------------------------------------------------------

@router.get("/dashboard")
def dashboard(current_user: Student = Depends(get_current_user)):
    return {
        "message": f"Welcome to your dashboard, {current_user.username}!",
        "user_id": current_user.id,
    }
