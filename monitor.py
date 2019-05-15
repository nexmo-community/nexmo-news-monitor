from dotenv import load_dotenv
import os
from os.path import join, dirname
import re
import requests
from bs4 import BeautifulSoup
import time
from SMSClient import SMSClient

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# app configuration
SITE_URL = os.getenv("SITE_URL")
SITE_NAME = os.getenv("SITE_NAME")
SEARCH_KEYWORD = os.getenv("SEARCH_KEYWORD")
POLL_INTERVAL = os.getenv("POLL_INTERVAL")
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

# messaging
MESSAGES_APPLICATION_ID = os.getenv("MESSAGES_APPLICATION_ID")
MESSAGES_KEY_FILE = os.getenv("MESSAGES_KEY_FILE")
TO_NUMBER = os.getenv("TO_NUMBER")
FROM_NUMBER = os.getenv("FROM_NUMBER")
JWT_EXPIRY = 1*60*60  # JWT expires after one hour (default is 15 minutes)

sms = SMSClient(MESSAGES_APPLICATION_ID, MESSAGES_KEY_FILE, JWT_EXPIRY)
print(sms.app_id)

def isUrl(text):
    pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    match = re.search(pattern, text)
    if match:
      return True
    else:
      return False

while True:

    # Check if using website URL or local file for testing
    if(isUrl(SITE_URL)):
        response = requests.get(SITE_URL, headers=REQUEST_HEADERS)
        soup = BeautifulSoup(response.text, "lxml")
    else:
        soup = BeautifulSoup(open(SITE_URL), "lxml")

    # if search term not found, wait for the poll interval and run again
    if str(soup).find(SEARCH_KEYWORD) == -1:
        time.sleep(int(POLL_INTERVAL))
        print('Nothing found...')
        continue

    else:
        msg = "Your search term *" + SEARCH_KEYWORD + "* was mentioned on " + SITE_NAME + "!"
        sms.send_message(FROM_NUMBER, TO_NUMBER, msg)
        break
