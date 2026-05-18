import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://app:app@postgres:5432/orders"

Base = declarative_base()

engine = None

for i in range(15):
    try:
        print(f"[DB] attempt {i} connecting...")

        engine = create_engine(DATABASE_URL)

        conn = engine.connect()
        conn.close()

        print("[DB] connected")
        break

    except Exception as e:
        print(f"[DB] not ready yet: {e}")
        time.sleep(2)

if engine is None:
    raise Exception("FATAL: Database not reachable")

# Import models AFTER Base and engine exist
from apps.common.models import Order

# Create missing tables
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)