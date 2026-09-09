import os
from requests_cache import CachedSession
import requests
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# create a cache of the for the API requests
session = CachedSession("api_cache", expire_after=(360*3))

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_FLUCTUATION_THRESHOLD = 3

STOCK_INFO_API_KEY = os.getenv("ALPHA_VANTAGE_TRADING_API")
NEWS_API_KEY = os.getenv("NEWSAPI.ORG_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_KEY = os.getenv("TELEGRAM_ACCESS_TOKEN")

STOCK_INFO_API_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
TELEGRAM_API_ENDPOINT = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"



# put checks in case there is any issue with loading the env variables
if STOCK_INFO_API_KEY is None: raise ValueError("Couldn't load the STOCK_INFO_API_KEY from .env please check the file or add the API key")
if NEWS_API_KEY is None: raise ValueError("Couldn't load the NEWS_API_KEY from .env please check the file or add the API key")
if TELEGRAM_CHAT_ID is None: raise ValueError("Couldn't load the TELEGRAM_CHAT_ID from .env please check the file or add the API key")
if TELEGRAM_API_KEY is None: raise ValueError("Couldn't load the TELEGRAM_API_KEY from .env please check the file or add the API key")




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
    """If the stock percentage cross the threshold then return the percentage and the dates that covered"""
    stock_api_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": STOCK_INFO_API_KEY
    }
    response = session.get(STOCK_INFO_API_ENDPOINT, params=stock_api_params)
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

def get_news(last_traded_day, day_before_last_traded_day):
    """Return the news data from the within the given dates"""
    news_api_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
        "from": day_before_last_traded_day,
        "to": last_traded_day,
        "language" : "en",

    }
    response = session.get(NEWS_API_ENDPOINT, params=news_api_params)
    response.raise_for_status()
    data = response.json()
    return data["articles"][:3]

def send_telegram_message(text):
    """Send the text parameter via telegram"""
    param = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_notification": False,
    }
    response = requests.get(TELEGRAM_API_ENDPOINT, params=param)
    print("Message Sent Successfully" if response.status_code == 200 else "Something Went Wrong")
    response.raise_for_status()



def main():

    #TODO-1:When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
    result = get_stock_price_data()
    if result is not None:
        change_in_percentage, last_traded_day, day_before_last_traded_day = result

        #TODO-2:Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
        news = get_news(last_traded_day,day_before_last_traded_day)
        percentage = f"{STOCK}: {"🔺" if change_in_percentage > 0 else "🔻"} {change_in_percentage} %"
        for items in news:
            text = f"{percentage}\nHeadline:{items["title"]}\nBrief:{items["content"]}\nURL:{items["url"]}\n"
            #TODO-3:Send a seperate message with the percentage change and each article's title and description to your phone number.
            send_telegram_message(text)

main()
