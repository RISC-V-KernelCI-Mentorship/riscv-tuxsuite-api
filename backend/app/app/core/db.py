from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings



_connect_args = {"check_same_thread": False}
_engine = create_engine(settings.DB_URL, connect_args=_connect_args)

def create_db():
    SQLModel.metadata.create_all(_engine)


def get_session():
    with Session(_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
