python3 -m venv venv
source venv/bin/activate
python script.py

# download data 
mkdir -p data/
cd data/
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz 
