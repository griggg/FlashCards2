from pydantic import BaseModel
from datetime import datetime
class FavoriteCardSchema(BaseModel):
    id: int
    card_fk: int
    user_fk: int
    created: datetime = datetime.now()