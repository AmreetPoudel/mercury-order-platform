from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://app:app@postgres:5432/orders"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)