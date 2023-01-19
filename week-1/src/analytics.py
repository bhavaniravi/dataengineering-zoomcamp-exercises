from engine import engine

taxi_trips_table = "yellow_taxi_trips"
zone_lookup_table = "taxi_zone_lookup"
datetime_format = "yyyy-MM-dd HH24:mm:ss"


# lpep_pickup_datetime = 15th Jan
res = engine.execute(
    f"SELECT count(*) FROM {taxi_trips_table} WHERE \
    EXTRACT(MONTH FROM lpep_pickup_datetime) = 1 AND \
    EXTRACT(DAY FROM lpep_pickup_datetime) = 15 AND \
    EXTRACT(DAY FROM lpep_dropoff_datetime) = 15"
)
print(list(res))

# lpep_pickup_datetime for max(trip_distance)
res = engine.execute(
    f"SELECT lpep_pickup_datetime FROM {taxi_trips_table} WHERE \
    trip_distance=(select max(trip_distance) from {taxi_trips_table})"
)
print(list(res))


# In lpep_pickup_datetime == 2019-01-01 find count(trips) passenger_count=2 or 3?
res = engine.execute(
    f"select count(*) from {taxi_trips_table} where \
(passenger_count = 2 OR passenger_count = 3) AND lpep_pickup_datetime::date = '2019-01-01' \
group by passenger_count;"
)
print(list(res))

# PULocationID = "Astoria Zone" find largest tip(DOLocationID)


res = engine.execute(
    f"""
    select tip_amount, pz, dz from (
        select t.tip_amount, zpu."Zone" as pz, zdo."Zone" as dz
        from
            {taxi_trips_table} t,
            {zone_lookup_table} zpu,
            {zone_lookup_table} zdo
        where
            t."PULocationID" = zpu."LocationID" AND
            t."DOLocationID" = zdo."LocationID" 
    ) t1 where t1.pz='Astoria' order by tip_amount desc LIMIT 1

    """.strip()
)
print(list(res))
