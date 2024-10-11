import geopandas as gpd
from shapely import Point, Polygon
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

file_list = [f for f in os.listdir(os.path.join('snowpack_data', 'index_shapefiles')) if os.path.isfile(os.path.join('snowpack_data', 'index_shapefiles', f))]
polygon_list = []
filename_list = {}
filename_list['grid_id'] = []
for fp in file_list:
  if fp[-3:] == 'shp':
    print(fp)
    this_shapefile = gpd.read_file(os.path.join('snowpack_data', 'index_shapefiles', fp))
    min_x, min_y, max_x, max_y = this_shapefile.total_bounds
    point_1 = (min_x,min_y)
    point_2 = (max_x,min_y)
    point_3 = (max_x,max_y)
    point_4 = (min_x,max_y)
    polygon_list.append(Polygon([point_1, point_2, point_3, point_4]))
    filename_list['grid_id'].append(fp)

large_grids = gpd.GeoDataFrame(filename_list, crs = this_shapefile.crs, geometry = polygon_list)
large_grids.to_file(os.path.join('snowpack_data', 'large_grids.shp'), driver='ESRI Shapefile')
