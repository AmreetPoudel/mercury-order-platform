from apps.common.db import Base, engine
from apps.common.models import Order

Base.metadata.create_all(bind=engine)

print("DB tables created successfully")