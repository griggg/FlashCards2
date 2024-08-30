from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from app.schemas.card_schema import CardSchema
from app.models.models import Card as CardModel, User as UserModel
from sqlalchemy import insert


class RepositoryCards():
    def __init__(self, session: Session):
        self.session = session

    def add_solve_card(self):
        pass

    def get_solves_by_user(self):
        pass

    def get_last_solves(self):
        pass


if __name__ == '__main__':
    from app.utils.config import configSession

    db = RepositoryCards(session=configSession())
    # cards = db.getAllCards()
    # print(cards)
    cards = db.get_all_cards(user_id=1)
    print(cards)
