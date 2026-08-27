import os
import requests

SERPAPI_EP = "https://serpapi.com/search"
class FlightSearch:
    def __init__(self):
        self._api_key = os.getenv("SERPAPI_KEY")

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        query = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time.strftime("%Y-%m-%d"),
            "return_date": to_time.strftime("%Y-%m-%d"),
            "type": "1",
            "adults": "1",
            "currency": "INR",
            "travel_class": "2",
            "api_key": self._api_key,

        }
        # Only include stops parameter if is_direct is True
        if is_direct:
            query["is_direct"] = "1"
        response = requests.get(url=SERPAPI_EP, params=query)

        if response.status_code != 200:
            print(f"check_flights error: {response.status_code}")
            return None

        data = response.json()
        if "error" in data:
            print(f"API error: {data['error']}")
            return None
        return data
