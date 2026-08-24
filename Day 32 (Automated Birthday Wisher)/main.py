import os
import pandas as pd
import random
import smtplib
import datetime as dt
from pathlib import Path
import base64

PLACEHOLDER = "[NAME]"
letters_folder = Path("letter_templates")
letter_files = list(letters_folder.glob("*.txt"))
user_email_b64 = "cGFydGhhc2FyYXRoaS5zaW5naEBnbWFpbC5jb20="
user_email = base64.b64decode(user_email_b64).decode("utf-8")
password = os.getenv("SMTP_PASSWORD")

burf = pd.read_csv("birthdays.csv")
today = dt.date.today()

matches = burf[
    (burf["month"] == today.month)
    & (burf["day"] == today.day)
]

for _, person in matches.iterrows():
    letter = random.choice(letter_files)
    name = person["name"]
    email = person["email"]
    with open(letter) as file:
        out_letter = file.read().replace(PLACEHOLDER, name)
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=user_email, password=password)
            connection.sendmail(from_addr=user_email, to_addrs=email, msg=f"Subject:Happy Birthday\n\n{out_letter}")
            connection.close()







