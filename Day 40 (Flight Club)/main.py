import requests_cache
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from datetime import datetime, timedelta
from notification_manager import NotificationManager

#=============================CONSERVE REQUESTS=====================================#

requests_cache.install_cache('flight_cache', backend='sqlite',
                             urls_expire_after={
                                 "*.sheety.co": requests_cache.DO_NOT_CACHE,
                                 "*": 3600
                             })

#===================================TALK TO SHEETY==================================#

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flights_search = FlightSearch()
notification_manager = NotificationManager()

#===============================RETRIEVE YOUR CUSTOMER EMAILS=======================#

customer_data = data_manager.get_customer_emails()
customer_email_list = [row["emailAddress"] for row in customer_data]

#====================================SET THE DATES==================================#

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=184)


#=================================DO A FLIGHT SEARCH================================#
ORIGIN_CITY_IATA = "DEL"

for destination in sheet_data:
    pprint(f"Getting flights for {destination['city']}...")
    flights = flights_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_today
    )



#============================SHOW THE CHEAPEST FLIGHTS==============================#

    cheapest_flight = find_cheapest_flight(flights, return_date=six_months_from_today.strftime("%Y-%m-%d"))
    pprint(f"{destination['city']}: INR {cheapest_flight.price}")

    # Only if no direct flights are available
    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        stopover_flights = flights_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_months_from_today,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(stopover_flights, return_date=six_months_from_today.strftime("%Y-%m-%d"))
        print(f"Cheapest indirect flight price is: INR {cheapest_flight.price}")

#===================================SEND AN EMAIL===================================#
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        data_manager.update_lowest_price(destination["id"], cheapest_flight.price)
        # Customise the message depending on the number of stops
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only INR {cheapest_flight.price} to fly direct " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only INR {cheapest_flight.price} to fly " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"with {cheapest_flight.stops} stop(s) " \
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        print(f"Check your email. Lower price flight found to {destination['city']}!")

        # Send emails to everyone on the list
        notification_manager.send_emails(email_list=customer_email_list, email_body=message)