from flask import Flask, render_template, request
import requests
from datetime import datetime
import smtplib
import base64
import os


posts = requests.get("https://api.npoint.io/8affa6f091a4887c6697").json()
user_email_b64 = "cGFydGhhc2FyYXRoaS5zaW5naEBnbWFpbC5jb20="
OWN_EMAIL = base64.b64decode(user_email_b64).decode("utf-8")
OWN_PASSWORD=os.getenv("SMTP_PASSWORD")

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.context_processor
def inject_now():
    return {'year': datetime.now().year}


if __name__ == "__main__":
    app.run(debug=True, port=5001)