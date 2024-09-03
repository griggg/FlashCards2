from pydantic import BaseModel

class CardSchema(BaseModel):
    id: int
    name: str
    problem: str
    answer: str
    category: str
    user_fk: int
    is_private: bool=True
