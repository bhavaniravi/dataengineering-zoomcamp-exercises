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
for df in pd.read_csv(url, compression="infer", chunksize=chunksize):
    print("Writing to sql")
    df.to_sql(
        name=table_name,
        con=engine,
        index=False,
        if_exists="append",
        dtype={
            "tpep_pickup_datetime": DateTime(),
            "tpep_dropoff_datetime": DateTime(),
            "lpep_pickup_datetime": DateTime(),
            "lpep_dropoff_datetime": DateTime(),
        },
    )
