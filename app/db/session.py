import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()
engine = sqlalchemy.create_engine(os.getenv("DATABASE_URL"))
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = session() #создаем конкретную сессию
    try:
        yield db
    finally:
        db.close() # после использования закрываем