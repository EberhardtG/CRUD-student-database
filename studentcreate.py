"""
WHY:
The StudentCreate schema defines the validated structure for creating new
student records. It ensures all incoming data is clean, safe, and properly
constrained before reaching the database. Because user‑supplied text fields
can contain unwanted whitespace or even malicious HTML/JavaScript, the schema
includes a sanitization validator to prevent stored XSS attacks and guarantee
consistent formatting across all student inputs.

DESIGN:
1. Field() constraints enforce strict validation rules:
   - username must be 1–75 characters
   - email must be 3–100 characters
   - major is optional but limited to 50 characters
   - gpa must fall within the academic range 0.0–4.0

2. A @field_validator on the username and major fields strips leading/trailing
   whitespace and removes HTML tags using a simple regex. This prevents users
   from injecting <script> tags or other markup that could lead to stored XSS
   if displayed by a frontend client.

3. Sanitization occurs before any database interaction, ensuring that all
   downstream components—routers, models, and database operations—receive
   clean, normalized data without needing to implement their own filtering.

4. By centralizing validation and sanitization inside the schema, the router
   logic remains simple and focused on business rules (such as duplicate email
   checks), while the schema guarantees that all incoming student data meets
   both structural and security requirements.

Together, these design choices create a robust, secure, and maintainable input
layer that protects the API from malformed or malicious data while keeping the
StudentCreate schema easy to understand and extend.
"""




from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class StudentCreate(BaseModel):
    username: str = Field(min_length=1, max_length=75)
    email: str = Field(min_length=3, max_length=100)
   
    major:Optional[str] =Field(default=None, max_length=50)
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)


    @field_validator("username", "major")
    def sanitize(cls, value: str) -> str:
        if value is None:
            return value
        # Remove HTML tags
        value = re.sub(r"<.*?>", "", value)
        # Strip whitespace
        return value.strip()
