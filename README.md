# CZ/CE4032 DATA ANALYTICS & MINING
## Group 32 - Group Members
- TAN JUN XIANG (U1521529C)
- NEO JIA JUN (U1522507E)
- GOH WAN CHIN (U1522065L)
- GUO WEI (U1520604K)
- LIU ZHIWEI (U1520546E)

## Dataset URL
New York City Taxi Trip Duration Prediction  
https://www.kaggle.com/c/nyc-taxi-trip-duration


# Generate Visualizations
This script generates graphs that were used for analyzing the dataset.

Files Required: train.csv
```
python visualization.py
```

# Data Cleaning & Feature Engineering
This script takes cleans and generates new features and saves it into a new file.

Dependencies: [Routing Application](#setting-up-routing-application) must be running 
File Required: train.csv
File Output: processed_train.csv
```
python feature_engineering.py
```

# Creating Models

Adding Scripts from JJ

# Setting up Routing Application
This application uses the Open Source Routing Machine (OSRM) docker container that finds the shortest travel distance for cars between two points. 

1. Download OpenStreetMap Data from New York from: http://download.geofabrik.de/north-america/us/new-york.html
2. Download `new-york-latest.osm.pbf` and put into `./data/new-york-latest.osm.pbf`
3. Run the following Docker Command to start the server
```
docker run -t -v $(pwd):/data osrm/osrm-backend osrm-extract -p /opt/car.lua /data/new-york-latest.osm.pbf
docker run -t -v $(pwd):/data osrm/osrm-backend osrm-partition /data/new-york-latest.osm.pbf
docker run -t -v $(pwd):/data osrm/osrm-backend osrm-customize /data/new-york-latest.osm.pbf
docker run -t -i -p 5000:5000 -v $(pwd):/data osrm/osrm-backend osrm-routed --algorithm mld /data/new-york-latest.osm.pbf
```
