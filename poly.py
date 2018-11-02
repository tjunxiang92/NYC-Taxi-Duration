from shapely.geometry import MultiPolygon, Polygon, Point

# https://en.wikipedia.org/wiki/Boroughs_of_New_York_City
# Search https://nominatim.openstreetmap.org/details.php?place_id=198029316
# Download Polygon - http://polygons.openstreetmap.fr/
def parse_poly(lines):
  """ Parse an Osmosis polygon filter file.

    Accept a sequence of lines from a polygon file, return a shapely.geometry.MultiPolygon object.

    http://wiki.openstreetmap.org/wiki/Osmosis/Polygon_Filter_File_Format
  """
  in_ring = False
  coords = []
  
  for (index, line) in enumerate(lines):
    if index == 0:
      # first line is junk.
      continue
    
    elif index == 1:
      # second line is the first polygon ring.
      coords.append([[], []])
      ring = coords[-1][0]
      in_ring = True
    
    elif in_ring and line.strip() == 'END':
      # we are at the end of a ring, perhaps with more to come.
      in_ring = False
  
    elif in_ring:
      # we are in a ring and picking up new coordinates.
      ring.append(list(map(float, line.split())))
  
    elif not in_ring and line.strip() == 'END':
      # we are at the end of the whole polygon.
      break
  
    elif not in_ring and line.startswith('!'):
      # we are at the start of a polygon part hole.
      coords[-1][1].append([])
      ring = coords[-1][1][-1]
      in_ring = True
  
    elif not in_ring:
      # we are at the start of a polygon part.
      coords.append([[], []])
      ring = coords[-1][0]
      in_ring = True
  
  # print(coords)
  return MultiPolygon(coords)

polygons = [
  ('brooklyn', parse_poly(open('polygons/brooklyn.poly').readlines())),
  ('manhattan', parse_poly(open('polygons/manhattan.poly').readlines())),
  ('bronx', parse_poly(open('polygons/bronx.poly').readlines())),
  ('staten_island', parse_poly(open('polygons/staten_island.poly').readlines())),
  ('queens', parse_poly(open('polygons/queens.poly').readlines())),
]
