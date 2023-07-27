from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from csv import DictReader
import time
import json


def get_cookies():
    """Getting cookies for authorization to get real price
        (only logged in clients have discounts up to 30%)
        You need to get cookies manually from your browser and paste them in cookies.csv
    """
    with open('cookies.csv') as f:
        dict_reader = DictReader(f)
        list_of_dict = list(dict_reader)
    return list_of_dict


def get_html_page(seller_id):
    """Opening firefox and wildberries' seller's page and save page for scrapping"""
    driver = webdriver.Firefox()
    try:
        driver.maximize_window()
        driver.get(f'https://www.wildberries.ru/seller/{seller_id}')
        time.sleep(2)
        cookie = get_cookies()

        for i in cookie:
            driver.add_cookie(i)
        driver.refresh()
        time.sleep(3)

        num_scrolls = 8
        for _ in range(num_scrolls):
            footer_element = driver.find_element(By.ID, 'footer')
            if footer_element:
                driver.execute_script("arguments[0].scrollIntoView();", footer_element)
                time.sleep(5)
        with open('page.html', 'w') as f:
            f.write(driver.page_source)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        driver.quit()


def save_json(data: list):
    """just save json with data"""
    with open('current_prices.json', 'w') as file:
        json.dump(data, file, indent=4)


def parse():
    """Parsing html page
      return list of prices with discount and product's id
    """
    with open('page.html', 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    data = []

    all_products = soup.find_all('article', class_='product-card product-card--hoverable j-card-item')
    for product in all_products:
        id_product = product.get('data-nm-id').strip()
        real_price = product.find('ins', class_='price__lower-price').text.strip().replace(' ', '').replace('₽', '')
        discount = product.find('p', class_='product-card__tip product-card__tip--sale').text.replace('-', '').replace('%', '')
        data.append({
            'nmId': id_product,
            'price': real_price,
            'discount': discount
        })
    sorted_data = sorted(data, key=lambda x: x['nmId'])
    print(len(sorted_data))
    return sorted_data
