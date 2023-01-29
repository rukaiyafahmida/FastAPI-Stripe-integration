from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
)
from decouple import config
from config.db import Base


class Products(Base):
    __tablename__ = config("PRODUCT_TABLE")

    id = Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String)
    description = Column(String)
    images = Column(String)
    unit_label = Column(String)
    currency = Column(String)
    default_price = Column(Float)
    created = Column(Float)
    updated = Column(Float)
