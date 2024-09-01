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


class TestApiCards:
    def test_get_all_cards(self, create_fake_user, auth_fake_user, create_fake_card: dict):
        headers = {
            "Authorization": f"Bearer {create_fake_user["username"]}"
        }
        with TestClient(app) as client:
            response = client.get("cards/getAllCards", headers=headers)
        assert response.status_code == 200

    def test_delete_card(self, create_fake_user, auth_fake_user, create_fake_card: dict):
        headers = {
            "Authorization": f"Bearer {create_fake_user["username"]}"
        }
        data = {
            "card_id": create_fake_card["id"]
        }
        with TestClient(app) as client:
            response = client.post("cards/delete_card", headers=headers, params=data)
        assert response.status_code == 200

