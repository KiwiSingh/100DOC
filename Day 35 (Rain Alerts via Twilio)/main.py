import os
import requests
from twilio.rest import Client
API_KEY = os.getenv("API_KEY")
MY_LAT = 29.8693496
MY_LONG = 77.8902124

parameters ={
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": API_KEY,
    "cnt": 4,
    "units": "metric"
}
def is_gonna_rain():
    try:
        response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters).json()
        weather_data = response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        weather_data = None

    for id in weather_data["list"]:
        if id["weather"][0]["id"] < 700:
            return True

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

if is_gonna_rain():
    message = client.messages.create(
        from_=os.getenv("TWILIO_TRIAL_NUMBER"),
        body="Inclement weather! Bring an umbrella ☂️", # This no longer works since Twilio
                                                        # migrated to a paid system btw
        to=os.getenv("MY_WHATSAPP_NUMBER"),
        content_sid=os.getenv("CONTENT_SID") # This depends on the templaate,
                                             # but I'm pretty sure paying users can generate
                                             # their own per message.
    )
    print("Great Scott! It's gonna rain!")
