from typing import Optional

from sqlalchemy.orm import as_declarative, DeclarativeBase, MappedColumn, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, ForeignKey, Column, Integer
from typing import List
class AbstractModel(DeclarativeBase):
    id: Mapped[int] = MappedColumn(primary_key=True)


class Card(AbstractModel):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    problem: Mapped[str]
    answer: Mapped[str]
    category: Mapped[str]
    user: Mapped["User"] = relationship(back_populates="cards", uselist=False)
    user_fk: Mapped[int] = mapped_column(ForeignKey("users.id"))


class User(AbstractModel):
    __tablename__ = "users"
    username: Mapped[str]
    email: Mapped[str | None]
    full_name: Mapped[str| None]
    disabled: Mapped[bool | None]
    cards: Mapped[List["Card"]] = relationship(back_populates="user", uselist=True)
    hashed_password: Mapped[str]

if __name__ == '__main__':
    from app.utils.config import configEngine as engine

    AbstractModel.metadata.drop_all(engine)

    AbstractModel.metadata.create_all(engine)


