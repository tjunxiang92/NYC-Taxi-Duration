import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import datetime
import calendar

def get_avg_speed(x,y):
    return x/(y/60/60)

def get_day_name(x):
    return calendar.day_name[x]

def get_month_name(x):
    '''months = ["Unknown",
          "January",
          "Febuary",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"]'''
    return calendar.month_name[x]

def get_timeofday(x):
  cat = x.hour // 6
  if cat == 0:
    return 'midnight'
  elif cat == 1:
    return 'morning'
  elif cat == 2:
    return 'afternoon'
  elif cat == 3:
    return 'night'

def haversine_(lat1, lng1, lat2, lng2):
    #function to calculate haversine distance between two coordinates
    lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
    AVG_EARTH_RADIUS = 6371  # in km
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = np.sin(lat * 0.5) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * np.arcsin(np.sqrt(d))
    return(h)

def manhattan_distance_pd(lat1, lng1, lat2, lng2):
    #function to calculate manhatten distance between pick_drop
    a = haversine_(lat1, lng1, lat1, lng2)
    b = haversine_(lat1, lng1, lat2, lng1)
    return a + b

train_df = pd.read_csv("train.csv")
train_data = train_df.copy()

#Figure 1
sns.set()
f, axes = plt.subplots()
sns.despine(left=True)
sns.distplot(np.log(train_df['trip_duration'].values+1), axlabel = 'Log(trip_duration)', label = 'log(trip_duration)', bins = 50)
plt.setp(axes, yticks=[])
plt.tight_layout()
plt.show()

#Feature Extraction
train_data['pickup_datetime'] = pd.to_datetime(train_data.pickup_datetime)
train_data.loc[:, 'pick_date'] = train_data['pickup_datetime'].dt.date
train_data.loc[:,'hour'] = train_data['pickup_datetime'].dt.hour
train_data.loc[:,'dayofweek'] = train_data['pickup_datetime'].dt.dayofweek
train_data.loc[:,'dayofmonth'] = train_data['pickup_datetime'].dt.day
train_data.loc[:,'month'] = train_data['pickup_datetime'].dt.month
train_data['pickup_timeofday'] = train_data['pickup_datetime'].map(get_timeofday)
train_data.loc[:,'distance'] = manhattan_distance_pd(train_data['pickup_latitude'].values, train_data['pickup_longitude'].values, train_data['dropoff_latitude'].values, train_data['dropoff_longitude'].values)
train_data.loc[:,'avg_speed'] = get_avg_speed(train_data['distance'].values,train_data['trip_duration'].values)

#Figure 2
ts_v1 = pd.DataFrame(train_data.loc[train_data['vendor_id']==1].groupby('pick_date')['trip_duration'].mean())
ts_v1.reset_index(inplace = True)
ts_v2 = pd.DataFrame(train_data.loc[train_data['vendor_id']==2].groupby('pick_date')['trip_duration'].mean())
ts_v2.reset_index(inplace = True)

from bokeh.palettes import Spectral4
from bokeh.plotting import figure, show
p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")
p.title.text = 'Click on legend entries to hide the corresponding lines'

for data, name, color in zip([ts_v1, ts_v2], ["vendor 1", "vendor 2"], Spectral4):
    df = data
    p.line(df['pick_date'], df['trip_duration'], line_width=2, color=color, alpha=0.8, legend=name)

p.legend.location = "top_right"
p.legend.click_policy="hide"
p.yaxis.axis_label = "Avg Trip Duration"
show(p)

#Figure 3
trip_number_v1 = pd.DataFrame(train_data.loc[train_data['vendor_id']==1].groupby('pick_date')['id'].count())
trip_number_v1.reset_index(inplace = True)
trip_number_v2 = pd.DataFrame(train_data.loc[train_data['vendor_id']==2].groupby('pick_date')['id'].count())
trip_number_v2.reset_index(inplace = True)

p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")
p.title.text = 'Click on legend entries to hide the corresponding lines'

for data, name, color in zip([trip_number_v1, trip_number_v2], ["vendor 1", "vendor 2"], Spectral4):
    df = data
    p.line(df['pick_date'], df['id'], line_width=2, color=color, alpha=0.8, legend=name)

p.legend.location = "bottom_right"
p.legend.click_policy="hide"
p.yaxis.axis_label = "No. of Trips"
show(p)

#Figure 4
f, axes = plt.subplots(2,2)
sns.distplot(train_df['pickup_latitude'].values, label = 'pickup_latitude',color="r",bins = 100, ax=axes[0,0])
sns.distplot(train_df['pickup_longitude'].values, label = 'pickup_longitude',color="b",bins =100, ax=axes[0,1])
sns.distplot(train_df['dropoff_latitude'].values, label = 'dropoff_latitude',color="r",bins =100, ax=axes[1, 0])
sns.distplot(train_df['dropoff_longitude'].values, label = 'dropoff_longitude',color="b",bins =100, ax=axes[1, 1])
plt.tight_layout()
plt.show()

