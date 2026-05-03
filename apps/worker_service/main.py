import redis
import json
import time

from apps.common.db import SessionLocal
from apps.common.models import Order as OrderModel

r = redis.Redis(host="redis", port=6379, decode_responses=True)

print("[WORKER] started")

while True:
    _, raw = r.brpop("orders")
    job = json.loads(raw)

    order_id = job["order_id"]

    db = SessionLocal()

    order = db.query(OrderModel).filter_by(order_id=order_id).first()

    if not order:
        print(f"[WARN] order not found: {order_id}")
        continue

    # 🔁 idempotency check
    if order.status == "completed":
        print(f"[SKIP] already completed: {order_id}")
        continue

    print(f"[WORKER] processing {order_id}")

    try:
        # mark processing
        order.status = "processing"
        db.commit()

        # simulate work
        time.sleep(2)

        # mark completed
        order.status = "completed"
        order.updated_at = time.time()
        db.commit()

        print(f"[WORKER] completed {order_id}")

    except Exception as e:
        print(f"[ERROR] {e}")
        order.status = "failed"
        db.commit()