from models.base import Base

from sqlalchemy import Column, Integer, String, Date, Float

tablename = 'market'


class Market(Base):
    __tablename__ = tablename

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String)
    date = Column(Date, nullable=False, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Integer)


# https://docs.timescale.com/api/latest/hypertable/create_hypertable/#optional-arguments
hypertable = f"SELECT create_hypertable('{tablename}', 'date');"
