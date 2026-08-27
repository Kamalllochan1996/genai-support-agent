from app.db.database import Base, engine
from app.db.models import Conversation


def init_db():
    Base.metadata.create_all(
        bind=engine
    )