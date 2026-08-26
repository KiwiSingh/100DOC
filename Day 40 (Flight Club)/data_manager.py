import os
import requests
from requests.auth import HTTPBasicAuth

PRICES_EP = os.getenv("SHEETY_GET_EP")
DEFAULT_LOWEST_PRICE = 10_000_000  # absurdly high so the first real fare always "wins"


class DataManager:
    def __init__(self):
        self.user = os.getenv("SHEETY_USERNAME")
        self.password = os.getenv("SHEETY_PASSWORD")
        self._authorization = HTTPBasicAuth(self.user, self.password)
        self.users_endpoint = os.getenv("SHEETY_USERS_EP")
        self.price_data = []
        self.flight_requests = []

    # =====================PRICE TRACKING (keyed by origin+destination)=====================#

    def get_price_data(self):
        """
        Reads the 'prices' sheet. Expects rows shaped like:
            { "id": ..., "origin": "DEL", "destination": "CGK", "lowestPrice": 34000 }
        """
        response = requests.get(url=PRICES_EP, auth=self._authorization)
        response.raise_for_status()
        data = response.json()
        self.price_data = data["prices"]
        return self.price_data

    def create_price_row(self, origin, destination, lowest_price=DEFAULT_LOWEST_PRICE):
        """
        Creates a new row for a route we haven't seen before, seeded at an
        absurdly high price so the very first real fare found always counts
        as an improvement. Returns the created row (includes its new id).
        """
        new_row = {
            "price": {
                "origin": origin,
                "destination": destination,
                "lowestPrice": lowest_price
            }
        }
        response = requests.post(url=PRICES_EP, json=new_row, auth=self._authorization)
        response.raise_for_status()
        return response.json()["price"]

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

    # ==========TRIP REQUESTS (from the 'users' sheet, fed by the Google Form)==========#

    def get_flight_requests(self):
        """
        Reads the "users" sheet (fed directly by the Google Form). Expects rows
        shaped like: { "emailAddress": ..., "origin": ..., "destination1": ...,
                        "destination2": ..., "destination3": ... }

        Since a Form only ever APPENDS a new row per submission, this dedupes
        by email and keeps the most recent submission for each person.
        """
        response = requests.get(url=self.users_endpoint, auth=self._authorization)
        response.raise_for_status()
        data = response.json()
        rows = data["users"]

        latest_by_email = {}
        for row in rows:
            email = row.get("emailAddress", "").strip().lower()
            if email:
                latest_by_email[email] = row  # later rows overwrite earlier ones

        self.flight_requests = list(latest_by_email.values())
        return self.flight_requests