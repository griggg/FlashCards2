from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi import APIRouter

from schemas.users_schema import UserSchema
from repository.users import RepositoryUsers
from utils.config import config_session

from utils.crypto import fake_hash_password

authRouter = APIRouter(prefix="")

app = authRouter

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(username) -> UserSchema:
    repository_users = RepositoryUsers(session=config_session)
    user = repository_users.get_user_by_username(username)
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


@app.post("/token", response_model=dict)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    repository_users = RepositoryUsers(session=config_session)
    user: UserSchema | None = repository_users.get_user_by_username(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    repository_users = RepositoryUsers(session=config_session)
    repository_users.set_user_active(id=user.id)

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me", response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    return current_user

@app.post("/users/create_account", response_model=UserSchema)
def create_account(user: UserSchema):
    # в форму передаёшь обычный пароль, на сервере он хэшируется
    repository_users = RepositoryUsers(session=config_session)
    if repository_users.get_user_by_id(user.id):
        raise HTTPException(status_code=403, detail="Пользователь с таким id уже есть")

    repository_users.create_user(user)
    return user

@app.post("/users/change_user", response_model=UserSchema)
def change_user(user: UserSchema, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    repository_users = RepositoryUsers(session=config_session)
    if not(repository_users.get_user_by_id(id=user.id)):
        raise HTTPException(status_code=400, detail="Пользователя с таким id не существует")
    if current_user.username != user.username:
        if repository_users.get_user_by_username(user.username):
            raise HTTPException(status_code=403, detail="Пользователь с таким именем уже существует")
    user.hashed_password = fake_hash_password(user.hashed_password)
    repository_users.change_user(user)
    return user


@app.post("/users/delete_user", response_model=str)
def delete_user(user_id: int, current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    repository_users = RepositoryUsers(session=config_session)

    if user_id != current_user.id:
        return HTTPException(status_code=403, detail="Невозможно удалить аккаунт другого пользователя")
    repository_users.delete_user(user_id)
    return "Пользователь удалён"

