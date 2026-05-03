import redis
import json
import time

from apps.common.db import SessionLocal
from apps.common.models import Order as OrderModel

r = redis.Redis(host="redis", port=6379, decode_responses=True)

PROCESSING_TIMEOUT = 10  # seconds

print("[WORKER] started")


def recover_stuck_jobs():
    processing_jobs = r.lrange("orders:processing", 0, -1)

    for raw in processing_jobs:
        job = json.loads(raw)

        if job.get("processing_started_at"):
            age = time.time() - job["processing_started_at"]

            if age > PROCESSING_TIMEOUT:
                print(f"[RECOVERY] requeueing stuck job {job['order_id']}")

                r.lrem("orders:processing", 1, raw)
                job["processing_started_at"] = None
                r.lpush("orders", json.dumps(job))


while True:
    # 🔥 Step 1: recover stuck jobs first
    recover_stuck_jobs()

    # 🔥 Step 2: safely pull job
    raw = r.brpoplpush("orders", "orders:processing")
    job = json.loads(raw)

    order_id = job["order_id"]

    db = SessionLocal()
    order = db.query(OrderModel).filter_by(order_id=order_id).first()

    if not order:
        print(f"[WARN] order not found: {order_id}")
        r.lrem("orders:processing", 1, raw)
        continue

    # 🧠 idempotency check
    if order.status == "completed":
        print(f"[SKIP] already completed: {order_id}")
        r.lrem("orders:processing", 1, raw)
        continue

    print(f"[WORKER] processing {order_id}")

    try:
        # mark processing
        order.status = "processing"
        db.commit()

        # update job timestamp
        job["processing_started_at"] = time.time()

        # update Redis copy
        r.lrem("orders:processing", 1, raw)
        r.lpush("orders:processing", json.dumps(job))

        # simulate work
        time.sleep(2)

        # mark completed
        order.status = "completed"
        order.updated_at = time.time()
        db.commit()

        print(f"[WORKER] completed {order_id}")

        # ✅ ACK (remove from processing queue)
        r.lrem("orders:processing", 1, json.dumps(job))

    except Exception as e:
        print(f"[ERROR] {e}")
        # ❌ do NOT remove → recovery will handle