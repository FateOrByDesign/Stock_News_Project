import os
from logging import lastResort

import requests
from dotenv import load_dotenv

# load environment variables
load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_FLUCTUATION_THRESHOLD = 3
STOCK_INFO_API_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_INFO_API_KEY = os.getenv("ALPHA_VANTAGE_TRADING_API")
if not STOCK_INFO_API_KEY: raise ValueError("Couldn't load the STOCK_INFO_API_KEY from .env please check the file or add the API key")

STOCK_API_PARAMS = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey" : STOCK_INFO_API_KEY
}


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


def get_stock_price_data():
    response = requests.get(STOCK_INFO_API_ENDPOINT, params=STOCK_API_PARAMS)
    response.raise_for_status()
    data = response.json()
    # get the last trading day and the day before that in order
    dates_to_look_into= list(data["Time Series (Daily)"].keys())[:2]
    stock_data = {}
    for key in dates_to_look_into:
        stock_data[key] = data["Time Series (Daily)"][key]
    # from the last trading day and the day before that calculate the percentage
    last_trading_day_closing_value = float(stock_data[dates_to_look_into[0]]['4. close'])
    day_before_last_trading_day_closing_value = float(stock_data[dates_to_look_into[1]]['4. close'])
    change_in_percentage = (last_trading_day_closing_value  - day_before_last_trading_day_closing_value) / day_before_last_trading_day_closing_value * 100
    change_in_percentage = round(change_in_percentage, 3)
    # check if the change in percentage is greater than the stock threshold
    if abs(change_in_percentage) > STOCK_FLUCTUATION_THRESHOLD:
        return (change_in_percentage, dates_to_look_into[0], dates_to_look_into[1])
    return None
def main():

#TODO:When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
    result = get_stock_price_data()
    if result is not None:
        change_in_percentage, last_traded_day, day_before_last_traded_day = result
        print(change_in_percentage,last_traded_day,day_before_last_traded_day)


main()
