from sqlalchemy import Boolean, Column, ForeignKey, Numeric, Integer, String
from sqlalchemy.types import Date
from database import Base


class State(Base):
    __tablename__ = "state"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, index=True)
    country_code = Column(String)
    population = Column(Integer)
    last_updated = Column(String)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)



