"""
WHY:
The StudentCreate schema validates all incoming data for creating new student
records. It ensures that required fields are present, optional fields follow
database constraints, and GPA values remain within the valid academic range.

DESIGN:
1. The name field is required and capped at 75 characters to match the database
   column definition and prevent overly long names.

2. The email field is required, capped at 100 characters, and validated with a
   minimum length to ensure meaningful input before checking for uniqueness in
   the database.

3. The major field is optional and capped at 50 characters, matching the
   database constraint and allowing students to exist without a declared major.

4. The gpa field is optional but validated to fall within the 0.0–4.0 range,
   ensuring realistic academic values and preventing invalid data from entering
   the database.

Overall, this schema provides strong validation, clean structure, and full
compatibility with the Student model and POST /students endpoint.
"""



from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=75)
    email: str = Field(min_length=3, max_length=100)
    major:Optional[str] =Field(max_length=50)
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)