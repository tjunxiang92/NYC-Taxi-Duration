# CZ/CE4032 DATA ANALYTICS & MINING
## Group 32 - Group Members
- TAN JUN XIANG (U1521529C)
- NEO JIA JUN (U1522507E)
- GOH WAN CHIN (U1522065L)
- GUO WEI (U1520604K)
- LIU ZHIWEI (U1520546E)

# Table of Contents
- [Dataset URL](#dataset-url)
- [Generate Visualizations](#generate-visualizations)
- [Data Cleaning & Feature Engineering](#data-cleaning--feature-engineering)
- [Training Models](#training-models)
- [Setting up Routing Application](#setting-up-routing-application)


# Dataset URL
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
Files Required:
* train.csv
* test.csv

Files Output:
* processed_train.csv
* processed_test.csv
```
python feature_engineering.py
```

# Training Models

Please make sure that you have anaconda install / jupyter notebook available since the code base is currently in a .ipynb file which is basically a jupyter notebook file. After installing, just type in the command:

Files Required: 
* processed_train.csv
* processed_test.csv
* train.csv 
* test.csv

Files Output: 
* nyc_kaggle_xgboost_top5_feature.csv
* nyc_kaggle_linear_regression_no_feature.csv
* nyc_kaggle_xgboost_no_feature.csv
* nyc_random_forest_no_feature.csv
* nyc_kaggle_xgboost.csv
* nyc_kaggle_linear_regression.csv
* nyc_kaggle_random_forest.csv

```
jupyter notebook 
```

Then go into the model_creation model, and thereafter click the Model Creation.ipynb file. We have our past work and result inside as well for the notebook. However, if needed, please restart and run all. The notebook will run and generate the results for you. 

The requirements to run the notebook can be found at ./model_creation/requirements.txt

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
