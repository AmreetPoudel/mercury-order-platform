
import threading
import uvicorn

from apps.worker_service.main import worker_loop


def start_worker():
    worker_loop()


def start_api():
    uvicorn.run("apps.api_service.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    t = threading.Thread(target=start_worker)
    t.daemon = True
    t.start()

    start_api()