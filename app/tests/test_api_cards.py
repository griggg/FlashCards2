import pytest
from repository.cards import RepositoryCards
from repository.users import RepositoryUsers
from utils.config import config_session
from random import randint
from schemas.users_schema import UserSchema
from schemas.card_schema import CardSchema

user_id = randint(10 ** 8, 10 ** 9)
user = {
    "id": user_id,
    "username": "alc",
    "email": "test@gmail.com",
    "full_name": "alsa",
    "disabled": True,
    "hashed_password": "secret"
}

def test_get_all_cards_by_user(db_session, client):
    repository_cards = RepositoryCards(session=config_session)

    # добавление авторизованного пользователя, который хочет посмотреть свои/чужие карточки
    repository_users = RepositoryUsers(session=config_session)
    user_schema: UserSchema = UserSchema(**user)
    user_schema.disabled = False
    repository_users.create_user(user_schema)







def test_add_card():


def test_change_card():


def test_delete_card():


def test_solve_card():


def test_get_solves_by_user():


