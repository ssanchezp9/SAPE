import os 
from dotenv import load_dotenv

def load_dsn() -> str:
    load_dotenv()
    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

    user: str = os.getenv("POSTGRES_USER")
    password: str = os.getenv("POSTGRES_PASSWORD")
    host: str = os.getenv("POSTGRES_HOST")
    port: str = os.getenv("POSTGRES_PORT")
    database: str = os.getenv("POSTGRES_DB")

    dsn: str = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    return dsn