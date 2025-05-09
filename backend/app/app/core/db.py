import ssl
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings


_connect_args = {}
if settings.DB_CERT_PATH is not None and len(settings.DB_CERT_PATH) > 0:
    ssl_context = ssl.create_default_context(cafile=settings.DB_CERT_PATH)
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    _connect_args["ssl"] = ssl_context

_engine = create_engine(settings.DB_URL, connect_args=_connect_args)

def create_db():
    SQLModel.metadata.create_all(_engine)


def get_session():
    with Session(_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
