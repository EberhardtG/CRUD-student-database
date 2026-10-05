"""
WHY:
auth.py handles password hashing, token creation, and user authentication for
the API. During development, bcrypt appeared installed but failed silently on
Windows due to native C‑extension issues. These failures caused 500 errors with
no traceback, making debugging nearly impossible. Switching to
pbkdf2_sha256 removes the native dependency and provides stable, secure hashing
across all platforms.

DESIGN:
1. Use pbkdf2_sha256 via Passlib for reliable, portable password hashing that
   avoids Windows bcrypt runtime failures.
2. Centralize hashing and verification in helper functions to keep credential
   logic consistent and testable.
3. Generate JWT access tokens with HS256 and embedded expiration for secure,
   short‑lived authentication.
4. Validate Bearer tokens in get_current_user and load the associated Student
   record, returning 401 for invalid or expired tokens.
5. Print the resolved file path at import time to confirm FastAPI is loading
   the correct module during development.

This keeps authentication stable, predictable, and secure across environments.
"""




from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Optional
import os
print("AUTH FILE LOADED FROM:", os.path.abspath(__file__))


SECRET_KEY="CHANGE_THIS_TO_SOMETHING_SAFE"
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES =30


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
http_bearer=HTTPBearer()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials= Security(http_bearer), db:Session= Depends(get_db)):
    token=credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str= payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token being used")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


    from app.models.student import Student
    student = db.query(Student).filter(Student.id == int(user_id)).first()
    if student is None:
        raise HTTPException(status_code=401, detail="user not found")
    return student