from fastapi.testclient import TestClient
from main import app
from random import randint
from repository.users import RepositoryUsers
from schemas.users_schema import UserSchema
import pytest
from utils.config import config_engine, config_session
from models.models import AbstractModel

user_id = randint(10 ** 8, 10 ** 9)

user = {
    "id": user_id,
    "username": "alc",
    "email": "test@gmail.com",
    "full_name": "alsa",
    "disabled": True,
    "hashed_password": "secret"
}


@pytest.mark.parametrize("user",
                         [user,
                          pytest.param(user, marks=pytest.mark.xfail)
                          ]
                         )
def test_create_user(db_session, user):
    with TestClient(app) as client:
        response = client.post("/users/create_account", json=user)
    assert response.status_code == 200
    repository_users = RepositoryUsers(session=db_session)
    assert repository_users.get_user_by_id(user_id)
    assert repository_users.get_user_by_id(user_id).username == user["username"]
    assert repository_users.get_user_by_id(user_id).email == user["email"]
    assert repository_users.get_user_by_id(user_id).full_name == user["full_name"]


def test_login(db_session, client):
    repository_users = RepositoryUsers(session=db_session)
    user_schema = UserSchema(**user)
    user_schema.disabled = True
    repository_users.create_user(user=user_schema)
    headers = {
        "username": user["username"],
        "password": user["hashed_password"],
    }
    response = client.post("/token", data=headers)

    assert response.status_code == 200
    assert repository_users.get_user_by_id(user["id"]).disabled == False


# @pytest.mark.skip
# def test_get_me(db_session, client):
#     """ disabled = False => авторизован"""
#
#     headers = {
#        "Authorization": f"Bearer user[username]"
#     }


def test_create_account(db_session, client):
    response = client.post("/users/create_account", json=user)

    assert response.status_code == 200
    repository_users = RepositoryUsers(session=db_session)
    assert repository_users.get_user_by_id(user["id"])


def test_change_user(db_session, client):
    repository_users = RepositoryUsers(session=db_session)
    user_schema = UserSchema(**user)
    user_schema.full_name = "nepon"
    user_schema.disabled = False
    repository_users.create_user(user=user_schema)

    auth = {
        "Authorization": f"Bearer {user["username"]}"
    }
    user_schema.full_name = "pon"
    response = client.post("/users/change_user", headers=auth, json=user_schema.model_dump())

    assert response.status_code == 200
    assert repository_users.get_user_by_id(user_schema.id).full_name == "pon"


def test_delete_user(db_session, client):
    repository_users = RepositoryUsers(session=db_session)
    user_schema = UserSchema(**user)
    # создание авторизованного пользователя
    user_schema.disabled = False
    repository_users.create_user(user=user_schema)

    auth = {
        "Authorization": f"Bearer {user["username"]}"
    }
    data = {
        "user_id": user_schema.id
    }
    response = client.post("/users/delete_user", headers=auth, params=data)

    assert response.status_code == 200
    assert not (repository_users.get_user_by_id(user_schema.id))
