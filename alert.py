import time
import yfinance as yf
from twilio.rest import Client
import os

stocks = ['AAPL', 'NVDA', 'META']
upper_limit = [286, 205, 612]
lower_limit = [283, 203, 611]

account_sid = os.getenv("TWILIO_ACCOUNT_SID")

auth_token = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)


def send_sms(message):
    print(f"\n {message}")
    client.messages.create(
        
        messaging_service_sid=os.getenv("Service"),
        to=os.getenv("Number"),
        body=message
    )

while True:
    prices = []
    for ticker in stocks:
        data = yf.Ticker(ticker)
        price = data.fast_info['last_price']
        prices.append(price)
        print(f"{ticker}: ${price:.2f}")

    for i in range(len(stocks)):
        if prices[i] > upper_limit[i]:
            send_sms(f"{stocks[i]} is at ${prices[i]:.2f}. You might want to sell!")
        elif prices[i] < lower_limit[i]:
            send_sms(f"{stocks[i]} is at ${prices[i]:.2f}. You might want to buy!")

    time.sleep(60)