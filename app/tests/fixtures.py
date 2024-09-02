from app.utils.config import config_session_maker
from app.repository.cards import RepositoryCards
from app.schemas.card_schema import CardSchema
from pytest import fixture
from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.users_schema import UserSchema
from app.models.models import Card
from fastapi.testclient import TestClient
from random import randint
from app.main import app
from app.utils.crypto import decode_hash_password

fake_user_data = {
        "id": 222,
        "username": "alc",
        "email": "test@gmail.com",
        "full_name": "alsa",
        "disabled": True,
        "hashed_password": "fakehashed"+"secret"
}

fake_card_data = {
        "id": 7777,
        "name": "test_card_name",
        "problem": "2 + 2",
        "answer": "4",
        "category": "зачет по математике",
        "user_fk": fake_user_data["id"]
    }

@fixture()
def session() -> Session:
    return config_session_maker()


@fixture()
def create_fake_user(session: Session) -> dict:

    if not(session.query(User).where(User.id == fake_user_data["id"]).all()):
        fake_user = User(**fake_user_data)
        session.add(fake_user)
        session.commit()
    fake_user_data["hashed_password"] = decode_hash_password(fake_user_data["hashed_password"])
    return fake_user_data

@fixture()
def create_fake_card(session: Session, create_fake_user: dict) -> dict:
    fake_user_data = create_fake_user

    session.query(Card).where(Card.id==fake_card_data["id"]).delete()
    session.add(Card(**fake_card_data))
    session.commit()
    return fake_card_data


@fixture()
def auth_fake_user(create_fake_user: dict) -> dict:
    print(f"{create_fake_user=}")
    data = {
        "username": create_fake_user["username"],
        "password": create_fake_user["hashed_password"],
    }
    with TestClient(app) as client:
        response = client.post("/token", data=data)
    print(response.json())
    return response.json()