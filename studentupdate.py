"""
WHY:
The StudentUpdate schema supports full replacement updates for student records.
It is used by the PUT /students/{id} endpoint, where clients must provide a
complete student object. This ensures that updates remain predictable and
consistent with REST semantics.

DESIGN:
1. The name field is required and capped at 75 characters, matching the database
   constraint and ensuring that full updates always include a valid student name.

2. The email field is required and capped at 100 characters, ensuring that full
   updates always include a valid email before checking for uniqueness in the
   database.

3. The major field is optional and capped at 50 characters, allowing students to
   be updated without requiring a declared major.

4. The gpa field is optional but validated to fall within the 0.0–4.0 range,
   ensuring that full updates cannot introduce invalid academic values.

Overall, this schema guarantees that PUT requests provide complete, validated,
and database‑aligned student data, while remaining fully compatible with the
Student model and StudentResponse schema.
"""



from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime



class StudentUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=75)
    email: str = Field(min_length=3, max_length=100)
    major: Optional[str] = Field(default=None, max_length=50)
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)
