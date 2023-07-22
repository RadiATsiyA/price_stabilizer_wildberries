import requests
import json
import time
import os
from dotenv import load_dotenv
from api_functions import get_current_price, change_current_price_to_target_price_in_json, send_changed_data

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
"""Блок который получает текущие данный с магазина, потом меняет их
    на нужные и отпавляет запрос на изменение цен"""

# get_current_price(headers_get)
#
# with open('target_prices.json') as tp:
#     target_data = json.load(tp)
#
# with open('current_prices.json') as cp:
#     current_data = json.load(cp)
#
# change_current_price_to_target_price_in_json(current_data, target_data)
#
# with open('future_data.json') as fd:
#     fdata = json.load(fd)
#     fd_data = json.dumps(fdata)
#
# time.sleep(5)
#
# send_changed_data(headers_post, fd_data)

# ----------------------ENDBLOCK---------------------------------------------------

