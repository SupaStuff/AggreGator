from models.base import Base
from models.asset_type import AssetType

from sqlalchemy import Column, Integer, String, Date, Float, Enum
from sqlalchemy.orm import relationship


class Lots(Base):
    __tablename__ = 'lots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String)
    date = Column(Date)
    price = Column(Float)
    type = Column(Enum(AssetType))
    trades = relationship("Trades", single_parent=True)
