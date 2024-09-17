import uvicorn
from fastapi import FastAPI
from uvicorn import run
from api.cards import cardsRouter
from contextlib import asynccontextmanager
from models.models import AbstractModel
from utils.config import config_engine
from api.auth import authRouter
from api.link_maker import link_maker

@asynccontextmanager
async def lifespan(app: FastAPI):
    AbstractModel.metadata.create_all(config_engine)
    yield
    # Clean up the ML models and release the resources

app = FastAPI(lifespan=lifespan)

app.include_router(cardsRouter, tags=["Cards"])
app.include_router(authRouter, tags=["Auth"])
app.include_router(link_maker, tags=["LinkMaker"])


if __name__ == '__main__':

    run(app, host="0.0.0.0", port=8061)  # docker
    # run(app, host="localhost", port=8061)  # localhost
