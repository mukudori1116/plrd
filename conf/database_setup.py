from sqlalchemy import Column, Integer, String, Float
from conf.setting import Base


class MTSData(Base):
    __tablename__ = 'mts'

    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    cell = Column(String)
    plate = Column(String)
    well_id = Column(Integer, nullable=False)
    well = Column(Float)


class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    file_name = Column(String)
