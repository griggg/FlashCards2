from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from app.schemas.card_schema import CardSchema
from app.models.models import Card as CardModel, User as UserModel
from sqlalchemy import insert
from app.schemas.solved_card_schema import SolveCardSchema
from app.models.models import SolveCard

class RepositorySolveCards():
    def __init__(self, session: Session):
        self.session = session

    def add_solve_card(self, solve_card: SolveCardSchema) -> None:
        self.session.add(SolveCard(**solve_card.model_dump(exclude_none=True)))
        self.session.commit()

    def get_solves_by_user(self, user_id: int) -> List[SolveCardSchema]:
        solves = self.session.query(SolveCard).where(SolveCard.user_fk == user_id).all()
        return [SolveCardSchema(**solve) for solve in solves]


if __name__ == '__main__':
    from app.utils.config import configSession

    db = RepositorySolveCards(session=configSession())
    # cards = db.getAllCards()
    # print(cards)
    cards = db.get_all_cards(user_id=1)
    print(cards)
