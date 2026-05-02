from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import time
import redis
import json

from apps.common.state import ORDERS_DB  # DB can stay for now

r = redis.Redis(host="redis", port=6379, decode_responses=True)

app = FastAPI()


class Order(BaseModel):
    item: str
    quantity: int


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.post("/orders")
def create_order(order: Order):
    order_id = str(uuid.uuid4())

    job = {
        "order_id": order_id,
        "item": order.item,
        "quantity": order.quantity,
        "created_at": time.time()
    }

    # 1. DB write (source of truth)
    ORDERS_DB[order_id] = {
        "status": "queued",
        "item": order.item,
        "quantity": order.quantity,
        "created_at": job["created_at"],
        "updated_at": job["created_at"]
    }

    # 2. PUSH TO REDIS (THIS IS THE QUEUE NOW)
    r.lpush("orders", json.dumps(job))

    print(f"[API] queued order: {order_id}")

    return {
        "order_id": order_id,
        "status": "queued"
    }


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    return ORDERS_DB.get(order_id, {"error": "not found"})