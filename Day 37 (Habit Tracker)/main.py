import requests
import os
from datetime import datetime

PXL_EP = "https://pixe.la/v1/users"
PXL_TOKEN = os.getenv("PXL_TOKEN")
USERNAME = "char1ot33r"
PARAMS = {
    "token": PXL_TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}


# response = requests.post(url=PXL_EP, json=PARAMS)
# print(response.text)

PXL_GRAPH_EP = f"{PXL_EP}/{USERNAME}/graphs"

GRAPH_PARAMS = {
    "id": "graph1",
    "name": "Python Tracker",
    "unit": "days",
    "type": "int",
    "color": "ajisai"
}

HEADERS = {
    "X-USER-TOKEN": PXL_TOKEN,
}

TODAY = datetime.now().strftime("%Y%m%d")

PXL_POST_PARAMS = {
    "date": TODAY,
    "quantity": input("How many days of Python lessons did you do today? "),
}

# response = requests.post(url=PXL_GRAPH_EP, json=GRAPH_PARAMS, headers=HEADERS)
# print(response.text)

PXL_POST_EP = f"{PXL_EP}/{USERNAME}/graphs/{GRAPH_PARAMS['id']}"
response = requests.post(url=PXL_POST_EP, json=PXL_POST_PARAMS, headers=HEADERS)
print(response.text)

# I didn't add PUT and DELETE endpoints because they are extremely elementary.
# I also doubt I'm going to update or delete any data once it's logged.