from app.utils.config import config_session_maker
from app.repository.cards import RepositoryCards
from app.schemas.card_schema import CardSchema

def test_get_all_cards():
    session = config_session_maker()

    repository_cards = RepositoryCards(session)
    cards = repository_cards.get_all_cards(user_id=1)
    print(cards)
    assert isinstance(cards, list)
    for i in cards:
        assert isinstance(i, CardSchema)
