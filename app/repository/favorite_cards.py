from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from schemas.card_schema import CardSchema
from models.models import (
    Card as CardModel,
    User as UserModel,
    SolveCard,
    FavoriteCard
)
from sqlalchemy import insert
from schemas.solved_card_schema import SolveCardSchema
from schemas.users_schema import UserSchema
from schemas.favorite_card import FavoriteCardSchema

class RepositoryFavoriteCards():
    def __init__(self, session: Session):
        self.session = session

    def add_favorite_card(self, favorite_card: FavoriteCardSchema) -> None:
        self.session.add(FavoriteCard(**favorite_card.model_dump(exclude_none=True)))
        self.session.commit()

    def get_favorite_cards_by_user(self, user_id: int) -> list:
        fav_cards = self.session.query(FavoriteCard).where(FavoriteCard.user_fk == user_id).all()
        return [FavoriteCardSchema(**fav_card.__dict__) for fav_card in fav_cards]

    def get_favorite_card(self, user_id: int, card_id) -> FavoriteCardSchema | None:
        fav_card = self.session.query(FavoriteCard).where(FavoriteCard.user_fk == user_id,
                                                           FavoriteCard.card_fk == card_id).one_or_none()
        if fav_card:
            return FavoriteCardSchema(**fav_card.__dict__)

    def delete_favorite_card(self, card_id: int, user_id: int) -> None:
        self.session.query(FavoriteCard).where(FavoriteCard.user_fk == user_id, FavoriteCard.card_fk == card_id).delete()
        self.session.commit()




