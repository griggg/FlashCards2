from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from app.schemas.cardSchema import CardSchema
from app.models.models import Card as CardModel
from sqlalchemy import insert
class RepositoryCards():
    def __init__(self, session: Session):
        self.session = session

    def getAllCards(self) -> List[CardSchema]:
        cards = self.session.query(CardModel).all()
        return [CardSchema(**cards.__dict__) for cards in cards]

    def addCard(self, card: CardSchema):
        card = CardModel(**card.model_dump(exclude_none=True))
        # TODO: сделать по нормальному преобразование pydantic или словаря в модель алхимии


        self.session.add(card)
        self.session.commit()


if __name__ == '__main__':
    from app.utils.config import configSession
    db = RepositoryCards(session=configSession())
    # cards = db.getAllCards()
    # print(cards)

    data = {
          "id": 1,
          "name": "string",
          "problem": "string",
          "answer": "string",
          "category": "string",
          "user_fk": "1"
    }
    card =CardSchema(**data)
    # card = CardModel(
    #     id=card.id,
    #     name=card.name,
    #     problem=card.problem,
    #     answer=card.answer,
    #     category=card.category,
    #     user_fk=card.user_fk
    # )
    print(card)
    db.addCard(card)

