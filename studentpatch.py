"""
WHY:
The StudentPatch schema supports partial updates to student records. It allows
clients to modify only the fields they want without needing to resend the entire
student object. This aligns with the PATCH semantics required in the assignment.

DESIGN:
1. All fields are optional, allowing clients to update any combination of
   name, email, major, or gpa without providing the full record.

2. Length constraints for name, email, and major match the SQLAlchemy model,
   ensuring that partial updates remain consistent with database rules.

3. The gpa field includes validation for the 0.0–4.0 range, preventing invalid
   academic values even during partial updates.

4. When used with model_dump(exclude_unset=True), only fields explicitly
   provided by the client are included in the update dictionary, ensuring clean
   and predictable PATCH behavior.

Overall, this schema provides safe, flexible, and fully validated partial update
support for the Student API.
"""




from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class StudentPatch(BaseModel):
    name: str = Field(default=None, max_length=75)
    email: str = Field(default=None, max_length=100)
    major:Optional[str] =Field(default=None,max_length=50)
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)