from .base import Base
from .asset_type import AssetType

from sqlalchemy import Column, Integer, String, Date, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship

tablename = 'trades'


class Trades(Base):
    __tablename__ = tablename

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String)
    quantity = Column(Float)
    date = Column(Date, nullable=False, primary_key=True)
    price = Column(Float)
    type = Column(Enum(AssetType))
    lot_id = Column(Integer, ForeignKey('lots.id'))
    lot = relationship("Lots")


# https://docs.timescale.com/api/latest/hypertable/create_hypertable/#optional-arguments
hypertable = f"SELECT create_hypertable('{tablename}', 'date');"
