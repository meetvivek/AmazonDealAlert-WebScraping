from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get sensitive information from environment variables
MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("PASSWORD")
TARGET_PRICE = int(os.getenv("TARGET_PRICE"))

URL = ("https://www.amazon.in/Samsung-Galaxy-Smartphone-Marble-Storage/dp/B0CS69DGSW?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&smid=A1EWEIV3F4B24B")

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 "
                  "Safari/537.36",
    "Accept-Language": "en-US,en;q=0.8"
}

response = requests.get(url=URL, headers=HEADER)
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

price = int(soup.find(name="span", class_="a-price-whole").getText().replace(",", "").split('.')[0])
title = soup.find(name="span", class_="a-size-large product-title-word-break").getText().strip()

if price <= TARGET_PRICE:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: AMAZON PRICE ALERT\n\n{title}, is\nnow Rs. {price}.\n\n{URL}"
        )
