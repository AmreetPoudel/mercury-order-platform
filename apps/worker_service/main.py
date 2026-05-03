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
## here we are updating the DB directly, but in a real system, we would have a separate service for this so try block 
#is just to avoid crashing the worker if the order is not found in the DB, which can happen if the API service is 
#restarted and loses its in-memory state. In a real system, we would have a persistent database that both services can 
#access, so this issue would not occur.
## still crashing but we are leaving it here 
    try:
        ORDERS_DB[order_id]["status"] = "completed"
    except KeyError:
        print(f"[WARN] order not found in DB: {order_id}")
    ORDERS_DB[order_id]["updated_at"] = time.time()

    print(f"[WORKER] completed {order_id}")


