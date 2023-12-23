from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class Musik(Base):
    __tablename__ = "musik"
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    description = Column(Text)
    year = Column(Integer)
