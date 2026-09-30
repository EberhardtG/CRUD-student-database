"""
WHY:
The main application module initializes the FastAPI instance, sets up the
database tables, and registers the CRUD endpoints that power the Student API.
It serves as the entry point for the entire application, ensuring that the
database layer and routing layer are fully connected before any requests are
handled. By keeping main.py minimal and focused, the project remains easy to
navigate, test, and maintain.

DESIGN:
1. The FastAPI app is created with a title, description, and version to provide
   clear documentation in Swagger UI and help clients understand the purpose of
   the API.

2. Base.metadata.create_all(bind=engine) is executed at startup to ensure that
   all SQLAlchemy models—including the Student model—have their corresponding
   tables created in the SQLite database. This guarantees that CRUD operations
   will function correctly without requiring manual migrations.

3. The Student model is imported so SQLAlchemy is aware of its definition when
   generating tables. Without this import, the students table would not be
   created, even if the router is loaded.

4. The CRUD router is imported from app.routers.crud_endpoints and registered
   using app.include_router(). This modular design keeps routing logic separate
   from application startup logic, making the project easier to extend and
   preventing circular imports. All Student CRUD operations are defined inside
   the crud_endpoints module, and main.py simply attaches them to the FastAPI
   application.

Overall, this module provides a clean and minimal entry point for the Student
API, ensuring that the database, models, and CRUD endpoints are properly
initialized and ready for use.
"""





from fastapi import FastAPI

from app.database import Base, engine
from app.models.student import Student
from app.routers.crud_endpoints import router as student_router


# Create all database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student API",
    description="A complete CRUD API for managing student records.",
    version="1.0.0",
)


# Include routers
app.include_router(student_router)
