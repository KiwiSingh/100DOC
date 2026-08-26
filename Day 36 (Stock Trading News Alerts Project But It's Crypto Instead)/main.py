PRODUCT = "ETH-USDT"
import os
import requests
import smtplib
import base64

user_email_b64 = "cGFydGhhc2FyYXRoaS5zaW5naEBnbWFpbC5jb20="
user_email = base64.b64decode(user_email_b64).decode("utf-8")
password = os.getenv("SMTP_PASSWORD")
## STEP 1: I'm gonna use Coinbase instead, sorry mate.

CB_URL = f"https://api.exchange.coinbase.com/products/{PRODUCT}/candles"
parameters = {
    "granularity": 86400, # intraday
    "limit": 3 # last 3 daily candles
}

cb_resp = requests.get(CB_URL, params=parameters, timeout=10)
cb_resp.raise_for_status()
candles = cb_resp.json()

yday_close = float(candles[1][4])
dby_close = float(candles[2][4])

pct_change = (yday_close - dby_close) / dby_close * 100



## STEP 2: I'm gonna use cryptocurrency.cv instead because it has no auth
CV_URL_BASE = "https://cryptocurrency.cv"
TICKER = PRODUCT.split("-")[0]
CV_URL = f"{CV_URL_BASE}/api/news"
cv_parameters = {
    "tickers": TICKER
}
if pct_change >= 5 or pct_change <= -5:
    cv_resp = requests.get(CV_URL, params=cv_parameters, timeout=10)
    cv_resp.raise_for_status()
    cv_news_data = cv_resp.json()
    cv_articles = cv_news_data.get("articles", [])[:2] # So that we don't get more than 2 articles lol
    message_body = ""
    for a in cv_articles:
        if pct_change >= 5:
            message_body += f"ETH: 🔺{pct_change}%\n"
        elif pct_change <= -5:
            message_body +=f"ETH: 🔻{pct_change}%\n"
        message_body += f"- {a['title']} [{a['source']}]\n"
        message_body += f"  {a['url']}\n\n"


## STEP 3: Gonna use SMTPLib to send myself an email instead lol
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=user_email, password=password)
        connection.sendmail(from_addr=user_email, to_addrs="char1ot33r@icloud.com", msg=f"Subject: ETH Price Movement Alert\n\n{message_body}")



