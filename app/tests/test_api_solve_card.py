import random

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


class TestApiSovleCard:

    def test_add_solve_of_card(self, create_fake_user, auth_fake_user, create_fake_card):
        headers = {
            "Authorization": f"Bearer {create_fake_user["username"]}"
        }
        data = {
            "id": randint(10 ** 8, 10 ** 9),
            "card_fk": create_fake_card["id"],
            "user_fk": create_fake_user["id"],
            "grade": "bad"
        }
        with TestClient(app) as client:
            response = client.post("/cards/solve_card", headers=headers, json=data)
        assert response.status_code == 200

    def test_get_solves_by_user(self, create_fake_user, auth_fake_user, create_fake_card):
        headers = {
            "Authorization": f"Bearer {create_fake_user["username"]}"
        }
        data = {
            "user_id": create_fake_user["id"]
        }
        with TestClient(app) as client:
            response = client.post("/cards/get_solves_by_user", headers=headers, params=data)
        assert response.status_code == 200
