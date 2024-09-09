from typing import Optional

from sqlalchemy.orm import as_declarative, DeclarativeBase, MappedColumn, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, ForeignKey, Column, Integer
from typing import List


class AbstractModel(DeclarativeBase):
    pass


class User(AbstractModel):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str | None]
    full_name: Mapped[str | None]
    disabled: Mapped[bool | None]
    hashed_password: Mapped[str]
    cards: Mapped[List["Card"]] = relationship(back_populates="user", uselist=True, cascade="all,delete")
    solved_cards: Mapped[List["SolveCard"]] = relationship(back_populates="user", uselist=True, cascade="all,delete")


class Card(AbstractModel):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    problem: Mapped[str]
    answer: Mapped[str]
    category: Mapped[str]
    user: Mapped["User"] = relationship(back_populates="cards", uselist=False)
    user_fk: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    # ondelete="CASCADE", при удалении строки в родительской таблице users
    # удалится и запись в дочерней cards. дочерняя - та, в которой внешний ключ
    solves: Mapped["SolveCard"] = relationship(back_populates="card", uselist=True, cascade="all,delete")
    is_private: Mapped[bool] = mapped_column(default=True)

class SolveCard(AbstractModel):
    __tablename__ = "solves_cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="solved_cards", uselist=False)
    card: Mapped["Card"] = relationship(back_populates="solves", uselist=False)
    card_fk: Mapped[int] = mapped_column(ForeignKey("cards.id", ondelete="CASCADE"))
    user_fk: Mapped[int] = mapped_column(ForeignKey("users.id"))
    grade: Mapped[str] # Bad, Medium, Good, насколько хорошо знаешь

if __name__ == '__main__':
    from utils.config import config_engine as engine

    AbstractModel.metadata.drop_all(engine)

    AbstractModel.metadata.create_all(engine)
