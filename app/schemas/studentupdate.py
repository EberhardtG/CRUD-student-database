from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from typing import Optional


class StudentUpdate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=75
    )

    email: EmailStr

    major: Optional[str] = Field(
        default=None,
        max_length=50
    )

    gpa: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=4.0
    )