from sqlalchemy import Column, ForeignKey, Integer, Float
from decouple import config
from config.db import Base
from sqlalchemy.orm import relationship


class OrderDetails(Base):
    __tablename__ = config("ORDER_DETAIL_TABLE")

    id = Column(Integer, primary_key=True, nullable=False)
    quantity = Column(Integer)
    placed_at = Column(Float)
    updated_at = Column(Float)
    transacted_at = Column(Float)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    orders = relationship(
        "Orders", back_populates=config("ORDER_DETAIL_TABLE"), lazy="joined"
    )
    product = relationship(
        "Products", back_populates=config("ORDER_DETAIL_TABLE"), lazy="joined"
    )
