from time import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.database import Base, engine
from app.exceptions import AppException
from app.routers.auth import router as auth_router
from app.routers.crud_endpoints import router as student_router
from app.routers.reports import router as reports_router


# ---------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# OpenAPI Tags
# ---------------------------------------------------------
tags_metadata = [
    {
        "name": "Students",
        "description": "Operations for creating, retrieving, updating, and deleting student records.",
    },
    {
        "name": "Auth",
        "description": "User registration, login, and protected endpoints.",
    },
    {
        "name": "Reports",
        "description": "Background report generation and notifications.",
    },
]


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------
app = FastAPI(
    title="Student Management API",
    description="""
A complete CRUD API for managing student records.

### Features

- Student CRUD Operations
- Email Validation
- Duplicate Email Protection
- JWT Authentication
- Background Reporting Tasks
- Custom Exception Handling
- Rate Limiting
- Automated Testing

### Quick Start

1. Start the API:

       uvicorn app.main:app --reload

2. Open Swagger UI:

       http://localhost:8000/docs

3. Test endpoints directly from Swagger.
""",
    version="1.0.0",
    openapi_tags=tags_metadata,
)


# ---------------------------------------------------------
# Exception Handlers
# ---------------------------------------------------------
async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "detail": exc.detail,
        },
    )


async def validation_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = [
        {
            "field": " -> ".join(
                str(loc)
                for loc in error["loc"]
            ),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "detail": "Validation failed",
            "errors": errors,
        },
    )


app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_handler,
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend-domain.com",
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    ],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# SlowAPI Rate Limiter
# ---------------------------------------------------------
limiter = Limiter(
    key_func=get_remote_address,
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)


# ---------------------------------------------------------
# Custom Rate Limiting Middleware
# ---------------------------------------------------------
RATE_LIMIT = 10
WINDOW = 60

request_counts = {}


@app.middleware("http")
async def rate_limit_middleware(
    request: Request,
    call_next,
):
    ip = request.client.host
    now = time()

    if ip not in request_counts:
        request_counts[ip] = []

    request_counts[ip] = [
        timestamp
        for timestamp in request_counts[ip]
        if now - timestamp < WINDOW
    ]

    if len(request_counts[ip]) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Too Many Requests"
            },
        )

    request_counts[ip].append(now)

    return await call_next(request)


# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------
app.include_router(student_router)

app.include_router(auth_router)

app.include_router(
    reports_router,
    prefix="/reports",
    tags=["Reports"],
)