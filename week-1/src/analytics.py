from engine import engine

taxi_trips_table = "yellow_taxi_trips"
zone_lookup_table = "taxi_zone_lookup"
datetime_format = "yyyy-MM-dd HH24:mm:ss"

# ALTER TABLE yellow_taxi_trips ALTER COLUMN lpep_dropoff_datetime TYPE DATE
# using TO_TIMESTAMP(lpep_dropoff_datetime, 'YYYY-MM-dd HH24:MI:SS');
# lpep_pickup_datetime = 15th Jan
# res = engine.execute(
#     f"SELECT count(*) FROM {taxi_trips_table} WHERE \
#     EXTRACT(MONTH FROM lpep_pickup_datetime) = 1 AND \
#     EXTRACT(DAY FROM lpep_pickup_datetime) = 15 AND \
#     EXTRACT(DAY FROM lpep_dropoff_datetime) = 15"
# )
# print(list(res))

# # lpep_pickup_datetime for max(trip_distance)
# res = engine.execute(
#     f"SELECT lpep_pickup_datetime FROM {taxi_trips_table} WHERE \
#     trip_distance=(select max(trip_distance) from {taxi_trips_table})"
# )
# print(list(res))
# # # In lpep_pickup_datetime == 2019-01-01 find count(trips) passenger_count=2 or 3?
# res = engine.execute(
#     f"select count(*) from {taxi_trips_table} where \
# (passenger_count = 2 OR passenger_count = 3) AND lpep_pickup_datetime::date = '2019-01-01' \
# group by passenger_count;"
# )
# print(list(res))

# # PULocationID = "Astoria Zone" find largest tip(DOLocationID)


# res = engine.execute(
#     f"""
#     select dz, max(t2.tip_sum) as mts from
#         (select dz,  sum(tip_amount) as tip_sum from (
#             select t.tip_amount, zpu."Zone" as pz, zdo."Zone" as dz
#             from
#                 {taxi_trips_table} t,
#                 {zone_lookup_table} lu,
#                 {zone_lookup_table} zdo
#             where
#                 t."PULocationID" = zpu."LocationID" AND
#                 t."DOLocationID" = zdo."LocationID"
#         ) t1 where pz = 'Astoria' group by dz
#     ) t2
#     group by dz order by max(t2.tip_sum) DESC LIMIT 2

#     """.strip()
# )
# print(list(res))

print(
    f"""
    select dz, max(t1.tip_sum) as mts from 
        (select t."DOLocationID" as dz, sum(tip_amount) as tip_sum from  
                {taxi_trips_table} t
            where "PULocationID" = 7 group by "DOLocationID"
        ) t1 
        group by dz order by max(t1.tip_sum) DESC LIMIT 2

    """
)
res = engine.execute(
    f"""
    select dz, max(t1.tip_sum) as mts from 
        (select t."DOLocationID" as dz, sum(total_amount) as tip_sum from  
                {taxi_trips_table} t
            where "PULocationID" = 7 group by "DOLocationID"
        ) t1 
        group by dz order by max(t1.tip_sum) DESC LIMIT 2

    """.strip()
)
print(list(res))
