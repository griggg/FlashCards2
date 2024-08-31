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

from fastapi.encoders import jsonable_encoder
from app.models.models import Card

from app.schemas.solved_card_schema import SolveCardSchema

cardsRouter = APIRouter(prefix="/cards")


@cardsRouter.get("/getAllCards/", response_model=List[CardSchema])
def get_all_cards(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    repository_cards = RepositoryCards(session=config_session_maker())

    return repository_cards.get_all_cards(user_id=current_user.id)


@cardsRouter.post("/addCard/", response_model=CardSchema)
def add_card(card: CardSchema, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    repository_cards = RepositoryCards(session=config_session_maker())
    repository_cards.add_card(card)
    return card


@cardsRouter.put("/changeCard")
def change_card():
    pass


@cardsRouter.post("/solve_card")
def solve_card(data: SolveCardSchema,
               card: CardSchema,
               current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    pass
