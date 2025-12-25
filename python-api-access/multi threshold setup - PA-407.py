from basic_api_access import BasicApiAccess
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dotenv import load_dotenv
import os
import requests
import json

# Create a .env file and enter your username and password into it (using USERNAME and PASSWORD as keys).
# If you don't have a username/password, please write to office@sobos.at
load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")


# This creates an on-demand threshold without a subscription
def set_ondemand_threshold(commonid: str, 
                  threshold: int,
                  contact_list: list,
                  alarm_msg: str = ""):
    url = "https://api.pegelalarm.at/api/uset/3.1/station/threshold"

    targets = []
    for contact in contact_list:
        if "telefon" in contact and contact["telefon"]:
             targets.append({
                "type": "SMS",
                "value": contact["telefon"],
                "active": True
            })
        if "email" in contact and contact["email"]:
            targets.append({
                "type": "EMAIL",
                "value": contact["email"],
                "active": True
            })

    payload = json.dumps({
        "commonid": commonid,
        "threshold": threshold,
        "unit": "cm",
        "direction": "ABOVE",
        "checkInFutureHours": 0,
        "description": alarm_msg,
        "silent": False,
        "targets": targets
    })
    
    baa = BasicApiAccess(username, password)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8',
        'X-AUTH-TOKEN': baa.xAuthToken,
        'Accept-Language': 'de-AT,de;q=0.9'
    }

    #print(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


# This creates a subscription
def set_dailymail_threshold(commonid: str,
                  billing_address: str = "strassmayr+pa-407-test@gmail.com"):
    url = "https://api.pegelalarm.at/api/uset/1.0/subscription/manage?skipThresholdTargetsValidation=true"
    
    payload = json.dumps({
        "commonid": commonid,
        "threshold": 9999,  # dummy value, not used for daily mails
        "unit": "cm",
        "direction": "ABOVE",
        "daily": True,
        "billingEmail": billing_address,
        "targets": [{
            "type":   "EMAIL",
            "value":  billing_address,
            "active": True
        }]
    })
    
    baa = BasicApiAccess(username, password)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8',
        'X-AUTH-TOKEN': baa.xAuthToken,
        'Accept-Language': 'de-AT,de;q=0.9'
    }

    #print(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)



station_data_prod = {
    "205351-at": {
        "name": "Kammer / Attersee",
        "HW1": 175, "HW5": 200, "HW10": 215, "HW30": 235
    },
    "205369-at": {
        "name": "Raudaschlsäge / Ager",
        "HW1": 83, "HW5": 90, "HW10": 105, "HW30": 115
    },
    "206276-at": {
        "name": "Dürnau / Ager",
        "HW1": 145, "HW5": 160, "HW10": 170, "HW30": 190
    },
    "205393-at": {
        "name": "Timelkam / Vöckla",
        "HW1": 295, "HW5": 370, "HW10": 395, "HW30": 445
    },
    "205401-at": {
        "name": "St. Georgen / Dürre Ager",
        "HW1": 250, "HW5": 310, "HW10": 340, "HW30": 370
    },
    "205419-at": {
        "name": "Vöcklabruck / Vöckla",
        "HW1": 270, "HW5": 360, "HW10": 390, "HW30": 420
    },
    "205427-at": {
        "name": "Schalchham / Ager",
        "HW1": 295, "HW5": 390, "HW10": 410, "HW30": 445
    }
}

station_data_dev = {
    "205351-at": {
        "name": "Kammer / Attersee",
        "HW1": 175, "HW5": 200, "HW10": 215, "HW30": 235
    },
    "205369-at": {
        "name": "Raudaschlsäge / Ager",
        "HW1": 83, "HW5": 90, "HW10": 105, "HW30": 115
    }
}

alarm_msgs = {
    "HW1": "HOCHWASSERALARM HW1 AM PEGEL {station_name} – SOFORTIGE RÄUMUNG FLUSSBEREICHE MINDESTENS AUSSERHALB HW10",
    "HW5": "HOCHWASSERALARM HW5 AM PEGEL {station_name} – SOFORTIGE RÄUMUNG BAUGRUBE UND ABSTELLEN GERÄTSCHAFTEN VON HW10 BIS MINDESTENS HW30",
    "HW10": "HOCHWASSERALARM HW10 AM PEGEL {station_name} – VORBEREITUNG FLUTUNG & BEOBACHTUNG BAUGRUBE UND ABSTELLEN GERÄTSCHAFTEN VON HW30 SO WEIT ALS MÖGLICH NACH OBEN",
    "HW30": "HOCHWASSERALARM HW30 AM PEGEL {station_name} – VERLASSEN DER BAUSTELLE IM HW30 BEREICH – VERSTÄNDIGUNG EINSATZORGANISATIONEN NACH ERFORDERNIS",
}

contact_list_prod = [
]

contact_list_dev = [
    {
        "id": 1,
        "name": "Johannes Strassmayr",
        "telefon": "+436644549594",
        "email": "strassmayr+pa-407-dev@gmail.com"
    },
    {
        "id": 2,
        "name": "Johnboy",
        "telefon": "+43664",
        "email": "insertsomemailaddress@gmail.com"
    }
]


station_data = station_data_dev
contact_list = contact_list_dev

do_ondemand = False         # already done
do_dailymail = False        # already done

if __name__ == "__main__":
    print("===== Setting thresholds for Pegelalarm PA-407 project =====")

    if do_ondemand:
        for station_id in station_data.keys():
            print(f"Station: {station_data[station_id]['name']}")
                
            for hw in ["HW1", "HW5", "HW10", "HW30"]:
                threshold_value = station_data[station_id][hw]
                alarm_msg = alarm_msgs[hw].format(station_name=station_data[station_id]["name"])
                #print(f"Setting threshold @{hw} = {threshold_value} cm")
                print(f"Alarm message: {alarm_msg}")
                
                set_ondemand_threshold(commonid=station_id, 
                            threshold=threshold_value, 
                            contact_list=contact_list, 
                            alarm_msg=alarm_msg) 
                print("----")
    
    if do_dailymail:
        n = 0
        for contact in contact_list:
            customer_email = contact["email"]
            target = f"strassmayr+pa-407-rename-{n}@gmail.com"
            print(f"Setting daily mail for {target}")
            set_dailymail_threshold(commonid="205427-at",
                        billing_address=target)
            n += 1
    
    print("================")