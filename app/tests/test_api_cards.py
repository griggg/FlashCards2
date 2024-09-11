import datetime

import pytest
from repository.cards import RepositoryCards
from repository.solve_card import RepositorySolveCards
from repository.users import RepositoryUsers
from random import randint

from schemas.favorite_card import FavoriteCardSchema
from schemas.users_schema import UserSchema
from schemas.card_schema import CardSchema
import os
from fastapi.testclient import TestClient
from main import app
from repository.favorite_cards import RepositoryFavoriteCards

user_id = randint(10 ** 8, 10 ** 9)
user_id2 = randint(10 ** 7, 10 ** 8)
user = {
    "id": user_id,
    "username": "alc",
    "email": "test@gmail.com",
    "full_name": "alsa",
    "disabled": False,
    "hashed_password": "secret"
}

user2 = {
    "id": user_id2,
    "username": "alc2",
    "email": "test@gmail.com",
    "full_name": "alsa",
    "disabled": False,
    "hashed_password": "secret"
}

card = {
    "id": 0,
    "name": "PublicCard",
    "problem": "string",
    "answer": "string",
    "category": "string",
    "user_fk": user_id,
    "is_private": False
}

card2 = {
    "id": 1,
    "name": "privateCard1",
    "problem": "string",
    "answer": "string",
    "category": "string",
    "user_fk": user_id,
    "is_private": True
}


def test_get_all_cards_by_user(db_session):
    # добавление авторизованного пользователя/ей, который хочет посмотреть свои/чужие карточки
    repository_users = RepositoryUsers(session=db_session)
    repository_cards = RepositoryCards(session=db_session)

    author_schema: UserSchema = UserSchema(**user)
    author_schema.disabled = False
    repository_users.create_user(author_schema)
    # добавление карточек
    repository_cards.add_card(CardSchema(**card))
    repository_cards.add_card(CardSchema(**card2))

    auth = {
        "Authorization": f"Bearer {author_schema.username}"
    }
    data = {
        "author_id": author_schema.id
    }
    # запрос
    with TestClient(app) as client:
        response = client.get(url="/cards/getAllCards", headers=auth, params=data)

    print(response.content, "content")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_add_card(db_session):
    from utils.config import config_session
    db_session = config_session
    repository_users = RepositoryUsers(session=db_session)
    repository_cards = RepositoryCards(session=db_session)

    author_schema: UserSchema = UserSchema(**user)
    author_schema.disabled = False
    repository_users.create_user(author_schema)

    auth = {
        "Authorization": f"Bearer {author_schema.username}"
    }
    data = card
    with TestClient(app) as client:
        response = client.post(url="/cards/addCard", headers=auth, json=data)
    assert response.status_code == 200

    assert repository_cards.get_card_by_id(card["id"])


def test_change_card(db_session, client):
    repository_users = RepositoryUsers(session=db_session)
    repository_cards = RepositoryCards(session=db_session)

    author_schema: UserSchema = UserSchema(**user)
    author_schema.disabled = False
    repository_users.create_user(author_schema)

    card_schema = CardSchema(**card)
    card_schema.is_private = False
    repository_cards.add_card(card_schema)

    changed_card = card_schema
    changed_card.is_private = True
    auth = {
        "Authorization": f"Bearer {author_schema.username}"
    }
    data = changed_card.model_dump(exclude_none=True)
    response = client.put(url="/cards/change_card", headers=auth, json=data)
    assert response.status_code == 200

    assert repository_cards.get_card_by_id(card["id"])

    assert repository_cards.get_card_by_id(card["id"]).is_private == True


def test_delete_card(db_session, client, add_active_user, add_card):
    auth = {
        "Authorization": f"Bearer {add_active_user.username}"
    }
    data = {
        "card_id": add_card.id
    }
    response = client.post(url="/cards/delete_card", headers=auth, params=data)
    assert response.status_code == 200
    repository_cards = RepositoryCards(session=db_session)
    assert not (repository_cards.get_card_by_id(add_card.id))


def test_solve_card(db_session, client, add_active_user, add_card, auth):

    solve_of_card = {
        "id": 0,
        "card_fk": add_card.id,
        "user_fk": add_active_user.id,
        "grade": "bad"
    }
    response = client.post(url="/cards/solve_card", headers=auth, json=solve_of_card)
    assert response.status_code == 200

    repository_solve_card = RepositorySolveCards(session=db_session)
    assert repository_solve_card.get_solve_by_id(solve_of_card["id"])


def test_get_solves_by_user(db_session, client, add_active_user, add_card, add_solve, auth):

    response = client.get(url="/cards/get_solves_by_user", headers=auth)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_add_card_to_favorite(db_session, client, add_active_user, add_card, auth):
    fav_card = {
      "id": 0,
      "card_fk": add_card.id,
      "user_fk": add_active_user.id,
      "created": str(datetime.datetime.now())
    }
    response = client.post(url="/cards/add_card_to_favorite", headers=auth, json=fav_card)
    assert response.status_code == 200

    repository_fav_cards = RepositoryFavoriteCards(session=db_session)
    assert repository_fav_cards.get_favorite_card(user_id=add_active_user.id, card_id=add_card.id)

def test_delete_card_from_favorite(db_session, client, add_active_user, add_card, add_favorite_card, auth):
    data = {
        "card_id": add_card.id
    }
    response = client.post(url="/cards/delete_favorite_card", headers=auth, params=data)
    assert response.status_code == 200

    repository_fav_cards = RepositoryFavoriteCards(session=db_session)
    assert not(repository_fav_cards.get_favorite_card(user_id=add_active_user.id, card_id=add_card.id))

def test_get_favorite_cards(db_session, client, add_active_user, add_card, add_favorite_card, auth):
    data = {
        "user_id": add_active_user.id
    }
    response = client.get(url="/cards/get_favorite_cards", headers=auth, params=data)
    assert response.status_code == 200
    fav_cards_by_user = response.json()
    assert  type(fav_cards_by_user) == list

    repository_fav_cards = RepositoryFavoriteCards(session=db_session)
    for fav_card in fav_cards_by_user:
        fav_card = FavoriteCardSchema(**fav_card)
        assert repository_fav_cards.get_favorite_card(user_id=fav_card.user_fk, card_id=fav_card.card_fk)


