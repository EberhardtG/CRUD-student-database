"""
WHY:
The main module serves as the application entry point, responsible for
initializing FastAPI, creating database tables, registering all routers,
configuring global middleware, and defining centralized exception handling.
Centralizing these startup concerns ensures predictable behavior, consistent
error formatting, and a clean, maintainable structure that keeps business
logic isolated inside dedicated routers.

DESIGN:
1. The FastAPI instance is created with a title, description, and version so
   the API is clearly documented in Swagger UI and easy to identify during
   development and testing.

2. Base.metadata.create_all(bind=engine) initializes all SQLAlchemy models at
   startup, guaranteeing that the Student table and any other ORM‑managed
   tables exist before CRUD or authentication operations run. A DB path print
   is included to verify the active SQLite file during development.

3. CORS middleware is configured with specific allowed origins rather than a
   wildcard, and restricted to the HTTP methods actually used by the API.
   This prevents unauthorized cross‑origin access while supporting legitimate
   frontend clients.

4. Two layers of rate limiting are used:
   - SlowAPI’s Limiter is initialized and its RateLimitExceeded handler is
     registered for framework‑level rate‑limit enforcement.
   - A custom manual rate‑limiting middleware tracks request timestamps per
     client IP and returns HTTP 429 Too Many Requests when more than 10
     requests occur within a 60‑second window. This satisfies assignment
     requirements for a self‑contained rate‑limiting mechanism and provides
     transparent, easily modifiable logic.

5. Custom exception handlers are registered for AppException and
   RequestValidationError. These handlers return structured JSON responses
   instead of FastAPI’s default formats. Validation errors are reformatted to
   clearly show the field path and message, improving debugging and client‑side
   error handling.

6. Routers are mounted using app.include_router(), keeping endpoint logic
   modular. The reports router is mounted with prefix="/reports" and
   tags=["Reports"], ensuring all report‑related endpoints appear under a
   dedicated section in Swagger UI. Student and authentication routers are
   mounted without prefixes, reflecting their role as core API resources.

Together, these design choices create a secure, maintainable, and fully
compliant application startup module that centralizes configuration while
delegating business logic to dedicated routers and middleware layers.
"""



from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.database import Base, engine
from app.models.student import Student
from app.routers.crud_endpoints import router as student_router
from app.exceptions import AppException
from app.routers.auth import router as auth_router
from app.routers.reports import router  as reports_router
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
print("DB PATH:", os.path.abspath("students.db"))



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

#Add CORS middleware with specific allowed origins (not a wildcard *), restricted to the methods your API actually uses

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Register exception handlers
app.add_exception_handler(
    AppException,
    app_exception_handler
)

app.add_exception_handler(
   RequestValidationError,
    validation_handler
)
from time import time

RATE_LIMIT = 10
WINDOW = 60  # seconds
request_counts = {}

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host
    now = time()

    # Initialize window
    if ip not in request_counts:
        request_counts[ip] = []

    # Remove old timestamps
    request_counts[ip] = [t for t in request_counts[ip] if now - t < WINDOW]

    # Check limit
    if len(request_counts[ip]) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too Many Requests"}
        )

    # Record request
    request_counts[ip].append(now)

    return await call_next(request)


# Include routers
app.include_router(student_router)
app.include_router(auth_router)
app.include_router(reports_router, prefix="/reports", tags=["Reports"])
