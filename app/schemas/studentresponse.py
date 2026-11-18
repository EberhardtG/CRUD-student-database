from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)
from typing import Optional


class StudentResponse(BaseModel):
    id: int

    name: str = Field(
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

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Grant",
                "email": "grant@example.com",
                "major": "Computer Science",
                "gpa": 3.8
            }
        }
    )