import os
import base64
import smtplib

user_email_b64 = "cGFydGhhc2FyYXRoaS5zaW5naEBnbWFpbC5jb20="
user_email = base64.b64decode(user_email_b64).decode("utf-8")
password = os.getenv("SMTP_PASSWORD")

class NotificationManager:
    def __init__(self):
        self.email = user_email
        self.password = password

    def send_email(self, message_body):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(self.email, self.password)
            connection.sendmail(from_addr=self.email, to_addrs="char1ot33r@icloud.com", msg=f"Subject: New Flight Deal Found\n\n{message_body}")

