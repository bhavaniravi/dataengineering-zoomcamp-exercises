# Week 1

- Taking inspiration from the project repo and giving my spin to it
- I have worked with Python, Docker, Kubernetes for last 4 years, taking the course to fill in the gaps

### Download Data

```
cd week-1
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz -P data/
gunzip data/*
```

The `-p data` will write it to data folder

### Creating a Docker-Compose file

1. Created two services one for postgres and another for the pipeline
2. Used docker-compose common environment variable param to pass the env variables.
3. Right now everything under the `ingestion` service is an assumption.

## Python Files

- Created two files `ingestion.py` and `analytics.py`
- `ingestion.py` will move the data and `analytics.py` will be used to run queries
- Created a centralized file call engine.py to be used by both analytics and ingestion.

## Ingestion script

- The zoomcamp script was chunking the df transforming and then ingesting
- Instead I took the route to use `chunksize` and `dtype` parameters

## Using Poetry

```
poetry init #initializes 
poetry add <library-name> 
```
## Generating Requirements file

When creating Dockerfile I realized I need a requirements file that's week specific. Since poetry is at the whole project level, I decided to generate `requirements.txt` file

```
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

## Building Docker Image

```
docker build -t ny_taxi .  
```

## Entrypoint 

- The entrypoint to the docker image is a bash script which will decide whether to run ingestion or analytics
- `entrypoint.sh` is inspired from Airflow Docker-compose setup where it is used to start different components of Airflow 

```
bash entrypoint.sh ingestion 
```