from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True, index=True)
    item = Column(String)
    quantity = Column(Integer)
    status = Column(String)
    created_at = Column(Float)
    updated_at = Column(Float)