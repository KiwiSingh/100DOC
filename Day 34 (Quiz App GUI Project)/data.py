import requests
parameters = {
    "amount": 10,
    "type": "boolean",
    "category": 27
}
question_data = requests.get(url="https://opentdb.com/api.php", params=parameters, timeout=10).json()["results"]