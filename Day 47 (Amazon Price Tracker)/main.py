#===========================================IMPORTS====================================================#

import os
from bs4 import BeautifulSoup
import requests
import smtplib
import base64
import html

#===========================================CONSTANTS==================================================#

PRODUCT_URL = "https://www.amazon.in/Western-Digital-Drive-3-5Inch-Encryption-Protection/dp/B08SMCPP58" 
                                                                    # URL with UTMs and stuff removed
TARGET_PRICE = 50000                                                # Seems like a reasonable price
                                                                    # given the memory shortage
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
user_email_b64 = "cGFydGhhc2FyYXRoaS5zaW5naEBnbWFpbC5jb20="
user_email = base64.b64decode(user_email_b64).decode("utf-8")
password = os.getenv("SMTP_PASSWORD")
to_address_b64 = "bWV0YWwuZ2FydXJ1d2luZC50ZXR1c2FpZ2EyMjNAZ21haWwuY29t"
to_address = base64.b64decode(to_address_b64).decode("utf-8")
subject = "Amazon Price Alert!"

#===========================================SOUPY SOUP================================================#


response = requests.get(url=PRODUCT_URL, headers=HEADERS, timeout=10)
soup = BeautifulSoup(response.text, "html.parser")
parent_div = soup.find("div", class_="a-section a-spacing-none aok-align-center aok-relative")
target_span = parent_div.find("span", id="apex-pricetopay-accessibility-label")
target_text = target_span.text
product_price = float((target_text.split("₹")[1].split(" with")[0]).replace(",", ""))
product_parent_div = soup.find("div", id="titleSection")
title_h1 = product_parent_div.find("h1", id="title")                # Yes, all of that effort just to
                                                                    # drill down into the title
product_title = html.unescape((title_h1.find("span", id="productTitle").text))
                                                                    # brings back the ampersand
message_body = f"{product_title} is now ₹{product_price}\n{PRODUCT_URL}"

#=========================================SENDING LE EMAIL===========================================#

if product_price <= TARGET_PRICE:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls
        connection.login(user_email, password)
        connection.sendmail(
            from_addr=user_email,
            to_addrs=to_address,
            msg=f"Subject:{subject}\n\n{message_body}".encode('utf-8')
        )
else:
    print("Price ain't drop yet, chief!")                         # Fallback print in case the price
                                                                  # hasn't dropped - or worse -
                                                                  # has risen!



