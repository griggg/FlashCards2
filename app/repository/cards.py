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

    def get_all_cards(self, user_id: int) -> List[CardSchema]:
        cards = self.session.query(CardModel).filter(CardModel.user_fk == user_id)

        return [CardSchema(**cards.__dict__) for cards in cards]

    def get_card_by_id(self, card_id):
        card = self.session.query(CardModel).where(CardModel.id == card_id).one_or_none()
        return card

    def add_card(self, card: CardSchema) -> None:
        card = CardModel(**card.model_dump(exclude_none=True))

        self.session.add(card)
        self.session.commit()

    def delete_card(self, card_id) -> None:
        self.session.query(CardModel).where(CardModel==card_id).delete()
        self.session.commit()

    def change_card(self, card: CardSchema):
        self.session.query(CardModel).where(CardModel.id == card.id)


if __name__ == '__main__':
    from app.utils.config import configSession

    db = RepositoryCards(session=configSession())
    # cards = db.getAllCards()
    # print(cards)
    cards = db.get_card_by_id(user_id=1)
    print(cards)
