"""
WHY:
The StudentUpdate schema supports full replacement updates for student records.
It is used by the PUT /students/{id} endpoint, where clients must provide a
complete student object. This ensures that updates remain predictable and
consistent with REST semantics, since PUT always replaces the entire resource.

DESIGN:
1. The username field is required and capped at 75 characters, matching the
   database constraint and ensuring that full updates always include a valid
   username.

2. The email field is required and capped at 100 characters, ensuring that full
   updates always include a valid email before the router performs its duplicate
   email check. This keeps validation responsibilities cleanly separated.

3. The major field is optional and capped at 50 characters, allowing students to
   be updated without requiring a declared major while still enforcing the same
   length constraints as the SQLAlchemy model.

4. The gpa field is optional but validated to fall within the 0.0–4.0 academic
   range, ensuring that full updates cannot introduce invalid GPA values.

Together, these design choices create a strict, predictable, and fully aligned
schema for full‑record updates, ensuring that PUT operations remain consistent
with both REST semantics and the underlying Student model.
"""



from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime



class StudentUpdate(BaseModel):
    username: str = Field(min_length=1, max_length=75)
    email: str = Field(min_length=3, max_length=100)
    major: Optional[str] = Field(default=None, max_length=50)
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)
