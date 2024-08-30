from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from app.schemas.cardSchema import CardSchema
from app.models.models import Card as CardModel, User as UserModel
from sqlalchemy import insert


class RepositoryCards():
    def __init__(self, session: Session):
        self.session = session

    def get_all_cards(self, user_id: int) -> List[CardSchema]:
        cards = self.session.query(CardModel).filter(CardModel.user_fk == user_id)

        return [CardSchema(**cards.__dict__) for cards in cards]

    def add_card(self, card: CardSchema):
        card = CardModel(**card.model_dump(exclude_none=True))

        self.session.add(card)
        self.session.commit()


if __name__ == '__main__':
    from app.utils.config import configSession

    db = RepositoryCards(session=configSession())
    # cards = db.getAllCards()
    # print(cards)
    cards = db.get_all_cards(user_id=1)
    print(cards)
