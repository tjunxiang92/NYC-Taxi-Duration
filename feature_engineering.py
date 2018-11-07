from datetime import datetime
from shapely.geometry import MultiPolygon, Polygon, Point
import geopy.distance
from poly import polygons
import pandas as pd
import json
import urllib.request
import matplotlib.pyplot as plt

# df = pd.read_csv('small.csv')
df = pd.read_csv('./data/train.csv')
# df = pd.read_csv('processed.csv')


# Remove rows with passenger count 0
df = df.drop(df[[int(x) == 0 for x in df['passenger_count']]].index)
# Remove rows with travel time larger than 21600(6 hours) or smaller than 10
df = df.drop(df[[int(x) > 21600 for x in df['trip_duration']]].index)
df = df.drop(df[[int(x) < 10 for x in df['trip_duration']]].index)
# Remove rows with longitude outside of range(-71,-76)
df = df.drop(df[[float(x) < -76 or float(x) > -71 for x in df['pickup_longitude']]].index)
df = df.drop(df[[float(x) < -76 or float(x) > -71 for x in df['dropoff_longitude']]].index)
# Remove rows with latitude outside of range(38, 43)
df = df.drop(df[[float(x) < 38 or float(x) > 43 for x in df['pickup_latitude']]].index)
df = df.drop(df[[float(x) < 38 or float(x) > 43 for x in df['dropoff_latitude']]].index)


# Get Day of the week, if it is peak timing, and what time is it in
def str_to_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


def get_hour(x):
    return str_to_datetime(x).hour


# Convert to categorical morning, afternoon, night, midnight
def get_timeofday(x):
    cat = str_to_datetime(x).hour // 6
    if cat == 0:
        return 'midnight'
    elif cat == 1:
        return 'morning'
    elif cat == 2:
        return 'afternoon'
    elif cat == 3:
        return 'night'


# Convert to is_peak - 7-9am, 5-8pm
def get_ispeak(x):
    hour = str_to_datetime(x).hour
    return (7 <= hour <= 9) or (16 <= hour <= 18)


# Convert to day of the week
def get_weekday(x):
    return str_to_datetime(x).weekday()


print("Processing Pickup & Dropoff")
df['pickup_hour'] = df['pickup_datetime'].map(get_hour)
df['pickup_timeofday'] = df['pickup_datetime'].map(get_timeofday)
df['pickup_ispeak'] = df['pickup_datetime'].map(get_ispeak)
df['pickup_day'] = df['pickup_datetime'].map(get_weekday)
print("Processing Pickup Done")

df['dropoff_hour'] = df['dropoff_datetime'].map(get_hour)
df['dropoff_hour'] = df['dropoff_datetime'].map(get_hour)
df['dropoff_timeofday'] = df['dropoff_datetime'].map(get_timeofday)
df['dropoff_ispeak'] = df['dropoff_datetime'].map(get_ispeak)
df['dropoff_day'] = df['dropoff_datetime'].map(get_weekday)
print("Processing Dropoff Done")


# Find which Borough the pickup and dropoff was from
def get_borough(x):
    point = Point(x[0], x[1])
    for name, polygon in polygons:
        if polygon.contains(point):
            return name

    return None


print("Processing Pickup, Dropoff Borough")
df["pickup_borough"] = df[["pickup_longitude", "pickup_latitude"]].apply(get_borough, axis=1)
print("Processing Pickup Borough Done")
df["dropoff_borough"] = df[["dropoff_longitude", "dropoff_latitude"]].apply(get_borough, axis=1)
print("Processing Dropoff Borough Done")


# Calculate Distance between pickup & dropoff in km
def get_distance(x):
    coords_1 = (x[0], x[1])
    coords_2 = (x[2], x[3])
    return round(geopy.distance.vincenty(coords_1, coords_2).meters)


df['distance'] = df[["pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude"]].apply(
    get_distance, axis=1)

print("Processing Distance")
df['distance'] = df[["pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude"]].apply(
    get_distance, axis=1)
print("Processing Distance Done")


# long1, lat1, long2, lat2
def get_car_distance(x):
    try:
        url = "http://127.0.0.1:5000/route/v1/driving/{},{};{},{}?steps=false&overview=false".format(
            x[0],
            x[1],
            x[2],
            x[3],
        )
        contents = urllib.request.urlopen(url).read()
        parsed_json = json.loads(contents)
        return parsed_json['routes'][0]['distance']
    except:
        print("Not Route Found {},{};{},{}".format(x[0], x[1], x[2], x[3]))
        return None


print("Processing Car Distance")
df['car_distance'] = df[["pickup_longitude", "pickup_latitude",
                         "dropoff_longitude", "dropoff_latitude"]].apply(get_car_distance, axis=1)
print("Processing Car Distance Done")

df.to_csv('processed_features.csv')
