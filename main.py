"""
WHY:
The main module serves as the entry point for the Student API. It initializes
the FastAPI application, creates database tables, registers API routes, and
configures centralized exception handling. Keeping these responsibilities in
one location ensures the application starts consistently and remains easy to
maintain.

DESIGN:
1. The FastAPI app is configured with a title, description, and version to
   provide clear API documentation through Swagger UI.

2. Base.metadata.create_all(bind=engine) automatically creates all database
   tables at startup, ensuring the Student model is available for CRUD
   operations.

3. The Student model is imported so SQLAlchemy recognizes the model definition
   during table creation.

4. The student router is registered using app.include_router(), keeping route
   definitions separate from application startup logic.

5. Custom exception handlers are registered using
   app.add_exception_handler() to provide consistent API error responses.

6. Request validation errors are formatted into a simplified JSON structure
   that clearly identifies invalid fields and messages.


"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.database import Base, engine
from app.models.student import Student
from app.routers.crud_endpoints import router as student_router
from app.exceptions import AppException

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student API",
    description="A complete CRUD API for managing student records.",
    version="1.0.0",
)


async def app_exception_handler(
    request: Request,
    exc: AppException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "detail": exc.detail
        }
    )


async def validation_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = [
        {
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"]
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "detail": "Validation failed",
            "errors": errors
        }
    )


# Register exception handlers
app.add_exception_handler(
    AppException,
    app_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_handler
)

# Include routers
app.include_router(student_router)
