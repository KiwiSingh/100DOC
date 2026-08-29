from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import smtplib
import base64
import html
import os

user_email_b64 = "cGFydGhhc2FyYXRoaS5zaW5naEBnbWFpbC5jb20="
user_email = base64.b64decode(user_email_b64).decode("utf-8")
password = os.getenv("SMTP_PASSWORD")
to_address_b64 = "bWV0YWwuZ2FydXJ1d2luZC50ZXR1c2FpZ2EyMjNAZ21haWwuY29t"
to_address = base64.b64decode(to_address_b64).decode("utf-8")
subject = "Amazon Price Alert!"
PRODUCT_URL = "https://www.amazon.in/Western-Digital-Drive-3-5Inch-Encryption-Protection/dp/B08SMCPP58" 
TARGET_PRICE = 50000


comet_binary = "/Volumes/Zweidrive/Applications/Comet.app/Contents/MacOS/Comet"

options = Options()
options.binary_location = comet_binary
service = Service()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)
driver.get(PRODUCT_URL)
price_rupees = float(driver.find_element(By.CLASS_NAME, value="a-price-whole").text.replace(",", ""))
product_title = html.unescape((driver.find_element(By.ID, value="productTitle")).text)
message_body = f"{product_title} is now ₹{price_rupees}\n{PRODUCT_URL}"

if price_rupees <= TARGET_PRICE:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user_email, password)
        connection.sendmail(
            from_addr=user_email,
            to_addrs=to_address,
            msg=f"Subject:{subject}\n\n{message_body}".encode('utf-8')
        )
else:
    print("Price ain't drop yet, chief!")

driver.quit()                  
