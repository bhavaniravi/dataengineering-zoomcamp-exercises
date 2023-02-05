from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_aws.s3 import S3Bucket
import psycopg2
import redshift_connector
import os
from prefect_aws import AwsCredentials
from redshift_auto_schema import RedshiftAutoSchema


aws_credentials_block = AwsCredentials.load("aws-access")
aws_access_key_id = aws_credentials_block.aws_access_key_id
aws_access_secret = aws_credentials_block.aws_secret_access_key

aws_access_secret = os.environ["AWS_SECRET_KEY"]


@task(retries=3)
def extract_from_s3(s3_path, filename) -> Path:
    """Download trip data from GCS"""
    gcs_block = S3Bucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=s3_path, local_path=f"../data/")
    return Path(f"../data/{s3_path}/{filename}")


@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    df["passenger_count"].fillna(0, inplace=True)
    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    df.to_csv(path, index=False)
    return path


@task()
def delete_table():
    conn = psycopg2.connect(
        dbname="trips_data_all",
        host="tf-redshift-cluster.cjb8qoyj6zhx.us-east-1.redshift.amazonaws.com",
        port=5439,
        user="exampleuser",
        password="examplePass1",
    )
    with conn as conn:

        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS trip_data")


@task()
def write_redshift(s3_path: Path) -> None:
    # s3://dtc-data-lake/data/yellow/yellow_tripdata_2021-01.parquet
    """Write CSV to Redshfit"""
    print(s3_path)
    conn = psycopg2.connect(
        dbname="trips_data_all",
        host="tf-redshift-cluster.cjb8qoyj6zhx.us-east-1.redshift.amazonaws.com",
        port=5439,
        user="exampleuser",
        password="examplePass1",
    )
    with conn as conn:

        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS trip_data")
            cur.execute(
                """CREATE TABLE if not exists trip_data (
"VendorID" FLOAT8
, "tpep_pickup_datetime" timestamp
, "tpep_dropoff_datetime" timestamp
, "passenger_count" FLOAT8
, "trip_distance" FLOAT8
, "RatecodeID" FLOAT8
, "store_and_fwd_flag" varchar(256)
, "PULocationID" BIGINT
, "DOLocationID" BIGINT
, "payment_type" FLOAT8
, "fare_amount" FLOAT8
, "extra" FLOAT8
, "mta_tax" FLOAT8
, "tip_amount" FLOAT8
, "tolls_amount" FLOAT8
, "improvement_surcharge" FLOAT8
, "total_amount" FLOAT8
, "congestion_surcharge" FLOAT8
);"""
            )

            # new_table = RedshiftAutoSchema(
            #     file="data/yellow/yellow_tripdata_2021-01.parquet",
            #     schema="public.trips_data_all",
            #     table="trip_data",
            #     conn=conn,
            # )
            # if not new_table.check_table_existence():
            #     ddl = new_table.generate_table_ddl()
            #     print(ddl)
            #     cur.execute(ddl)

            cur.execute(
                f"""copy trip_data from '{s3_path}'
credentials 'aws_access_key_id={aws_access_key_id};aws_secret_access_key={aws_access_secret}'
FORMAT AS PARQUET;"""
            )
            # Commit your transaction
            cur.execute("commit;")
        print("Copy executed fine!")


@task()
def count_redshift():
    conn = psycopg2.connect(
        dbname="trips_data_all",
        host="tf-redshift-cluster.cjb8qoyj6zhx.us-east-1.redshift.amazonaws.com",
        port=5439,
        user="exampleuser",
        password="examplePass1",
    )
    with conn as conn:
        with conn.cursor() as curr:
            res = curr.execute("select count(*) from trip_data")
            print(curr.fetchall())


@flow()
def etl_to_redshift(color, year, month):
    s3_bucket = "s3://dtc-data-lake"
    s3_path = f"{s3_bucket}/data/{color}/{color}_tripdata_{year}-{month:02}.parquet"

    write_redshift(s3_path)


@flow()
def etl_redshift_flow(
    months: list[int] = [1, 2], year: int = 2021, color: str = "yellow"
):
    delete_table()
    for month in months:
        etl_to_redshift(color=color, year=year, month=month)

    count_redshift()


if __name__ == "__main__":
    color = "yellow"
    months = [2, 3]
    year = 2021
    etl_redshift_flow(months, year, color)
