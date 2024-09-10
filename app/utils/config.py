from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.secret import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_TEST_NAME

MODE = "TEST"
# MODE = "PROD"
print(f"MODE DATABASE IS {MODE}")
if MODE == "TEST":
    url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_TEST_NAME}"
else:
    url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"


# def make_engine():
#     return create_engine(url)
config_engine = create_engine(url)
config_session = sessionmaker(config_engine, autoflush=False, autocommit=False)()
