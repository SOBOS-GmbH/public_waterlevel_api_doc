from basic_api_access import BasicApiAccess
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dotenv import load_dotenv
import os

# Create a .env file and enter your username and password into it (using USERNAME and PASSWORD as keys).
# If you don't have a username/password, please write to office@sobos.at
load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")


def chartGaugeWaterlevel(station_name, water_name, loadStartDate, loadEndDate, title=None, filename=None):
    baa = BasicApiAccess(username, password)
    currentStationData = baa.query_current_data(station_name=station_name, water_name=water_name)
    print("Result: " + str(currentStationData["stations"][0]))
    result0CommonId = currentStationData["stations"][0]["commonid"]

    # Load historic water level height for a specific station
    df = baa.query_historic_data(result0CommonId, loadStartDate, loadEndDate)
    if df.empty:
        print("DataFrame ist leer.")
    else:
        df.set_index("sourceDate", inplace=True)
        print("Result: " + str(df))

        # Chart data
        if title is None:
            title = station_name + " / " + water_name + " from " \
                    + (load_to - load_hours).strftime("%Y-%m-%d %H:%M") + " to " + load_to.strftime("%Y-%m-%d %H:%M")

        ax = plt.gca()
        ax.plot(df.index.values, df['value'].values, '-o', color='blue', markersize=2)
        ax.set(xlabel="Source date", ylabel="cm", title=title)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.close()


if __name__ == "__main__":
    load_to = datetime.datetime.now()
    load_hours = datetime.timedelta(hours=2 * 24)
    chartGaugeWaterlevel("Linz", "Donau", load_to - load_hours, load_to)
