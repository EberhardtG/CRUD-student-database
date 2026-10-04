"""
WHY
----
This testing setup isolates the application from its real database and middleware
so tests run deterministically. A dedicated SQLite test database ensures each test
starts with a clean state, and overriding `get_db` guarantees all ORM operations
use that isolated environment. Rate‑limiting middleware is removed because it
interferes with automated tests (TestClient always uses the same IP), causing
429 responses unrelated to CRUD behavior.

DESIGN
------
1. In‑memory SQLite engine (StaticPool)
   - Fast, isolated, and shared across connections during tests.

2. Dependency override for get_db
   - Forces all endpoints to use the test database session.

3. Middleware removal
   - Prevents rate‑limiting from affecting test outcomes.

4. TestClient fixture
   - Creates tables before each test and drops them afterward for full isolation.
"""




import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from sqlalchemy.pool import StaticPool

# this creates a new database engine for testing, using an in-memory SQLite database
TEST_DATABASE_URL = "sqlite:///./test_students.db"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# override the get_db dependency to use the testing database session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
# Disable rate limiting for tests
# Completely disable rate limiting during tests
app.user_middleware = []
app.middleware_stack = None
app.build_middleware_stack()



# this fixture provides a TestClient instance for testing the FastAPI app
@pytest.fixture
def client():
    # create the database tables before running tests
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as c:
        yield c

    # drop the database tables after tests are done
    Base.metadata.drop_all(bind=engine)
