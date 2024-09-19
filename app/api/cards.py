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
from repository.users import RepositoryUsers
from utils.config import REDIS_HOST
import redis
from utils.link_maker import make_link_by_id

cardsRouter = APIRouter(prefix="/cards")


@cardsRouter.get("/getAllCards/", response_model=List[CardSchema])
def get_all_cards_by_user(author_id: int, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """ Возвращает все свои/чужие карточки """
    repository_cards = RepositoryCards(session=config_session)
    repository_users = RepositoryUsers(session=config_session)

    if repository_users.get_user_by_id(author_id) is None:
        raise HTTPException(status_code=404, detail="Пользователя с таким id не существует")

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


@cardsRouter.put("/change_card", response_model=CardSchema)
def change_card(card: CardSchema, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """ Изменяет карточку """
    repository_card = RepositoryCards(session=config_session)

    if card.user_fk != current_user.id:
        raise HTTPException(status_code=403, detail="Пользователь не может менять чужие карточки")
    repository_card.change_card(card)
    return card


@cardsRouter.post("/delete_card", response_model=str)
def delete_card(card_id, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """ Удаляет карточку """
    repository_card = RepositoryCards(session=config_session)
    card = repository_card.get_card_by_id(card_id=card_id)

    if card.user_fk != current_user.id:
        raise HTTPException(status_code=403, detail="Пользователь не может удалять чужие карточки")
    repository_card.delete_card(card_id)

    # удаляем shareLink на карточку, если есть
    redis_con = redis.Redis(host=REDIS_HOST, port=6379)
    link = make_link_by_id(card_id=card_id)
    redis_con.delete(link)

    return f"{card_id=} карточка удалена"


@cardsRouter.post("/solve_card", response_model=SolveCardSchema)
def solve_card(solve_card: SolveCardSchema,
               current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """ Добавляет решение карточки """
    repository_solve_card = RepositorySolveCards(session=config_session)
    repository_solve_card.add_solve_card(solve_card)
    return solve_card


@cardsRouter.get("/get_solves_by_user", response_model=List[SolveCardSchema])
def get_solves_by_user(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """ возвращает все решения авторизованного пользователя """

    repository_solve_card = RepositorySolveCards(session=config_session)
    return repository_solve_card.get_solves_by_user(current_user.id)


@cardsRouter.post("/add_card_to_favorite", response_model=str)
def add_card_to_favorite(favorite_card: FavoriteCardSchema,
                         current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """ Добавляет карточку в избранное """
    repository_card = RepositoryCards(session=config_session)
    repository_favorite_cards = RepositoryFavoriteCards(session=config_session)

    card = repository_card.get_card_by_id(favorite_card.card_fk)
    if not card:
        return HTTPException(status_code=404, detail="Карточки с таким id не существует")

    if favorite_card.user_fk != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Вы не можете добавить карточку в избранное для другого пользователя")

    if card.user_fk != current_user.id:
        if card.is_private == True:
            raise HTTPException(status_code=403, detail="Эта карточка не доступна для вас")

    repository_favorite_cards.add_favorite_card(favorite_card)
    return f"Карточка {favorite_card.card_fk=} добавленая в избранное для пользователя {favorite_card.user_fk}"


@cardsRouter.post("/delete_favorite_card", response_model=str)
def delete_card_from_favorite(card_id: int,
                              current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """ Удаляет карточку из избранных для пользователя """
    # Удаляет favorite card, у которого fav_card.user_fk == current_user.id и card_id == fav_card.card_fk
    repository_favorite_cards = RepositoryFavoriteCards(session=config_session)
    repository_favorite_cards.delete_favorite_card(card_id=card_id, user_id=current_user.id)
    return f"Карточка {card_id=} удалена из избранного для пользователя {current_user.id}"


@cardsRouter.get("/get_favorite_cards", response_model=List[FavoriteCardSchema])
def get_favorite_cards(user_id: int):
    """ Возвращает список избранных карточек какого-то пользователя """
    repository_favorite_cards = RepositoryFavoriteCards(session=config_session)
    fav_cards_by_user = repository_favorite_cards.get_favorite_cards_by_user(user_id=user_id)
    return fav_cards_by_user


@cardsRouter.get("/get_card_by_link/", response_model=CardSchema)
def get_card_by_link(link: str,
                     current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    """  Возвращает карточку по ссылке на неё """
    repository_card = RepositoryCards(session=config_session)
    redis_con = redis.Redis(host=REDIS_HOST, port=6379)
    card_id = redis_con.get(link)
    if card_id:
        card_id = card_id.decode("utf-8")
    else:
        raise HTTPException(status_code=404, detail="По этой ссылке карточек не найдено")

    card = repository_card.get_card_by_id(card_id=card_id)
    if repository_card.get_card_by_id(card_id=card_id) is None:
        # если мы удалили карточку, то мы хотим чтобы в редисе удалилась ссылка на неё
        raise HTTPException(status_code=404, detail="Карточки с таким id не существует")
    return card


@cardsRouter.post("/make_link_to_card/", response_model=str)
def make_link_to_card(card_id: int,
                      current_user: Annotated[UserSchema, Depends(get_current_active_user)],
                      time_expire_sec: int = 10**4
                      ):
    """ Создаёт ссылку на карточку, по которой другие пользователи смогут её посмотреть """
    repository_card = RepositoryCards(session=config_session)
    if repository_card.get_card_by_id(card_id=card_id):
        redis_con = redis.Redis(host=REDIS_HOST, port=6379)
        link = make_link_by_id(card_id=card_id)
        redis_con.set(link, card_id)
        redis_con.expire(link, time_expire_sec)
    else:
        raise HTTPException(status_code=404, detail="Карточка с таким id не найдена")
    return link
