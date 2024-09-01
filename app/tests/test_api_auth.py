from app.utils.config import config_session_maker
from app.repository.cards import RepositoryCards
from app.schemas.card_schema import CardSchema
from pytest import fixture
from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.users_schema import UserSchema
from app.models.models import Card
from fastapi.testclient import TestClient
from app.tests.fixtures import *
from app.main import app
from random import randint

class TestApiAuth:
    def test_create_account(self):

        user = {
            "id": randint(10**8, 10**9),
            "username": "alc",
            "email": "test@gmail.com",
            "full_name": "alsa",
            "disabled": True,
            "hashed_password": "secret"
        }
        with TestClient(app) as client:
            response = client.post("/users/create_account",json=user)
        assert response.status_code == 200

    def test_change_user(self, create_fake_user):
        user_data = create_fake_user
        user_data["username"] = "nealsa"
        with TestClient(app) as client:
            response = client.post("/users/change_user",json=user_data)
        assert response.status_code == 200

    def test_delete_user(self, create_fake_user):
        data = {
            "user_id": create_fake_user["id"]
        }
        with TestClient(app) as client:
            response = client.post("/users/delete_user", params=data)
        assert response.status_code == 200

    def test_token(self, create_fake_user):
        headers = {
            "username": create_fake_user["username"],
            "password": decode_hash_password(create_fake_user["hashed_password"]),
        }
        with TestClient(app) as client:
            response = client.post("/token", data=headers)
        assert response.status_code == 200
