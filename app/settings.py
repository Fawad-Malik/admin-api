from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi_sqlalchemy import db
import os 
from dotenv import load_dotenv
load_dotenv()
DB_HOSTNAME = os.getenv("DB_URL")
DB_USER = os.getenv("DB_USER")
DB_PW = os.getenv("DB_PW")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


MYSQL_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(DB_USER, DB_PW, DB_HOSTNAME, DB_PORT, DB_NAME)
engine = create_engine(
    MYSQL_DATABASE_URI, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
