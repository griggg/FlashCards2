from app.utils.config import config_session_maker
from app.repository.cards import RepositoryCards
from app.schemas.card_schema import CardSchema
from pytest import fixture
from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.users_schema import UserSchema
from app.models.models import Card

@fixture()
def session() -> Session:
    return config_session_maker()


@fixture()
def create_fake_user(session: Session) -> dict:
    fake_user_data = {
        "id": 280923,
        "username": "alc",
        "email": "test@gmail.com",
        "full_name": "alsa",
        "disabled": False,
        "hashed_password": "secret"
    }
    if session.query(User).where(User.id == fake_user_data["id"]):
        return fake_user_data
    fake_user = User(**fake_user_data)
    session.add(fake_user)
    session.commit()
    return fake_user_data

@fixture()
def create_fake_card(session: Session, create_fake_user: dict) -> dict:
    fake_user_data = create_fake_user
    fake_card_data = {
        "id": 44444,
        "name": "test_card_name",
        "problem": "2 + 2",
        "answer": "4",
        "category": "зачет по математике",
        "user_fk": fake_user_data["id"]
    }
    session.query(Card).where(Card.id==fake_card_data["id"]).delete()
    session.add(Card(**fake_card_data))
    session.commit()
    return fake_card_data


class TestRepositoryCards:
    def test_get_all_cards(self, create_fake_user: dict, session: Session):
        fake_user_data = UserSchema(**create_fake_user)
        repository_cards = RepositoryCards(session)
        cards = repository_cards.get_all_cards(user_id=fake_user_data.id)
        print(cards)
        assert isinstance(cards, list)
        for i in cards:
            assert isinstance(i, CardSchema)

    def test_add_card(self, session: Session, create_fake_card: dict):
        fake_card_data = create_fake_card
        fake_card: Card = session.query(Card).where(Card.id==fake_card_data["id"]).one()
        assert fake_card == Card(**fake_card_data)
