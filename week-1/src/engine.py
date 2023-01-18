from dotenv import load_dotenv
import os

load_dotenv()
from sqlalchemy import create_engine

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ.get("POSTGRES_HOST", "")
db = os.environ["POSTGRES_DB"]
port = os.environ.get("POSTGRES_PORT", "5432")
db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
print("connecting to ", db_url)
engine = create_engine(db_url)
