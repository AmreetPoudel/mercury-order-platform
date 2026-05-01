from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import time

from common.queue import QUEUE, ORDERS_DB

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
        "created_at": time.time(),
    }

    # Save initial state
    ORDERS_DB[order_id] = {
        "status": "queued",
        "item": order.item,
        "quantity": order.quantity,
    }

    # Push to queue
    QUEUE.append(job)

    print(f"[API] Order queued: {job}")

    return {
        "order_id": order_id,
        "status": "queued"
    }


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = ORDERS_DB.get(order_id)

    if not order:
        return {"error": "not found"}

    return order