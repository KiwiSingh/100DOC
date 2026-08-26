import os
import requests
from datetime import datetime

GENDER = "male"
WEIGHT_KG = 120
HEIGHT_CM = 177
AGE = 30

APP_ID = os.getenv("WK_APP_ID")
API_KEY = os.getenv("WK_API_KEY")
WK_EP = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"
WK_QUERY = input("Tell me which exercises you did: ")
SHEETY_EP = os.getenv("SHEETY_EP")

HEADERS = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

PARAMS = {
    "query": WK_QUERY,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(WK_EP, json=PARAMS, headers=HEADERS)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
time_now = datetime.now().strftime("%X")
SHEETY_BEARER = os.getenv("SHEETY_BEARER")
BEARER_HEADERS = {
    "Authorization": f"Bearer {SHEETY_BEARER}"
}

for exercise in result["exercises"]:
    SHEETY_PARAMS = {
        "workout": {
            "date": today_date,
            "time": time_now,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    sheety_response = requests.post(SHEETY_EP, json=SHEETY_PARAMS, headers=BEARER_HEADERS)

    print(sheety_response.text)