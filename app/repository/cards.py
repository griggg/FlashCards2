from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from schemas.card_schema import CardSchema
from models.models import Card as CardModel, User as UserModel
from sqlalchemy import insert, and_


class RepositoryCards():
    def __init__(self, session: Session):
        self.session = session

    def get_all_cards_by_user(self, author_id: int) -> List[CardSchema]:
        cards = self.session.query(CardModel).filter(CardModel.user_fk == author_id)

        return [CardSchema(**cards.__dict__) for cards in cards]

    def get_all_public_cards(self, author_id):
        cards = self.session.query(CardModel).filter(and_(CardModel.user_fk == author_id, CardModel.is_private==False))
        return cards

    def get_card_by_id(self, card_id):
        card = self.session.query(CardModel).where(CardModel.id == card_id).one_or_none()
        return card

    def add_card(self, card: CardSchema) -> None:
        card = CardModel(**card.model_dump(exclude_none=True))

        self.session.add(card)
        self.session.commit()

    def delete_card(self, card_id) -> None:
        self.session.query(CardModel).where(CardModel.id==card_id).delete()
        self.session.commit()

    def change_card(self, new_card: CardSchema):
        card = self.session.query(CardModel).where(CardModel.id == new_card.id)
        self.session.query(card.update(new_card.model_dump(exclude_none=True)))
        self.session.commit()


if __name__ == '__main__':
    from app.utils.config import config_session_maker

    db = RepositoryCards(session=config_session_maker())
    # cards = db.getAllCards()
    # print(cards)
    cards = db.get_card_by_id(user_id=1)
    print(cards)
