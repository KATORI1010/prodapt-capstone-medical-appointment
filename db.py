from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import settings

engine = create_engine(str(settings.DATABASE_URL), echo=True)


def get_db_session():
    return sessionmaker(bind=engine)()


def get_db():
    engine = create_engine(str(settings.DATABASE_URL), echo=not settings.PRODUCTION)
    db = sessionmaker(bind=engine)()
    try:
        yield db
    finally:
        db.close()
