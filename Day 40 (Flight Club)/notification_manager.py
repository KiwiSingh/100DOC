import base64
import os
import smtplib

user_email_b64 = "cGFydGhhc2FyYXRoaS5zaW5naEBnbWFpbC5jb20="
user_email = base64.b64decode(user_email_b64).decode("utf-8")


class NotificationManager:
    def __init__(self):
        self.email = user_email
        self.password = os.getenv("SMTP_PASSWORD")

    def send_email(self, to_address, subject, body):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(self.email, self.password)
            connection.sendmail(
                from_addr=self.email,
                to_addrs=to_address,
                msg=f"Subject:{subject}\n\n{body}".encode('utf-8')
            )