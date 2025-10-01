import requests
import json
import pandas as pd
import auth_token_generator as alg

class BasicApiAccess(object):
    xAuthToken = None

    def __init__(self, usr, pwd):
        credentials = {
            "username": usr,
            "password": pwd
        }
        self.xAuthToken = self.get_xauth_token(credentials)

    def get_xauth_token(self, credentials):
        api_key = self.get_api_key(credentials)
        x_auth_token = alg.AuthTokenGenerator().calc_xauth_token(credentials["username"], api_key)
        return x_auth_token

    @staticmethod
    def get_api_key(credentials_int):
        url = "https://api.pegelalarm.at/api/login"
        payload = json.dumps(credentials_int)
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=payload, verify=False)


        if response.status_code == 200:
            if response.json()['status']['code'] == 200:
                return response.json()['payload']['apiKey']
            else:
                print("Invalid login: " + str(response.json()))
        else:
            print("Failed to call API: " + response.url)
        return None

    def query_current_data(self, station_name="", water_name="", common_id=""):
        parameters = {
            "qStationName": station_name,
            "qWater": water_name,
            "commonid": common_id
        }
        headers = {
            "Content-Type": "application/json",
            "X-AUTH-TOKEN": self.xAuthToken
        }
        response = requests.get("https://api.pegelalarm.at/api/station/1.1/list", params=parameters, headers=headers, verify=False)
        if response.status_code == 200:
            # jsonPrint(response.json()['payload'])
            return response.json()['payload']
        else:
            print("Failed to call API: " + response.url)

    # Possible values for 'unit': "height" and "flow"
    # Possible values for 'granularity': "raw" (for recent 3 months of data), "hour", "day", "month", "year" and "era"
    def query_historic_data(self, commonid, load_start_date_utc, load_end_date_utc, unit="height", granularity="hour"):
        load_start_date_str = load_start_date_utc.strftime("%d.%m.%YT%H:%M:%S") + "%2B0200"
        load_end_date_str = load_end_date_utc.strftime("%d.%m.%YT%H:%M:%S") + "%2B0200"
        url = "https://api.pegelalarm.at/api/station/1.1/" + unit + "/" + commonid + "/history?" + "loadStartDate=" \
              + load_start_date_str + "&loadEndDate=" + load_end_date_str + "&granularity=" + granularity
        headers = {
            "Content-Type": "application/json",
            "X-AUTH-TOKEN": self.xAuthToken
        }
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            history_df = pd.DataFrame(response.json()["payload"]["history"])
            if history_df.empty:
                print("DataFrame ist leer.")
            else:
                history_df['sourceDate'] = pd.to_datetime(history_df['sourceDate'], format='%d.%m.%YT%H:%M:%S%z')
            return history_df
        else:
            print("Failed to call API: " + response.url)
        return None
