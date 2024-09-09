from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.secret import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{"db"}:5432/{DB_NAME}"


config_engine = create_engine(url)
config_session_maker = sessionmaker(config_engine, autoflush=False)
