from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MTSData(Base):
    __tablename__ = 'mts'

    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    cell = Column(String)
    plate = Column(String)
    well_id = Column(Integer, nullable=False)
    well = Column(Float)
