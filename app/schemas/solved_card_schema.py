from pydantic import BaseModel

class SolveCardSchema(BaseModel):
    id: int
    card_fk: int
    user_fk: int
    grade: str  # Bad, Medium, Good, насколько хорошо знаешь