from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import insert
from typing import List
from schemas.users_schema import UserSchema as UserSchema
from models.models import User

from utils.crypto import fake_hash_password

class RepositoryUsers():
    def __init__(self, session: Session):
        self.session = session

    def set_user_active(self, id):
        user = self.session.query(User).where(User.id == id).one()
        user.disabled = False
        self.session.add(user)
        self.session.commit()

    def get_user_by_id(self, id: int):
        user = self.session.query(User).where(User.id == id).one_or_none()
        if user:
            return UserSchema(**user.__dict__)
        return None

    def get_user_by_username(self, username: str) -> UserSchema:
        user = self.session.query(User).where(User.username == username).all()
        if not(user):
            # raise HttpException  service
            return None
        return UserSchema(**user[0].__dict__)

    def create_user(self, user: UserSchema):
        data = User(**user.model_dump(exclude_none=True))
        data.hashed_password = fake_hash_password(data.hashed_password)
        self.session.add(data)
        self.session.commit()

    def change_user(self, user: UserSchema):
        self.session.query(User).filter(User.id == user.id).update(user.model_dump(exclude_none=True))
        self.session.commit()

    def delete_user(self, user_id: int):
        self.session.query(User).where(User.id==user_id).delete()
        self.session.commit()


if __name__ == '__main__':
    from utils.config import configSession

    db = configSession()

    repo = RepositoryUsers(db)
    # print(repo.getUserByUsername("johndoe"))
    # quit()
    