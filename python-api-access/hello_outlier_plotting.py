import datetime
from hello_chart import chartGaugeWaterlevel
import pandas as pd

# 1) Reads meta-data from outliers from a CSV file
# 2) Loads the historic data from before and after the outlier
# 3) Plots a chart of the loaded data and writes it to a file

hours_delta = datetime.timedelta(hours=24)
#df_outliers = pd.read_csv('input/outliers_subset.csv', sep=";")            # Use this for debugging
df_outliers = pd.read_csv('input/outliers.csv', sep=";")
for index, row in df_outliers.iterrows():
    outlier_dts = datetime.datetime.strptime(row["sourcedate"], '%Y-%m-%d %H:%M:%S.%f')
    station_name = row["stationname"]
    water_name = row["water"]
    filename = 'output/' + station_name + '_' + water_name + '_' + outlier_dts.strftime("%Y%m%d-%H%M") + '.png'
    title = station_name + " / " + water_name + " at " + outlier_dts.strftime("%Y-%m-%d %H:%M")

    chartGaugeWaterlevel(station_name, water_name,
                         outlier_dts - hours_delta,  outlier_dts + hours_delta,
                         title, filename)

