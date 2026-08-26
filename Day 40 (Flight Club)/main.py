import re
import requests_cache
from pprint import pprint
from data_manager import DataManager, DEFAULT_LOWEST_PRICE
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from datetime import datetime, timedelta
from notification_manager import NotificationManager

# =============================CONSERVE REQUESTS=====================================#

requests_cache.install_cache('flight_cache', backend='sqlite',
                              urls_expire_after={
                                  "*.sheety.co": requests_cache.DO_NOT_CACHE,
                                  "*": 3600
                              })

# ===================================SET UP HELPERS==================================#

data_manager = DataManager()
flights_search = FlightSearch()
notification_manager = NotificationManager()

# ====================================SET THE DATES==================================#

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=184)
return_date_str = six_months_from_today.strftime("%Y-%m-%d")

# =========================PULL EACH USER'S TRIP REQUEST=============================#
# Each row = one Google Form submission: {email, origin, destination1, destination2, destination3}

flight_requests = data_manager.get_flight_requests()

price_data = data_manager.get_price_data()
price_lookup = {
    (row["origin"].strip().upper(), row["destination"].strip().upper()): row
    for row in price_data
}

# Reset every known route back to the absurdly-high default at the START of
# each run, so every valid fare found this run counts as an "improvement" and
# every recipient on a matching route gets emailed, regardless of past runs.
for row in price_lookup.values():
    data_manager.update_lowest_price(row["id"], DEFAULT_LOWEST_PRICE)
    row["lowestPrice"] = DEFAULT_LOWEST_PRICE

# Snapshot BEFORE the run starts. Everyone in this run gets compared against
# this, not against each other -- otherwise the first person to search a route
# "claims" the improvement and everyone else sharing that route gets skipped.
baseline_lowest = {key: row["lowestPrice"] for key, row in price_lookup.items()}

IATA_PATTERN = re.compile(r"^[A-Z]{3}$")


def is_valid_iata(code):
    return bool(IATA_PATTERN.match(code))


for request in flight_requests:
    email = request.get("emailAddress", "").strip()
    origin = request.get("origin", "").strip().upper()
    destinations = [
        request.get("destination1", "").strip().upper(),
        request.get("destination2", "").strip().upper(),
        request.get("destination3", "").strip().upper(),
    ]
    destinations = [d for d in destinations if d]  # drop any blank fields

    if not email:
        pprint(f"Skipping row: no email address found. Raw row: {request}")
        continue

    if not origin:
        pprint(f"Skipping {email}: no origin airport code given.")
        continue

    if not is_valid_iata(origin):
        pprint(f"Skipping {email}: origin '{origin}' isn't a valid 3-letter IATA code.")
        continue

    if not destinations:
        pprint(f"Skipping {email}: no destination cities given at all.")
        continue

    valid_destinations = [d for d in destinations if is_valid_iata(d)]
    invalid_destinations = [d for d in destinations if not is_valid_iata(d)]
    if invalid_destinations:
        pprint(f"{email}: dropping invalid destination code(s) {invalid_destinations}.")

    destinations = valid_destinations
    if not destinations:
        pprint(f"Skipping {email}: none of their destination codes were valid.")
        continue

    results = []

    for destination in destinations:
        pprint(f"Getting flights from {origin} to {destination} for {email}...")

        flights = flights_search.check_flights(
            origin, destination, from_time=tomorrow, to_time=six_months_from_today
        )
        cheapest = find_cheapest_flight(flights, return_date=return_date_str)

        # Only if no direct flights are available
        if cheapest.price == "N/A":
            pprint(f"No direct flight {origin}->{destination}. Checking indirect...")
            flights = flights_search.check_flights(
                origin, destination, from_time=tomorrow, to_time=six_months_from_today, is_direct=False
            )
            cheapest = find_cheapest_flight(flights, return_date=return_date_str)

        if cheapest.price == "N/A":
            pprint(f"No flights at all found from {origin} to {destination}.")
            continue

        route_key = (origin, destination)
        price_row = price_lookup.get(route_key)

        if price_row is None:
            pprint(f"No price history for {origin}->{destination}. Creating baseline row.")
            price_row = data_manager.create_price_row(origin, destination)
            price_lookup[route_key] = price_row
            baseline_lowest[route_key] = price_row["lowestPrice"]

        stored_lowest = baseline_lowest[route_key]

        if cheapest.price < stored_lowest:
            pprint(f"{origin}->{destination}: INR {cheapest.price} beats stored lowest INR {stored_lowest}.")
            # Only push to the sheet if this is a new low WITHIN this run too --
            # avoids redundant/conflicting writes when several people share a route.
            if cheapest.price < price_row["lowestPrice"]:
                data_manager.update_lowest_price(price_row["id"], cheapest.price)
                price_row["lowestPrice"] = cheapest.price
            results.append(cheapest)
        else:
            pprint(f"{origin}->{destination}: INR {cheapest.price} isn't lower than stored INR {stored_lowest}. Skipping.")

    if not results:
        pprint(f"No results for {email}, skipping email.")
        continue

    # ==========================BUILD A PERSONALIZED MESSAGE==========================#

    lines = []
    for flight in results:
        if flight.stops == 0:
            lines.append(
                f"- INR {flight.price}: direct, {flight.origin_airport} -> {flight.destination_airport}, "
                f"depart {flight.out_date}, return {flight.return_date}."
            )
        else:
            lines.append(
                f"- INR {flight.price}: {flight.stops} stop(s), {flight.origin_airport} -> {flight.destination_airport}, "
                f"depart {flight.out_date}, return {flight.return_date}."
            )

    message = "Here are the best fares we found for your requested trips:\n\n" + "\n".join(lines)

    pprint(f"---- Email to be sent to {email} ----")
    pprint(message)
    pprint("---------------------------------------")

    notification_manager.send_email(
        to_address=email,
        subject="Your Personalized Flight Deals!",
        body=message
    )
    pprint(f"Sent personalized flight deals to {email}.")