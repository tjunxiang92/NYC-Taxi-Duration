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


Generate your CSV
```
head -n1000 dataset.csv > small.csv
```

Generate a subset of train.csv taking random samples from the dataset
```
tail -n +2 nyc_taxi_train_dataset.csv | gshuf -n 100000 > processed.csv
head -n1 nyc_taxi_train_dataset.csv | cat - processed.csv > temp && mv temp processed.csv
```

# Setting up OSRM on docker
```
docker run -t -v $(pwd):/data osrm/osrm-backend osrm-extract -p /opt/car.lua /data/new-york-latest.osm.pbf
docker run -t -v $(pwd):/data osrm/osrm-backend osrm-partition /data/new-york-latest.osm.pbf
docker run -t -v $(pwd):/data osrm/osrm-backend osrm-customize /data/new-york-latest.osm.pbf
docker run -t -i -p 5000:5000 -v $(pwd):/data osrm/osrm-backend osrm-routed --algorithm mld /data/new-york-latest.osm.pbf
```
