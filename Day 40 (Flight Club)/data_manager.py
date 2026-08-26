import os
import requests
from requests.auth import HTTPBasicAuth

PRICES_EP = os.getenv("SHEETY_GET_EP")
class DataManager:
    def __init__(self):
        self.user = os.getenv("SHEETY_USERNAME")
        self.password = os.getenv("SHEETY_PASSWORD")
        self._authorization = HTTPBasicAuth(self.user, self.password)
        self.users_endpoint = os.getenv("SHEETY_USERS_EP")
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=PRICES_EP, auth=self._authorization)
        data = response.json()
        self.destination_data = data["prices"] # These prices are in INR now btw
        return self.destination_data


    #================UPDATE THE PRICE IN THE SPREADSHEET==================#

    def update_lowest_price(self, row_id, new_price):
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }
        requests.put(
            url=f"{PRICES_EP}/{row_id}",
            json=new_data,
            auth=self._authorization
        )
    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint, auth=self._authorization)
        data = response.json()
        # Name of spreadsheet 'tab' with the customer emails should be "users".
        self.customer_data = data["users"]
        return self.customer_data