from multiprocessing import Manager

manager = Manager()

# Shared queue
QUEUE = manager.list()

# Fake DB (temporary state)
ORDERS_DB = manager.dict()