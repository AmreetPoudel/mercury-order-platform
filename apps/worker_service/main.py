import redis
import json
import time

from apps.common.db import SessionLocal
from apps.common.models import Order as OrderModel

r = redis.Redis(host="redis", port=6379, decode_responses=True)

PROCESSING_TIMEOUT = 10
MAX_RETRIES = 3

print("[WORKER] started")


def recover_stuck_jobs():
    processing_jobs = r.lrange("orders:processing", 0, -1)

    for raw in processing_jobs:
        job = json.loads(raw)

        if job.get("processing_started_at"):
            age = time.time() - job["processing_started_at"]

            if age > PROCESSING_TIMEOUT:
                print(f"[RECOVERY] requeue stuck job {job['order_id']}")

                r.lrem("orders:processing", 1, raw)
                job["processing_started_at"] = None
                r.lpush("orders", json.dumps(job))


while True:
    # 🔁 recover stuck jobs
    recover_stuck_jobs()

    # 🔥 atomic move: queue → processing
    raw = r.brpoplpush("orders", "orders:processing")
    job = json.loads(raw)

    order_id = job["order_id"]

    db = SessionLocal()
    order = db.query(OrderModel).filter_by(order_id=order_id).first()

    if not order:
        print(f"[WARN] order not found: {order_id}")
        r.lrem("orders:processing", 1, raw)
        continue

    # 🧠 idempotency
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

        # 🔥 simulate failure condition (you can toggle this)
        # if job["retry_count"] < 2:
        #     raise Exception("simulated failure")

        time.sleep(2)

        # success
        order.status = "completed"
        order.updated_at = time.time()
        db.commit()

        print(f"[WORKER] completed {order_id}")

        # ✅ ACK
        r.lrem("orders:processing", 1, json.dumps(job))

    except Exception as e:
        print(f"[ERROR] {order_id} failed: {e}")

        # 🔁 retry logic
        job["retry_count"] += 1

        if job["retry_count"] <= MAX_RETRIES:
            print(f"[RETRY] {order_id} attempt {job['retry_count']}")

            r.lrem("orders:processing", 1, raw)
            job["processing_started_at"] = None
            r.lpush("orders", json.dumps(job))

        else:
            print(f"[DLQ] {order_id} moved to dead letter queue")

            r.lrem("orders:processing", 1, raw)
            r.lpush("orders:dlq", json.dumps(job))

            order.status = "failed"
            db.commit()