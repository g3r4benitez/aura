import os
from sqlmodel import create_engine, Session, SQLModel

from app.models.conversation import Conversation

SQLALCHEMY_DATABASE_URL = os.environ.get("DB_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

