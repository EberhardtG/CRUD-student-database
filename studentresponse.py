"""
WHY
----
The StudentResponse schema defines the exact structure of student objects returned
by the API. It ensures all outbound data is clean, typed, and aligned with the
SQLAlchemy Student model. Using `from_attributes=True` allows Pydantic v2 to
serialize ORM instances automatically, eliminating manual conversions and keeping
response handling simple and predictable. The added `json_schema_extra` example
improves API documentation by giving clients a clear, realistic sample payload in
Swagger and ReDoc.

DESIGN
------
1. The id field reflects the database primary key, ensuring each returned student
   is uniquely identifiable.

2. The username and email fields enforce the same length constraints as the
   database model, guaranteeing consistency across create, update, and response
   schemas.

3. The major field is optional and capped at 50 characters, matching the database
   column definition and ensuring predictable formatting.

4. The gpa field is optional but validated to remain within the academic 0.0–4.0
   range, preventing invalid values from being returned.

5. The model_config uses `from_attributes=True` for seamless ORM → Pydantic
   serialization, and `json_schema_extra` provides a clear example object that
   enhances API documentation and improves client usability.

Together, these design choices produce a clean, typed, and documentation‑friendly
response model that ensures consistent, predictable output across all student
operations.
"""




from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class StudentResponse(BaseModel):
    id: int
    username: str = Field(max_length=75)
    email: str = Field(max_length=100)
    major: Optional[str] = Field(default=None, max_length=50)
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "Grant",
                "email": "grant@example.com",
                "major": "CS",
                "gpa": 3.8,
            }
        },
    ) 
