from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator,
)
from typing import Optional
import re


class StudentCreate(BaseModel):
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

    @field_validator(
        "name",
        "major",
        mode="before"
    )
    @classmethod
    def sanitize(cls, value):
        if value is None:
            return value

        value = re.sub(
            r"<.*?>",
            "",
            value
        )

        return value.strip()