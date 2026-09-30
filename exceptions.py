"""
WHY:
The exceptions module centralizes application-specific errors used throughout
the Student API. By defining custom exceptions, the application can provide
consistent error messages and status codes while keeping router logic clean and
easy to maintain.

DESIGN:
1. AppException serves as a base class that stores a detail message and HTTP
   status code for all custom exceptions.

2. NotFoundError represents missing resources and is used when a requested
   record cannot be found.

3. DuplicateError represents unique-constraint violations, such as attempting
   to use an email address that already exists.

4. AppValidationError represents business-rule validation failures that occur
   beyond Pydantic schema validation.


"""


class AppException(Exception):
    """Base exception for application-specific errors."""

    def __init__(self, detail: str, status_code: int):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class NotFoundError(AppException):
    """Raised when a requested resource cannot be found."""

    def __init__(self, detail: str = "Resource not found."):
        super().__init__(
            detail=detail,
            status_code=404
        )


class DuplicateError(AppException):
    """Raised when a unique constraint is violated."""

    def __init__(self, detail: str = "Resource already exists."):
        super().__init__(
            detail=detail,
            status_code=409
        )


class AppValidationError(AppException):
    """Raised for business-rule validation errors."""

    def __init__(self, detail: str = "Validation failed."):
        super().__init__(
            detail=detail,
            status_code=422
        )