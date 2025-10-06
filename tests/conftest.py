import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.models import Base
from app.dependencies import get_db

from dotenv import load_dotenv  #
#from urllib.parse import quote_plus

load_dotenv()

def _compose_test_url() -> str:
    database_url = os.getenv("database_url", "")

    return database_url

TEST_DATABASE_URL = _compose_test_url()

# Create a dedicated engine/sessionmaker for tests
engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

@pytest.fixture(scope="function")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)

def _get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(setup_db):  # ensures tables exist prior to requests
    app.dependency_overrides[get_db] = _get_test_db
    c = TestClient(app)
    try:
        yield c
    finally:
        app.dependency_overrides.clear()

