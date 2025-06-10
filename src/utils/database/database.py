from src.utils.database import dsn_loader
from psycopg_pool import NullConnectionPool

class Database:

    def __init__(self, max_size: int = 10):
        self.dsn: str = dsn_loader.load_dsn()
        self.pool = NullConnectionPool(
            conninfo=self.dsn, open=True, max_size=max_size
        )

    def get_connection(self):
        return self.pool.getconn()
    