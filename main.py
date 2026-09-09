import os
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
    "function" : "GLOBAL_QUOTE",
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
    change_in_percentage = float(data["Global Quote"]["10. change percent"].split("%")[0])
    if abs(change_in_percentage) > STOCK_FLUCTUATION_THRESHOLD:
        return change_in_percentage
    return "No major fluctuations"
def main():

#TODO:When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
    stock_percentage = get_stock_price_data()
    print(stock_percentage)

main()
