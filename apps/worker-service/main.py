import time
import random

from common.queue import QUEUE, ORDERS_DB


def process_job(job):
    order_id = job["order_id"]

    print(f"[WORKER] Processing order: {order_id}")

    # Simulate processing time
    time.sleep(2)

    # Simulate random failure
    if random.random() < 0.2:
        print(f"[WORKER] Failed processing: {order_id}")
        ORDERS_DB[order_id]["status"] = "failed"
        return

    # Success path
    ORDERS_DB[order_id]["status"] = "completed"

    print(f"[WORKER] Completed order: {order_id}")


def worker():
    print("[WORKER] Started")

    while True:
        if len(QUEUE) > 0:
            job = QUEUE.pop(0)
            process_job(job)
        else:
            time.sleep(1)


if __name__ == "__main__":
    worker()