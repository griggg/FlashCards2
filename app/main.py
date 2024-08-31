import uvicorn
from fastapi import FastAPI
from uvicorn import run
from app.api.cards import cardsRouter
from contextlib import asynccontextmanager
from app.models.models import AbstractModel
from app.utils.config import config_session_maker, config_engine
from app.api.auth import authRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    AbstractModel.metadata.create_all(config_engine)
    yield
    # Clean up the ML models and release the resources

app = FastAPI(lifespan=lifespan)

app.include_router(cardsRouter, tags=["Cards"])
app.include_router(authRouter, tags=["Auth"])


if __name__ == '__main__':

    run(app, host="localhost")
