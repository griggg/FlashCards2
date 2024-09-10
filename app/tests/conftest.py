import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from utils.config import config_engine
from models.models import AbstractModel
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import sessionmaker

@pytest.fixture(autouse=True, scope='session')
def db_engine():
    AbstractModel.metadata.drop_all(config_engine)
    AbstractModel.metadata.create_all(config_engine)

    yield config_engine  # db engine to the test session

    AbstractModel.metadata.drop_all(config_engine)


@pytest.fixture(autouse=True, scope='function')
def db_session(db_engine):
    session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine,
        expire_on_commit=False,
    )()

    yield session_local  # every test will get a new db session

    session_local.rollback()  # rollback the transactions
    # truncate all tables
    for table in reversed(AbstractModel.metadata.sorted_tables):
        session_local.execute(text(f'TRUNCATE {table.name} CASCADE;'))
        session_local.commit()
    session_local.close()


@pytest.fixture(scope='session')
def client():
    with TestClient(app) as c:
        yield c
