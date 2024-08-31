from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from app.schemas.card_schema import CardSchema
from app.models.models import Card as CardModel, User as UserModel
from sqlalchemy import insert
from app.schemas.solved_card_schema import SolveCardSchema

class RepositorySolveCards():
    def __init__(self, session: Session):
        self.session = session

    def add_solve_card(self) -> None:
        pass

    def get_solves_by_user(self) -> List[SolveCardSchema]:
        pass

    def get_last_solves(self) -> List[SolveCardSchema]:
        pass


if __name__ == '__main__':
    from app.utils.config import configSession

    db = RepositorySolveCards(session=configSession())
    # cards = db.getAllCards()
    # print(cards)
    cards = db.get_all_cards(user_id=1)
    print(cards)
