"""
WHY:
The database module provides the foundational infrastructure required for all
SQLAlchemy operations in the Student API. It centralizes the engine, session
factory, and declarative base so that every model and router in the application
shares a consistent and reliable database connection. Separating these concerns
keeps the project organized, prevents circular imports, and ensures that the
database layer remains easy to maintain and extend.

DESIGN:
1. The DATABASE_URL is defined once and used to create a SQLAlchemy engine.
   SQLite requires the check_same_thread=False setting so that FastAPI can
   safely open sessions across multiple requests.

2. The engine is created at module load time and reused throughout the
   application. This ensures efficient connection handling and avoids the
   overhead of repeatedly constructing new engines.

3. SessionLocal is a session factory configured with autocommit=False and
   autoflush=False. This gives the API full control over when changes are
   committed and prevents unintended writes during request handling.

4. The DeclarativeBase subclass (Base) serves as the foundation for all ORM
   models. Every SQLAlchemy model inherits from Base, allowing the application
   to create tables and metadata consistently across the entire project.

5. The get_db dependency yields a database session for each request and ensures
   that the session is closed afterward. This pattern prevents connection leaks,
   keeps transactions isolated per request, and integrates cleanly with FastAPI’s
   dependency injection system.

Overall, this module provides a clean, minimal, and reliable database layer that
supports all CRUD operations in the Student API. It follows SQLAlchemy 2.0 best
practices and keeps the project’s architecture simple and maintainable.
"""




from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





