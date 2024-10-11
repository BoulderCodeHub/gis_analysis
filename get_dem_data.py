import rasterio as rio
import os
import pandas as pd
import geopandas as gpd
import numpy as np

file_list_raster = [f for f in os.listdir('dem_data') if os.path.isfile(os.path.join('dem_data', f))]
file_list_shapes = [f for f in os.listdir(os.path.join('snowpack_data', 'index_shapefiles')) if os.path.isfile(os.path.join('snowpack_data', 'index_shapefiles', f))]
raster_header = 'USGS_1_'
lat_string = 'n'
long_string = 'w'
raster_ender = '_'
if not os.path.isdir(os.path.join('snowpack_data', 'elevation_shapefiles')):
  os.mkdir(os.path.join('snowpack_data', 'elevation_shapefiles'))
for fp in file_list_shapes:
  if fp[-3:] == 'shp':
    print(fp)
    this_shapefile = gpd.read_file(os.path.join('snowpack_data', 'index_shapefiles', fp))
    this_shapefile = this_shapefile.to_crs('EPSG:4269')
    print(this_shapefile.crs)
    coord_vals = fp.split('_')
    lat_coord = coord_vals[0][1:]
    long_coord = coord_vals[1][2:]
    raster_name = raster_header + lat_string + str(int(lat_coord) + 1) + long_string + str(int(long_coord)) + raster_ender
    found_file = False
    for raster_fp in file_list_raster:
      if raster_name in raster_fp:
        found_file = True
        break
    if found_file:
      with rio.open(os.path.join('dem_data', raster_fp)) as src:
        print(raster_fp)
        band1 = src.read()[0]
        print(this_shapefile.columns)
        new_vals = np.zeros(len(this_shapefile.index))
        idx_cnt = 0
        for index, row in this_shapefile.iterrows():
          geom_list = []
          diff_list = [-0.00222, -0.00111, 0.0, 0.00111, 0.00222]
          for dx in diff_list:
            for dy in diff_list:
              geom_list.append((row.geometry.x + dx, row.geometry.y + dy))
          value =  list(rio.sample.sample_gen(src, geom_list))
          new_vals[idx_cnt] = np.mean(value)
          if idx_cnt % 5000 == 0:
            print(index, end = " ")
            print(new_vals[idx_cnt])
          idx_cnt += 1
            
      elevation_locs_dict = {}
      elevation_locs_dict['elevation'] = new_vals
      elevation_locs_dict['id'] = this_shapefile['id']
      
      elevation_locs_df = pd.DataFrame(elevation_locs_dict, index = this_shapefile.index)
      elevation_locs_gdf = gpd.GeoDataFrame(elevation_locs_df, crs = this_shapefile.crs, geometry = this_shapefile.geometry)
      elevation_locs_gdf.to_file(os.path.join('snowpack_data', 'elevation_shapefiles', fp))
    else:
      print('no file')
