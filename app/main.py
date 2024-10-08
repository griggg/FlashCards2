import uvicorn
from fastapi import FastAPI
from uvicorn import run
from api.cards import cardsRouter
from contextlib import asynccontextmanager
from models.models import AbstractModel
from utils.config import config_engine
from api.auth import authRouter
from utils.config import APP_HOST

@asynccontextmanager
async def lifespan(app: FastAPI):
    AbstractModel.metadata.create_all(config_engine)
    yield
    # Clean up the ML models and release the resources


app = FastAPI(lifespan=lifespan)

app.include_router(cardsRouter, tags=["Cards"])
app.include_router(authRouter, tags=["Auth"])

if __name__ == '__main__':
    run(app, host=APP_HOST, port=8061)  # docker 0.0.0.0 | localhost
    # run(app, host="localhost", port=8061)  # localhost
