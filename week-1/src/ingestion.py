import pandas as pd
import os
from dotenv import load_dotenv

from engine import engine
from sqlalchemy.types import DateTime
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARN)
# import subprocess

load_dotenv()
url = os.environ["DATA_URL"]

table_name = os.environ["TABLE_NAME"]
chunksize = int(os.environ.get("CHUNK_SIZE", 1000))

print("Reading csv")
df = pd.read_csv(url, compression="infer")
# df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
# df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

# Instead of these above two lines I'm using chunk_size and dtype parameter

print("Writing to sql")
df.to_sql(
    name=table_name,
    con=engine,
    if_exists="replace",
    chunksize=chunksize,
    index=False,
    method="multi",
    dtype={"tpep_pickup_datetime": DateTime(), "tpep_dropoff_datetime": DateTime()},
)
