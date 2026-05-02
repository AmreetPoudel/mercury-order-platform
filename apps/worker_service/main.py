import time
import random

from apps.common.state import QUEUE, ORDERS_DB


def process_job(job):
    order_id = job["order_id"]

    print(f"[WORKER] picked: {order_id}")

    # mark processing
    ORDERS_DB[order_id]["status"] = "processing"
    ORDERS_DB[order_id]["updated_at"] = time.time()

    time.sleep(2)

    # simulate failure
    if random.random() < 0.2:
        ORDERS_DB[order_id]["status"] = "failed"
        ORDERS_DB[order_id]["updated_at"] = time.time()
        print(f"[WORKER] failed: {order_id}")
        return

    ORDERS_DB[order_id]["status"] = "completed"
    ORDERS_DB[order_id]["updated_at"] = time.time()

    print(f"[WORKER] completed: {order_id}")


def worker_loop():
    print("[WORKER] started")

    while True:
        if len(QUEUE) > 0:
            job = QUEUE.pop(0)
            process_job(job)
        else:
            time.sleep(3)


if __name__ == "__main__":
    worker_loop()