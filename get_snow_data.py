import earthaccess
import os
import netCDF4 # import libraries
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np

earthaccess.login()
num_lat_grid_cells = 21
num_long_grid_cells = 27
counter1 = 0
counter2 = 0
while counter2 < num_lat_grid_cells:
  vals_exist = False
  try:
    results = earthaccess.search_data(
        short_name='WUS_UCLA_SR',
        bounding_box=(-126 + counter1, 30 + counter2, -126 + counter1 + 1, 30 + counter2 + 1),
        temporal=("2010-01", "2010-02"),
        count= 10)
    vals_exist = True
  except Exception as e:
    print(e)
    
        
      
  if vals_exist:
    files = earthaccess.download(results, "./snowpack_data")
  counter1 += 1
  if counter1 == num_long_grid_cells:
    counter2 += 1
    counter1 = 0
  print(counter1, end = " ")
  print(counter2)
    
