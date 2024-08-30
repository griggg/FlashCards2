from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from app.schemas.user import User as UserSchema
from app.models.models import User


class RepositoryUsers():
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_username(self, username: str):
        user = self.session.query(User).where(User.username == username).all()[0]
        return UserSchema(**user.__dict__)

    def


if __name__ == '__main__':
    from app.utils.config import configSession

    db = configSession()

    repo = RepositoryUsers(db)
    # print(repo.getUserByUsername("johndoe"))
    # quit()
    fake_users_db = {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
    # user = User(
    #     username="johndoe",
    #     full_name="John Doe",
    #     email="johndoe@example.com",
    #     hashed_password="fakehashedsecret",
    #     disabled=False,
    # )
    db.add(User(**fake_users_db))
    # db.add(user)
    db.commit()

    all_users = db.query(User).all()
    print(all_users)
