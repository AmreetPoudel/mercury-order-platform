import time
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

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

SessionLocal = sessionmaker(bind=engine)