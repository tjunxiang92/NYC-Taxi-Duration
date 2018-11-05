import json
import urllib.request

# long1, lat1, long2, lat2
def get_distance(x):
  url = "http://127.0.0.1:5000/route/v1/driving/{},{};{},{}?steps=false&overview=false".format(
    x[0],
    x[1],
    x[2],
    x[3],
  )
  print(url)
  contents = urllib.request.urlopen(url).read()
  parsed_json = json.loads(contents)
  return parsed_json['routes'][0]['distance']


dist = get_distance([-73.944725036621094, 40.779273986816406, -73.961753845214844, 40.766147613525391]) / 1.609
print(dist)
