import geopandas
import pandas as pd
from shapely.geometry import mapping, MultiLineString, MultiPoint, LineString, Point, Polygon

df = geopandas.read_file('/content/drive/My Drive/corrected_shp_reproject/combined_reproject2.shp') 

def trung_diem(A, B):
  x1 = (A.coords[0][0] + B.coords[0][0])/2
  y1 = (A.coords[0][1] + B.coords[0][1])/2
  return Point(x1,y1)

def tim_diem_biet_trung_diem(A,B):
  x1 = 2*A.coords[0][0] - B.coords[0][0]
  y1 = 2*A.coords[0][1] - B.coords[0][1]
  return Point(x1,y1)

def open_gable_roof(polygon):
  all_coords = mapping(polygon)["coordinates"]

  sizeA = pow(all_coords[0][0][0] - all_coords[0][1][0], 2) + pow(all_coords[0][0][1] - all_coords[0][1][1], 2)
  sizeB = pow(all_coords[0][3][0] - all_coords[0][0][0], 2) + pow(all_coords[0][0][1] - all_coords[0][3][1], 2)

  if sizeA > sizeB:
      x1 = abs(all_coords[0][0][0] + all_coords[0][3][0])/2
      y1 = abs(all_coords[0][0][1] + all_coords[0][3][1])/2
      x2 = abs(all_coords[0][2][0] + all_coords[0][1][0])/2
      y2 = abs(all_coords[0][2][1] + all_coords[0][1][1])/2
  else:
      x1 = abs(all_coords[0][0][0] + all_coords[0][1][0])/2
      y1 = abs(all_coords[0][0][1] + all_coords[0][1][1])/2
      x2 = abs(all_coords[0][2][0] + all_coords[0][3][0])/2
      y2 = abs(all_coords[0][2][1] + all_coords[0][3][1])/2

  A = Point(x1, y1)
  B = Point(x2, y2)
  
  return LineString([A, B])

  def hip_roof(polygon):
  all_coords = mapping(polygon.geometry[0])["coordinates"]

  x1 = abs(all_coords[0][0][0]*3 + all_coords[0][1][0]*3+ all_coords[0][2][0] + all_coords[0][3][0])/8
  y1 = abs(all_coords[0][0][1]*3 + all_coords[0][1][1]*3 + all_coords[0][2][1] + all_coords[0][3][1])/8
  x2 = abs(all_coords[0][2][0]*3 + all_coords[0][3][0]*3+all_coords[0][0][0] + all_coords[0][1][0])/8
  y2 = abs(all_coords[0][2][1]*3 + all_coords[0][3][1]*3+all_coords[0][0][1] + all_coords[0][1][1])/8

  A = Point(x1, y1)
  B = Point(x2, y2)
  
  return LineString([A, B])

  def mansard_roof(polygon):
  all_coords = mapping(polygon)["coordinates"]

  A = Point(all_coords[0][0][0], all_coords[0][0][1])
  B = Point(all_coords[0][1][0], all_coords[0][1][1])
  C = Point(all_coords[0][2][0], all_coords[0][2][1])
  D = Point(all_coords[0][3][0], all_coords[0][3][1])
  
  C1 = A1 = trung_diem(A,C)
  D1 = B1 = trung_diem(B,D)
  
  for i in range(2):
    A1 = trung_diem(A1,A)
    B1 = trung_diem(B1,B)
    C1 = trung_diem(C1,C)
    D1 = trung_diem(D1,D)
  
  return Polygon([A1, B1, C1, D1, A1])

  def flat_roof(polygon):
  all_coords = mapping(polygon)["coordinates"]

  A = Point(all_coords[0][0][0], all_coords[0][0][1])
  B = Point(all_coords[0][1][0], all_coords[0][1][1])
  C = Point(all_coords[0][2][0], all_coords[0][2][1])
  D = Point(all_coords[0][3][0], all_coords[0][3][1])
  
  C1 = A1 = trung_diem(A,C)
  D1 = B1 = trung_diem(B,D)
  
  for i in range(2):
    A1 = trung_diem(A1,A)
    B1 = trung_diem(B1,B)
    C1 = trung_diem(C1,C)
    D1 = trung_diem(D1,D)

  A2 = tim_diem_biet_trung_diem(A,A1)
  B2 = tim_diem_biet_trung_diem(B,B1)
  C2 = tim_diem_biet_trung_diem(C,C1)
  D2 = tim_diem_biet_trung_diem(D,D1)
  return Polygon([A2, B2, C2, D2, A2])


linestring = []
ground =[]
height = []
for i in range(100):
  try:
    if len(df['geometry'].get(i).exterior.coords) == 5:
      
      linestring.append(flat_roof(df.geometry[i]))
      height.append(df['height'].get(i)+1)
  except:
    print(i)


# Cấu hình ra shapefile
gs = geopandas.GeoSeries(linestring)
d = {'geometry': linestring, 'r_height': height}
gdf = geopandas.GeoDataFrame(d, crs="EPSG:4326")
gdf.to_file('/content/drive/My Drive/corrected_shp_reproject/flat.shp') 