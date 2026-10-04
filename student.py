"""
WHY:
The Student model defines the database representation of student records in the
API. It uses SQLAlchemy 2.0’s typed ORM, providing a clean, strongly‑typed
structure that integrates directly with Pydantic v2 response models through
from_attributes=True. By centralizing all database constraints—required fields,
uniqueness rules, optional fields, and GPA range validation—the model ensures
that every student stored in the system is consistent, valid, and aligned with
the assignment requirements.

DESIGN:
1. The model inherits from DeclarativeBase, enabling SQLAlchemy 2.0’s typed ORM
   features. This provides strong typing, cleaner model definitions, and seamless
   compatibility with Pydantic schemas.

2. The id field is an integer primary key, guaranteeing that each student can be
   uniquely identified. SQLAlchemy automatically indexes primary keys, ensuring
   efficient lookup performance for GET, PUT, PATCH, and DELETE operations.

3. The username field is required, capped at 75 characters, and marked as unique.
   This ensures that each student has a distinct username and prevents duplicate
   entries. The length constraint aligns with the validation rules in the
   StudentCreate and StudentUpdate schemas.

4. The email field is required, capped at 100 characters, and marked as unique.
   This enforces the assignment requirement that no two students may share the
   same email. The router performs a duplicate‑email check before insertion or
   update, maintaining consistency between API‑level validation and database
   constraints.

5. The major field is optional and capped at 50 characters, allowing students to
   exist without a declared major while still enforcing a reasonable length
   limit. This matches the optional nature of the field in all Pydantic schemas.

6. The gpa field is optional and stored as a Float. A CheckConstraint enforces
   the valid academic range of 0.0–4.0, ensuring that invalid GPA values cannot
   be inserted or updated. This mirrors the validation rules in all Pydantic
   schemas and guarantees consistency between API and database layers.

Together, these design choices produce a clean, typed, and constraint‑driven
Student model that integrates smoothly with the rest of the application and
ensures reliable, validated data storage.
"""



from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, CheckConstraint
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(75), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    

    major: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gpa: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (
        CheckConstraint("gpa >= 0.0 AND gpa <= 4.0", name="gpa_range"),
    )

