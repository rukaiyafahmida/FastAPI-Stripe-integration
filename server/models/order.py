from sqlalchemy import Column, ForeignKey, Integer, Float, String
from decouple import config
from sqlalchemy.orm import relationship
from config.db import Base


class Orders(Base):
    __tablename__ = config("ORDER_TABLE")

    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String)
    posted_at = Column(Float)
    transacted_at = Column(Float)
    updated_at = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    users = relationship("Users", back_populates=config("ORDER_TABLE"), lazy="joined")
