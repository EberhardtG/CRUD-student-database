import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


# ---------------------------------------------------------
# Test Database Configuration
# ---------------------------------------------------------
TEST_DATABASE_URL = "sqlite:///./test_students.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ---------------------------------------------------------
# Override Database Dependency
# ---------------------------------------------------------
def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ---------------------------------------------------------
# Disable Rate Limiting During Tests
# ---------------------------------------------------------
app.user_middleware.clear()
app.middleware_stack = None
app.build_middleware_stack()


# ---------------------------------------------------------
# Test Client Fixture
# ---------------------------------------------------------
@pytest.fixture
def client():

    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)