from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi import APIRouter

from app.schemas.users_schema import UserSchema
from app.repository.users import RepositoryUsers
from app.utils.config import config_session_maker

from app.utils.crypto import fake_hash_password

authRouter = APIRouter(prefix="")
# если префикс указать другой, то авторизация как то не работает
# хз почему, так надо почитать чужие проекты и в доке написано много интересного


app = authRouter


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


def get_user(username) -> UserSchema:
    repository_users = RepositoryUsers(session=config_session_maker())
    user = repository_users.get_user_by_username(username)
    print("user1", user)
    if user:
        return user


def fake_decode_token(token):
    user = get_user(token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    print("Token:", token)
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    repository_users = RepositoryUsers(session=config_session_maker())
    user_dict = repository_users.get_user_by_username(form_data.username).model_dump(exclude_none=True)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserSchema(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    repository_users = RepositoryUsers(session=config_session_maker())
    repository_users.set_user_active(id=user_dict["id"])

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    return current_user

@app.post("/users/create_account")
def create_account(user: UserSchema):
    # в форму передаёшь обычный пароль, на сервере он хэшируется
    repository_users = RepositoryUsers(session=config_session_maker())
    repository_users.create_user(user)
    return user

@app.post("/users/change_user")
def change_user(user: UserSchema, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    repository_users = RepositoryUsers(session=config_session_maker())
    if not(repository_users.get_user_by_id(id=user.id)):
        raise HTTPException(status_code=403, detail="Пользователя с таким id не существует")
    if current_user.username != user.username:
        print(repository_users.get_user_by_username(user.username), "log123")
        if repository_users.get_user_by_username(user.username):
            raise HTTPException(status_code=403, detail="Пользователя с таким именем уже существует")
    user.hashed_password = fake_hash_password(user.hashed_password)
    repository_users.change_user(user)
    return user


@app.post("/users/delete_user")
def delete_user(user_id: int, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    repository_users = RepositoryUsers(session=config_session_maker())
    repository_users.delete_user(user_id)
    return "Пользователь удалён"

