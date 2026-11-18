from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class StudentPatch(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=75
    )

    email: Optional[EmailStr] = None

    major: Optional[str] = Field(
        default=None,
        max_length=50
    )

    gpa: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=4.0
    )