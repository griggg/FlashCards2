from fastapi import APIRouter, Depends
from app.repository.cards import RepositoryCards
from app.utils.config import config_session_maker
from typing import List, Annotated
from app.schemas.card_schema import CardSchema
from app.schemas.users_schema import UserSchema
# from app.utils.crypto import fake_decode_token

from fastapi.security import OAuth2PasswordBearer
from app.api.auth import get_current_active_user
from app.schemas.card_schema import CardSchema
from app.repository.solve_card import RepositorySolveCards
from fastapi.encoders import jsonable_encoder
from app.models.models import Card
from fastapi import HTTPException
from app.schemas.solved_card_schema import SolveCardSchema

cardsRouter = APIRouter(prefix="/cards")


@cardsRouter.get("/getAllCards/", response_model=List[CardSchema])
def get_all_cards(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    repository_cards = RepositoryCards(session=config_session_maker())

    return repository_cards.get_all_cards(user_id=current_user.id)


@cardsRouter.post("/addCard/", response_model=CardSchema)
def add_card(card: CardSchema, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):

    repository_cards = RepositoryCards(session=config_session_maker())
    if repository_cards.get_card_by_id(card.id):
        raise HTTPException(status_code=403, detail="Запись с таким id уже существует")
    repository_cards.add_card(card)
    return card


@cardsRouter.put("/change_card")
def change_card(card: CardSchema):
    repository_card = RepositoryCards(session=config_session_maker())
    repository_card.change_card(card)
    return card

@cardsRouter.post("/delete_card")
def delete_card(card_id):
    repository_card = RepositoryCards(session=config_session_maker())
    repository_card.delete_card(card_id)
    return f"{card_id=} карточка удалена"

@cardsRouter.post("/solve_card")
def solve_card(solve_card: SolveCardSchema,
               current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    repository_solve_card = RepositorySolveCards(session=config_session_maker())
    repository_solve_card.add_solve_card(solve_card)
    return solve_card

@cardsRouter.post("/get_solves_by_user")
def solve_card(user_id: int,
               current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    repository_solve_card = RepositorySolveCards(session=config_session_maker())
    return repository_solve_card.get_solves_by_user(user_id)