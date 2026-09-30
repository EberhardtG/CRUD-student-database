"""
WHY:
The Student model defines the database representation of student records in the
API. It provides a typed, SQLAlchemy 2.0‑compliant structure that integrates
cleanly with Pydantic v2 through from_attributes=True. By centralizing all
database constraints—required fields, uniqueness rules, optional fields, and GPA
range validation—the model ensures that every student stored in the system is
consistent, valid, and aligned with the assignment requirements.

DESIGN:
1. The model inherits from DeclarativeBase, enabling SQLAlchemy 2.0’s typed ORM
   features. This ensures strong typing, cleaner model definitions, and seamless
   compatibility with Pydantic response schemas.

2. The id field is an integer primary key, guaranteeing that each student can be
   uniquely identified. SQLAlchemy automatically indexes primary keys, providing
   efficient lookup performance for GET, PUT, PATCH, and DELETE operations.

3. The name field is required and capped at 75 characters, matching the database
   constraint and preventing overly long names. This aligns with the validation
   rules in StudentCreate and StudentUpdate.

4. The email field is required, capped at 100 characters, and marked as unique.
   This enforces the assignment requirement that no two students may share the
   same email. The router performs a 409 Conflict check before insertion or
   update to maintain this constraint at the API layer.

5. The major field is optional and capped at 50 characters, allowing students to
   exist without a declared major while still enforcing a reasonable length
   limit. This matches the optional nature of the field in all Pydantic schemas.

6. The gpa field is optional and stored as a Float. A CheckConstraint enforces
   the valid academic range of 0.0–4.0, ensuring that invalid GPA values cannot
   be inserted or updated. This mirrors the validation rules in all Pydantic
   schemas and guarantees consistency between API and database layers.

Overall, this model provides a clean, typed, and fully validated foundation for
all student‑related operations. It ensures strong alignment between the database
schema, Pydantic models, and CRUD router, resulting in a reliable and maintainable
Student API.
"""


from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, CheckConstraint
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(75), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    major: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gpa: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (
        CheckConstraint("gpa >= 0.0 AND gpa <= 4.0", name="gpa_range"),
    )
