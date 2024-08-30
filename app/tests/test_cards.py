from app.utils.config import configSession
from app.repository.cards import RepositoryCards
from app.schemas.cardSchema import CardSchema

def test_get_all_cards():
    session = configSession()

    repository_cards = RepositoryCards(session)
    cards = repository_cards.get_all_cards(user_id=1)
    print(cards)
    assert isinstance(cards, list)
    for i in cards:
        assert isinstance(i, CardSchema)
