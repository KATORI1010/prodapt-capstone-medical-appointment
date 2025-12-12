import os
from models import Base
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from testcontainers.postgres import PostgresContainer
from fastapi.testclient import TestClient
from main import app, get_db
from ai import inmemory_vector_store, get_vector_store


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine", dbname="test_db") as container:
        yield container


# @pytest.fixture(scope="session")
# def db_engine(postgres_container):
#     db_url = postgres_container.get_connection_url()
#     engine = create_engine(db_url)
#     Base.metadata.create_all(engine)
#     yield engine


# @pytest.fixture(scope="session")
# def db_engine():
#     engine = create_engine(
#         url="sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
#     )
#     Base.metadata.create_all(engine)
#     yield engine


@pytest.fixture(scope="session")
def db_engine():
    db_url = "postgresql+psycopg2://postgres:Altohiro2019!@localhost:5432/postgres"
    engine = create_engine(str(db_url))
    yield engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()
    transaction = connection.begin()

    try:
        yield session
    finally:
        if transaction.is_active:
            transaction.rollback()
        session.close()
        connection.close()


@pytest.fixture(scope="function")
def vector_store():
    yield from inmemory_vector_store()


@pytest.fixture(scope="function")
def client(db_session, vector_store):
    def override_get_db():
        yield db_session

    def override_vector_store():
        yield vector_store

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_vector_store] = override_vector_store

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
