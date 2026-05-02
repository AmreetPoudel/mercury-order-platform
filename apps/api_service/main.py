from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import time

from apps.common.state import QUEUE, ORDERS_DB

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

    # 1. write DB (source of truth)
    ORDERS_DB[order_id] = {
        "status": "queued",
        "item": order.item,
        "quantity": order.quantity,
        "created_at": job["created_at"],
        "updated_at": job["created_at"]
    }

    # 2. push to queue
    QUEUE.append(job)

    print(f"[API] queued order: {order_id}")

    return {
        "order_id": order_id,
        "status": "queued"
    }


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    return ORDERS_DB.get(order_id, {"error": "not found"})


@app.get("/debug/queue")
def debug_queue():
    return {
        "queue_size": len(QUEUE),
        "items": QUEUE
    }