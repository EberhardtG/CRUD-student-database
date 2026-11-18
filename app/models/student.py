from __future__ import annotations

from sqlalchemy import (
    String,
    Integer,
    Float,
    CheckConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(75),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    major: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    gpa: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    # Required for authentication
    hashed_password: Mapped[str | None] = mapped_column(
    String(255),
    nullable=True
)

    __table_args__ = (
        CheckConstraint(
            "gpa >= 0.0 AND gpa <= 4.0",
            name="gpa_range"
        ),
    )