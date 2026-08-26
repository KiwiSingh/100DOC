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
        self.connection = smtplib.SMTP("smtp.gmail.com", 587)

    def send_emails(self, email_list, email_body):
        with self.connection:
            self.connection.starttls()
            self.connection.login(self.email, self.password)
            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )

