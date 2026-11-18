from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)

import os




# ---------------------------------------------------------
# TOKEN RESPONSE
# ---------------------------------------------------------
class TokenResponse(BaseModel):
    access_token: str = Field(
        ...,
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"]
    )

    token_type: str = Field(
        default="bearer",
        examples=["bearer"]
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token":
                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )


# ---------------------------------------------------------
# TOKEN DATA
# ---------------------------------------------------------
class TokenData(BaseModel):
    user_id: str | None = None


# ---------------------------------------------------------
# LOGIN REQUEST
# ---------------------------------------------------------
class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        examples=["student@example.com"]
    )

    password: str = Field(
        ...,
        min_length=1,
        examples=["secret123"]
    )


# ---------------------------------------------------------
# USER CREATE
# ---------------------------------------------------------
class UserCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=75,
        examples=["Grant Eberhardt"]
    )

    email: EmailStr = Field(
        ...,
        examples=["grant@example.com"]
    )

    password: str = Field(
        ...,
        min_length=6,
        examples=["secret123"]
    )


# ---------------------------------------------------------
# USER RESPONSE
# ---------------------------------------------------------
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Grant Eberhardt",
                "email": "grant@example.com"
            }
        }
    )