NYC Dataset
https://www.kaggle.com/c/nyc-taxi-trip-duration/data

Generate your CSV
```
head -n1000 dataset.csv > small.csv
```

Generate a subset of train.csv taking random samples from the dataset
```
tail -n +2 nyc_taxi_train_dataset.csv | gshuf -n 100000 > processed.csv
head -n1 nyc_taxi_train_dataset.csv | cat - processed.csv > temp && mv temp processed.csv
```

# Set up routing on docker
```
docker run -t -v $(pwd):/data osrm/osrm-backend osrm-extract -p /opt/car.lua /data/new-york-latest.osm.pbf
docker run -t -v $(pwd):/data osrm/osrm-backend osrm-partition /data/new-york-latest.osm.pbf
docker run -t -v $(pwd):/data osrm/osrm-backend osrm-customize /data/new-york-latest.osm.pbf
docker run -t -i -p 5000:5000 -v $(pwd):/data osrm/osrm-backend osrm-routed --algorithm mld /data/new-york-latest.osm.pbf
```