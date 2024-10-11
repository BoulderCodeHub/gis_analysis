import geopandas as gpd
from shapely import Point, Polygon
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import earthaccess
import os
import netCDF4 # import libraries
print(earthaccess.__version__)

large_grids = gpd.read_file(os.path.join('snowpack_data', 'large_grids.shp'))
print(large_grids.crs)
large_grids = large_grids.to_crs('EPSG:4269')
earthaccess.login()
days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
for file_name in ['CBRFC', 'CNRFC']:
  basin_gdf = gpd.read_file(os.path.join(file_name + '_Basins', 'b_' + file_name.lower() + '.shp'))
  basin_gdf = basin_gdf.to_crs('EPSG:4269')
  for index, row in large_grids.iterrows():
    this_grid = large_grids[large_grids.index == index]
    basins_in_this_grid = gpd.sjoin(basin_gdf, this_grid, how = 'inner', predicate = 'intersects')
    try:
      basins_in_this_grid = basins_in_this_grid.drop('index_left', axis=1)
    except:
      pass
    try:
      basins_in_this_grid = basins_in_this_grid.drop('index_right', axis=1)
    except:
      pass
      
    print(row['grid_id'], end = " ")
    print(len(basins_in_this_grid.index))
    if len(basins_in_this_grid.index) > 0:
      grid_points = gpd.read_file(os.path.join('snowpack_data', 'elevation_shapefiles', row['grid_id']))
      grid_locs = row['grid_id'].split('_')
      grid_lat = int(grid_locs[0][1:])
      grid_long = int(grid_locs[1][2:])
      year_pull = 2010
      month_pull = 10
      day_pull = 1
      next_year = 2010
      next_month = 10
      next_day = 2
      leap_counter = 0
      while year_pull < 2021 or month_pull < 10:
        this_date = str(year_pull) + '-' + str(month_pull) + '-' + str(day_pull)
        next_date = str(next_year) + '-' + str(next_month) + '-' + str(next_day)
        found_vals = False
        try:
          results = earthaccess.search_data(
            short_name='wus_ucla_sr',
            bounding_box=(-1 * grid_long, grid_lat, -1 * grid_long + 1, grid_lat + 1),
            temporal=(this_date, next_date),
            count= 3)
          found_vals = True
        except Exception as e:
          print(e)
        print(this_date, end = " ")
        print(next_date)
        if found_vals:
          for b_idx, b_rw in basins_in_this_grid.iterrows():
            this_basin = basins_in_this_grid[basins_in_this_grid.index == b_idx]
            this_basin_points = gpd.sjoin(grid_points, this_basin, how = 'inner', predicate = 'within')
        
        day_pull += 1
        next_day += 1
        if leap_counter == 0 and month_pull == 2:
          days_use = 29
        else:
          days_use = days_in_month[month_pull - 1]
        if day_pull == days_use:
          day_pull = 1
          month_pull += 1
          if month_pull == 13:
            month_pull = 1
            year_pull += 1
            leap_counter += 1
            if leap_counter == 4:
              leap_counter = 0
        if leap_counter == 0 and month_pull == 2:
          days_use_next = 29
        else:
          days_use_next = days_in_month[next_month - 1]
        if next_day == days_use_next:
          next_day = 1
          next_month += 1
          if next_month == 13:
            next_month = 1
            next_year += 1
            