from fastapi import APIRouter, Depends
from repository.cards import RepositoryCards
from utils.config import config_session
from typing import List, Annotated
from schemas.card_schema import CardSchema
from schemas.users_schema import UserSchema
# from app.utils.crypto import fake_decode_token

from fastapi.security import OAuth2PasswordBearer
from api.auth import get_current_active_user
from schemas.card_schema import CardSchema
from repository.solve_card import RepositorySolveCards
from fastapi.encoders import jsonable_encoder
from models.models import Card
from fastapi import HTTPException
from schemas.solved_card_schema import SolveCardSchema

cardsRouter = APIRouter(prefix="/cards")


@cardsRouter.get("/getAllCards/", response_model=List[CardSchema])
def get_all_cards_by_user(author_id: int, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """ Возвращает все свои/чужие карточки """
    repository_cards = RepositoryCards(session=config_session)
    if author_id == current_user.id:
        cards = repository_cards.get_all_cards_by_user(author_id=author_id)
    else:
        cards = repository_cards.get_all_public_cards(author_id=author_id)

    return cards


@cardsRouter.post("/addCard/", response_model=CardSchema)
def add_card(card: CardSchema, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """Добавляет карточку"""
    repository_cards = RepositoryCards(session=config_session)
    if repository_cards.get_card_by_id(card.id):
        raise HTTPException(status_code=403, detail="Запись с таким id уже существует")
    if card.user_fk != current_user.id:
        raise HTTPException(status_code=403, detail="Нельзя добавлять карточки чужим пользователям")
    repository_cards.add_card(card)
    return card


@cardsRouter.put("/change_card")
def change_card(card: CardSchema, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """ Изменяет карточку """
    if card.user_fk != current_user.id:
        raise HTTPException(status_code=403, detail="Пользователь не может менять чужие карточки")
    repository_card = RepositoryCards(session=config_session)
    repository_card.change_card(card)
    return card

@cardsRouter.post("/delete_card")
def delete_card(card_id, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """ Удаляет карточку """
    repository_card = RepositoryCards(session=config_session)
    card = repository_card.get_card_by_id(card_id=card_id)
    # with open("log.txt", "w", encoding="utf-8") as file:
    #     file.write(f"{card.user_fk}, {current_user.id}, \n")
    if card.user_fk != current_user.id:
        raise HTTPException(status_code=403, detail="Пользователь не может удалять чужие карточки")
    repository_card.delete_card(card_id)
    return f"{card_id=} карточка удалена"

@cardsRouter.post("/solve_card")
def solve_card(solve_card: SolveCardSchema,
               current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """ Добавляет решение карточки """
    repository_solve_card = RepositorySolveCards(session=config_session)
    repository_solve_card.add_solve_card(solve_card)
    return solve_card

@cardsRouter.post("/get_solves_by_user")
def get_solves_by_user(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """ возвращает все решения авторизованного пользователя """

    repository_solve_card = RepositorySolveCards(session=config_session)
    return repository_solve_card.get_solves_by_user(current_user.id)