#Excluding the outlier locations
df = train_df.loc[(train_df.pickup_latitude > 40.6) & (train_df.pickup_latitude < 40.9)]
df = df.loc[(df.dropoff_latitude>40.6) & (df.dropoff_latitude < 40.9)]
df = df.loc[(df.dropoff_longitude > -74.05) & (df.dropoff_longitude < -73.7)]
df = df.loc[(df.pickup_longitude > -74.05) & (df.pickup_longitude < -73.7)]
train_data_new = df.copy()

#Figure 5
rgb = np.zeros((3000, 3500, 3), dtype=np.uint8)
rgb[..., 0] = 255
rgb[..., 1] = 255
rgb[..., 2] = 255
train_data_new['pick_lat_new'] = list(map(int, (train_data_new['pickup_latitude'] - (40.6000))*10000))
train_data_new['drop_lat_new'] = list(map(int, (train_data_new['dropoff_latitude'] - (40.6000))*10000))
train_data_new['pick_lon_new'] = list(map(int, (train_data_new['pickup_longitude'] - (-74.050))*10000))
train_data_new['drop_lon_new'] = list(map(int,(train_data_new['dropoff_longitude'] - (-74.050))*10000))

summary_plot = pd.DataFrame(train_data_new.groupby(['pick_lat_new', 'pick_lon_new'])['id'].count())
summary_plot.reset_index(inplace = True)
summary_plot.head(120)
lat_list = summary_plot['pick_lat_new'].unique()
for i in lat_list:
    lon_list = summary_plot.loc[summary_plot['pick_lat_new']==i]['pick_lon_new'].tolist()
    unit = summary_plot.loc[summary_plot['pick_lat_new']==i]['id'].tolist()
    for j in lon_list:
        a = unit[lon_list.index(j)]
        if (a//50) >0:
            rgb[i][j][0] = 255
            rgb[i,j, 1] = 0
            rgb[i,j, 2] = 255
        elif (a//10)>0:
            rgb[i,j, 0] = 0
            rgb[i,j, 1] = 255
            rgb[i,j, 2] = 0
        else:
            rgb[i,j, 0] = 255
            rgb[i,j, 1] = 0
            rgb[i,j, 2] = 0
fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(14,20))
img = ax.imshow(rgb, cmap = 'hot')
ax.set_axis_off() 
plt.show()

#Figure 6
df = train_data.loc[train_data.passenger_count!=0]
train_data2 = df.copy()
train_data2['trip_duration'] = np.log(train_data['trip_duration'])
sns.set()
sns.set_palette("husl")
sns.violinplot(x='passenger_count', y='trip_duration', hue='vendor_id', data=train_data2, split=True, inner='quart',palette={1: "g", 2: "r"})
plt.show()

#Figure 7
sns.boxplot(x="dayofweek", y="trip_duration", hue="vendor_id", data=train_data, palette="husl")
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.subplots_adjust(right=0.85)
plt.ylim(0,6000)
plt.xticks(np.arange(7), calendar.day_name[0:7])
plt.show()

#Figure 8
summary_time_duration = pd.DataFrame(train_data.groupby(['dayofweek','hour'])['trip_duration'].mean())
summary_time_duration.reset_index(inplace=True)
summary_time_duration['unit']=1
summary_time_duration['dayofweek']=summary_time_duration['dayofweek'].map(get_day_name)
sns.tsplot(data=summary_time_duration, time="hour", unit='unit', condition="dayofweek", value='trip_duration')
plt.legend(loc='upper center', ncol=3)
plt.show()

#Figure 9
summary_timeofday = pd.DataFrame(train_data.groupby(['vendor_id','pickup_timeofday'])['id'].count())
summary_timeofday.reset_index(inplace=True)
sns.barplot(x='pickup_timeofday', y='id', hue='vendor_id', data=summary_timeofday, order=["morning","afternoon","night","midnight"])
plt.xlabel("Time of Day") 
plt.ylabel("No. of Rides")
plt.tight_layout()
plt.show()

#Figure 10
summary_avg_speed = pd.DataFrame(train_data.groupby(['dayofweek','hour'])['avg_speed'].mean())
summary_avg_speed.reset_index(inplace=True)
summary_avg_speed['dayofweek']=summary_avg_speed['dayofweek'].map(get_day_name)
sns.lineplot(x='hour', y='avg_speed', data=summary_avg_speed, hue='dayofweek', legend='full')
plt.legend(ncol=2)
plt.show()

#Figure 11
summary_heatmap = pd.DataFrame(train_data.groupby(['month','dayofmonth'])['id'].count())
summary_heatmap.reset_index(inplace=True)
heatmap = summary_heatmap.pivot(index='dayofmonth',columns='month',values='id')
heatmap.rename(columns=get_month_name,inplace=True)
sns.heatmap(heatmap, annot=True, fmt='g', xticklabels=True, yticklabels=True, cmap="coolwarm")
plt.tight_layout()
plt.show()
