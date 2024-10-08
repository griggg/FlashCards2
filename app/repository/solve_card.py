from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from schemas.card_schema import CardSchema
from models.models import Card as CardModel, User as UserModel
from sqlalchemy import insert
from schemas.solved_card_schema import SolveCardSchema
from models.models import SolveCard

class RepositorySolveCards():
    def __init__(self, session: Session):
        self.session = session

    def add_solve_card(self, solve_card: SolveCardSchema) -> None:
        self.session.add(SolveCard(**solve_card.model_dump(exclude_none=True)))
        self.session.commit()

    def get_solves_by_user(self, user_id: int) -> List[SolveCardSchema]:
        solves = self.session.query(SolveCard).where(SolveCard.user_fk == user_id).all()
        return [SolveCardSchema(**solve.__dict__) for solve in solves]

    def get_solve_by_id(self, solve_id: int) -> SolveCardSchema | None:
        solve = self.session.query(SolveCard).where(SolveCard.id == solve_id).one_or_none()
        return solve

if __name__ == '__main__':
    from utils.config import configSession

    db = RepositorySolveCards(session=configSession())
    # cards = db.getAllCards()
    # print(cards)
    cards = db.get_all_cards(user_id=1)
    print(cards)
