from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import time
import redis
import json

from apps.common.db import SessionLocal
from apps.common.models import Order as OrderModel

r = redis.Redis(host="redis", port=6379, decode_responses=True)

app = FastAPI()


class Order(BaseModel):
    item: str
    quantity: int


@app.on_event("startup")
def startup():
    from apps.common.db import engine
    from apps.common.models import Base
    Base.metadata.create_all(bind=engine)


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.post("/orders")
def create_order(order: Order):
    db = SessionLocal()

    order_id = str(uuid.uuid4())
    now = time.time()

    # 1. write DB
    db_order = OrderModel(
        order_id=order_id,
        item=order.item,
        quantity=order.quantity,
        status="queued",
        created_at=now,
        updated_at=now
    )

    db.add(db_order)
    db.commit()

    # 2. push to Redis
    job = {"order_id": order_id}
    r.lpush("orders", json.dumps(job))

    return {"order_id": order_id, "status": "queued"}


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    db = SessionLocal()

    order = db.query(OrderModel).filter_by(order_id=order_id).first()

    if not order:
        return {"error": "not found"}

    return {
        "order_id": order.order_id,
        "status": order.status,
        "item": order.item,
        "quantity": order.quantity
    }