import earthaccess
import os
import netCDF4 # import libraries
import matplotlib.pyplot as plt
read_from_cloud = False
if read_from_cloud:
  earthaccess.login()
  results = earthaccess.search_data(
      short_name='wus_ucla_sr',
      bounding_box=(-125, 30, -100, 50),
      temporal=("1980-01", "2024-08"),
      count=10
  )
  files = earthaccess.download(results, "./snowpack_data")

read_from_netcdf = True
if read_from_netcdf:
  file_list = [f for f in os.listdir('snowpack_data') if os.path.isfile(os.path.join('snowpack_data', f))]
  for fp in file_list:
    nc = netCDF4.Dataset(os.path.join('snowpack_data', fp))
    try:
      for yy in range(0, 5):
        #print(nc['SWE_Post'][200,yy,:,:])
        print(nc['Latitude'][:])
        fig, ax = plt.subplots()
        cax = ax.imshow(nc['SWE_Post'][200,yy,:,:], interpolation='nearest', cmap='coolwarm')
        fig.colorbar(cax)

        plt.show()
        plt.close()        
    except:
      print(fp)

