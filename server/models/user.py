from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
)
from decouple import config
from config.db import Base


class Users(Base):
    __tablename__ = config("USER_TABLE")

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    user_email = Column(String)
    created_at = Column(Float)
    last_updated_at = Column(Float)
