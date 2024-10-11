import os
import netCDF4
import geopandas as gpd
import pandas as pd
import numpy as np

file_list = [f for f in os.listdir('snowpack_data') if os.path.isfile(os.path.join('snowpack_data', f))]
if not os.path.isdir(os.path.join('snowpack_data', 'index_shapefiles')):
  os.mkdir(os.path.join('snowpack_data', 'index_shapefiles'))
  
for fp in file_list:
  if 'SD_POST' in fp:
    print(fp)
    nc = netCDF4.Dataset(os.path.join('snowpack_data', fp))
    filename = fp.split('_')
    df = pd.DataFrame(index = np.arange(225 * 225), columns = ['id', 'Latitude', 'Longitude'])      
    fileNameID_main = filename[4] + '_' + filename[5] + '_'
    for xxx in range(0, 225):
      for yyy in range(0, 225):
        index_val = xxx * 225 + yyy
        df.loc[index_val, 'id'] = 'Lat' + str(yyy) + '_Long' + str(xxx)
        df.loc[index_val, 'Latitude'] = nc['Latitude'][yyy]
        df.loc[index_val, 'Longitude'] = nc['Longitude'][xxx]
    this_grid = gpd.GeoDataFrame(df, crs = 'EPSG:4326', geometry = gpd.points_from_xy(df.Longitude, df.Latitude))
    this_grid.to_file(os.path.join('snowpack_data', 'index_shapefiles', fileNameID_main + '.shp'), driver='ESRI Shapefile')
