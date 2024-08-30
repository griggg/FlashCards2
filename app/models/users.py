from typing import Optional, List

from sqlalchemy.orm import as_declarative, DeclarativeBase, MappedColumn, Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, ForeignKey, Column, Integer

# TODO: над научиться разделять модели на файлы

# class AbstractModelUser(DeclarativeBase):
#     id: Mapped[int] = MappedColumn(primary_key=True)
#
#
#
#
# if __name__ == '__main__':
#     from app.utils.config import configEngine as engine
#
#     AbstractModelUser.metadata.drop_all(engine)
    # AbstractModelUser.metadata.create_all(engine)
