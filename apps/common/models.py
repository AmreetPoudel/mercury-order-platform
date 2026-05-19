from sqlalchemy import Column, String, Integer, Float
from apps.common.db import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    item = Column(String)
    quantity = Column(Integer)
    status = Column(String)

    created_at = Column(Float)
    updated_at = Column(Float)