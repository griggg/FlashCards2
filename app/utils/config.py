from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.secret import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"


configEngine = create_engine(url)
configSession = sessionmaker(configEngine, autoflush=False)
