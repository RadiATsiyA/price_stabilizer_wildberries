import requests
import json
import time
import os
from dotenv import load_dotenv
from api_functions import (get_current_price_using_api, change_current_price_to_target_price_in_json,
                           send_changed_data, get_current_price_using_parsing)

load_dotenv()

WB_TOKEN = os.getenv("WB_TOKEN")


headers_get = {
    'Authorization': f'Bearer {WB_TOKEN}'
}
# response = requests.get(url, headers=headers_get)

headers_post = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {WB_TOKEN}'
}
# response = requests.post(url, data=json_data, headers=headers_post)

# ---------------------STARTBLOCK-------------------------------------------------
"""Блок который получает текущие данныe с магазина, меняет их
    на нужные и отпавляет запрос на изменение цен"""

# get_current_price_using_api(headers_get)
get_current_price_using_parsing(seller_id=1195494)

with open('target_prices.json') as tp:
    target_data = json.load(tp)

with open('current_prices.json') as cp:
    current_data = json.load(cp)

change_current_price_to_target_price_in_json(current_data, target_data)

with open('future_data.json') as fd:
    fdata = json.load(fd)
    fd_data = json.dumps(fdata)

time.sleep(3)

send_changed_data(headers_post, fd_data)

# ----------------------ENDBLOCK---------------------------------------------------

