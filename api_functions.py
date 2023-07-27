import requests
import json
import parser


def get_current_price_using_parsing(seller_id):
    """Before calling this function you need to add cookies to cookies.csv
       from page where you already logged in wildberries.ru
    """
    parser.get_html_page(seller_id)
    data = parser.parse()
    parser.save_json(data)


def get_current_price_using_api(headers_get):
    """Создает json файл с текущей информацией о товарах  обращаесь к API"""
    response = requests.get('https://suppliers-api.wildberries.ru/public/api/v1/info', headers=headers_get)

    if response.status_code == 200:
        current_prices = response.json()
        id_and_prices_only = []

        for item in current_prices:
            id_price = {
                'nmId': item['nmId'],
                'price': item['price'],
                'discount': item['discount']
            }
            id_and_prices_only.append(id_price)

        sorted_data = sorted(id_and_prices_only, key=lambda x: x['nmId'])
        parser.save_json(sorted_data)


def change_current_price_to_target_price_in_json(current_data, target_data) -> None:
    """Сравниевает действующую цену со скидкой и ставит нужную цену"""
    future_data = []
    for item in range(len(current_data)):
        
        cd_nmId = current_data[item]['nmId']
        cd_price = current_data[item]['price']
        cd_discount = current_data[item]['discount']

        td_nmId = target_data[item]['nmId']
        td_price = target_data[item]['price']

        # cd_price_with_discount = int(cd_price - (cd_price * (cd_discount/100)))

        if td_nmId == cd_nmId:
            needed_price = int(td_price / (1 - (cd_discount / 100)))
            future_item = {
                'nmId': td_nmId,
                'price': needed_price
            }
            future_data.append(future_item)
        else:
            print('error cd_nmId != td_nmId')
            break
    with open('future_data.json', 'w') as fd:
        json.dump(future_data, fd, indent=4)


def send_changed_data(headers_post, fd_data):
    """Отправляет измененный файл с ценнами файл для изменений"""
    response = requests.post('https://suppliers-api.wildberries.ru/public/api/v1/prices',
                             headers=headers_post, data=fd_data)

    if response.status_code == 200:
        print('Запрос успешно выполнен')
    else:
        print('Произошла ошибка при выполнении запроса\n')
        print('Response text:', response.text)
