import redis
import json
import time
from apps.common.state import ORDERS_DB

r = redis.Redis(host="redis", port=6379, decode_responses=True)

print("[WORKER] started")

while True:
    _, raw = r.brpop("orders")  # blocking call
    job = json.loads(raw)

    order_id = job["order_id"]

    print(f"[WORKER] processing {order_id}")

    # simulate work
    time.sleep(2)

    ORDERS_DB[order_id]["status"] = "completed"
    ORDERS_DB[order_id]["updated_at"] = time.time()

    print(f"[WORKER] completed {order_id}")