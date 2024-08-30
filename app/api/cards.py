from fastapi import APIRouter, Depends
from app.repository.cards import RepositoryCards
from app.utils.config import configSession
from typing import List, Annotated
from app.schemas.cardSchema import CardSchema
from app.schemas.user import User
from app.utils.crypto import fake_decode_token

from fastapi.security import OAuth2PasswordBearer
from app.api.auth import get_current_active_user
from app.schemas.cardSchema import CardSchema
cardsRouter = APIRouter(prefix="/cards")
from fastapi.encoders import jsonable_encoder
from app.models.models import Card
@cardsRouter.get("/getAllCards/", response_model=List[CardSchema])
def getAllCards(current_user: Annotated[User, Depends(get_current_active_user)]):
    dbCards = RepositoryCards(session=configSession())
    return dbCards.getAllCards()


@cardsRouter.post("/addCard/", response_model=CardSchema)
def addCard(card: CardSchema, current_user: Annotated[User, Depends(get_current_active_user)]):
    repoCards = RepositoryCards(session=configSession())
    tmp = card
    repoCards.addCard(card)
    print("good")
    return tmp

@cardsRouter.put("/changeCard")
def changeCard():
    """ Разобраться put или что какой метод юзать, придумать как это нормально сделать"""

    pass