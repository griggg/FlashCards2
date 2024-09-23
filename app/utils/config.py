from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os


import redis

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DB_TEST_NAME = os.getenv("DB_TEST_NAME")
DB_TEST_USER = os.getenv("DB_TEST_USER")
DB_TEST_PASSWORD = os.getenv("DB_TEST_PASSWORD")
DB_TEST_HOST = os.getenv("DB_TEST_HOST")

APP_HOST = os.getenv("APP_HOST")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

MODE = "TEST"
# MODE = "PROD"
print(f"MODE DATABASE IS {MODE}")
if MODE == "TEST":
    # включать при разработке или запуске тестов
    url = f"postgresql://{DB_TEST_USER}:{DB_TEST_PASSWORD}@{DB_TEST_HOST}:5432/{DB_TEST_NAME}"
else:
    url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

# def make_engine():
#     return create_engine(url)
config_engine = create_engine(url)
config_session = sessionmaker(config_engine, autoflush=False, autocommit=False)()

def get_redis_con():
    redis_con = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    return redis_con