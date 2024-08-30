import uvicorn
from fastapi import FastAPI
from uvicorn import run
from api.cards import cardsRouter
from contextlib import asynccontextmanager
from models.models import AbstractModel
from utils.config import config_session_maker, config_engine
from api.auth import authRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    AbstractModel.metadata.create_all(config_engine)
    yield
    # Clean up the ML models and release the resources

app = FastAPI(lifespan=lifespan)

app.include_router(cardsRouter, tags=["Cards"])
app.include_router(authRouter, tags=["Auth"])


run(app, host="localhost")
