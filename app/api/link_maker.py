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
from repository.favorite_cards import RepositoryFavoriteCards
from schemas.favorite_card import FavoriteCardSchema
import redis
from utils.secret import REDIS_HOST

link_maker = APIRouter(prefix="/linkmaker")

@link_maker.get("/get_card_by_link/", response_model=CardSchema)
def get_card_by_link(link: str,
                        current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    repository_card = RepositoryCards(session=config_session)
    redis_con = redis.Redis(host=REDIS_HOST, port=6379)
    card_id = redis_con.get(link).decode("utf-8")

    card = repository_card.get_card_by_id(card_id=card_id)
    if repository_card.get_card_by_id(card_id=card_id) is None:
        # если мы удалили карточку, то мы хотим чтобы в редисе удалилась ссылка на неё
        raise HTTPException(status_code=400, detail="Карточки с таким id не существует")
    return card



@link_maker.post("/make_link_to_card/")
def make_link_to_card(card_id: int,
                        current_user: Annotated[UserSchema, Depends(get_current_active_user)],
                      time_expire:int = 100000
                      ):
    repository_card = RepositoryCards(session=config_session)
    if repository_card.get_card_by_id(card_id=card_id):
        redis_con = redis.Redis(host=REDIS_HOST, port=6379)
        link = "ABCASADSA"
        redis_con.mset({link: card_id})
    else:
        raise HTTPException(status_code=400, detail="Карточка с таким id не найдена")
    return link