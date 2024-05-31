from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.base import Base
from app.settings import DATABASE_URL

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db/microblog"

engine = create_engine(DATABASE_URL)
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = SessionLocal()
    try:
        if db.query(models.User).count() == 0:
            users = [
                models.User(name='Test', api_key='test'),
                models.User(name='Michail', api_key='misha'),
                models.User(name='Alexey', api_key='lesha')
            ]
            db.add_all(users)
            db.commit()
    finally:
        db.close()
