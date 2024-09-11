from datetime import datetime
from random import randint

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from repository.cards import RepositoryCards
from repository.favorite_cards import RepositoryFavoriteCards
from repository.solve_card import RepositorySolveCards
from repository.users import RepositoryUsers
from schemas.card_schema import CardSchema
from schemas.solved_card_schema import SolveCardSchema
from schemas.users_schema import UserSchema
from utils.config import url
from models.models import AbstractModel
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from schemas.favorite_card import FavoriteCardSchema

config_engine = create_engine(url)
AbstractModel.metadata.drop_all(config_engine)
AbstractModel.metadata.create_all(config_engine)


@pytest.fixture(autouse=True, scope='function')
def db_engine():
    connection = config_engine.connect()
    transaction = connection.begin()
    yield config_engine  # db engine to the test session
    print("AAAAA")
    transaction.rollback()
    connection.close()


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
        session_local.execute(table.delete())
        session_local.commit()
    session_local.close()


@pytest.fixture(scope='session')
def client():
    with TestClient(app) as c:
        yield c


user_id = randint(10 ** 8, 10 ** 9)


@pytest.fixture(scope="function")
def add_active_user(db_session):
    repository_users = RepositoryUsers(session=db_session)
    user = {
        "id": user_id,
        "username": "alc",
        "email": "test@gmail.com",
        "full_name": "alsa",
        "disabled": False,
        "hashed_password": "secret"
    }
    repository_users.create_user(UserSchema(**user))
    return UserSchema(**user)


@pytest.fixture(scope="function")
def add_card(db_session, add_active_user):
    card = {
        "id": 0,
        "name": "PublicCard",
        "problem": "string",
        "answer": "string",
        "category": "string",
        "user_fk": user_id,
        "is_private": False
    }
    repository_cards = RepositoryCards(session=db_session)
    repository_cards.add_card(CardSchema(**card))
    return CardSchema(**card)


@pytest.fixture(scope="function")
def add_solve(db_session, add_active_user, add_card, ):
    solve = {
        "id": 0,
        "card_fk": add_card.id,
        "user_fk": add_active_user.id,
        "grade": "bad"
    }
    repository_cards = RepositorySolveCards(session=db_session)
    repository_cards.add_solve_card(SolveCardSchema(**solve))
    return SolveCardSchema(**solve)


@pytest.fixture(scope="function")
def add_favorite_card(db_session, add_active_user, add_card):
    fav_card = {
        "id": 0,
        "card_fk": add_card.id,
        "user_fk": add_active_user.id,
        "created": str(datetime.now())
    }
    fav_card_schema = FavoriteCardSchema(**fav_card)
    repository_fav_cards = RepositoryFavoriteCards(session=db_session)
    repository_fav_cards.add_favorite_card(fav_card_schema)
    return fav_card_schema


@pytest.fixture(scope="function")
def auth(db_session, add_active_user):
    return {
        "Authorization": f"Bearer {add_active_user.username}"
    }
