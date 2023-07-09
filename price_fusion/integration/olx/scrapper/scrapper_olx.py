from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


MAIN_URL = 'https://www.olx.com.br/'

def get_product_details_from_olx(code, details):
    
    driver = get_driver()
    search_product(driver=driver, code=code)
    go_to_product_page(driver=driver, code=code)

    result = {
        'price': retrieve_price(driver)
    }

    try:
        for property in details:
            value = find_product_property(driver, property)
            result[property] = value
    except:
        print('Property not found')

    return result



def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.page_load_strategy = 'eager'
    options.add_argument("--window-size=1366,768")
    driver = webdriver.Chrome(options=options)
    return driver



def search_product(driver, code):
    driver.get(MAIN_URL)
    search = driver.find_element(By.ID, 'searchtext-input')
    search.send_keys(code)
    search.send_keys(Keys.RETURN)



def go_to_product_page(driver, code):
    original_window = driver.current_window_handle
    WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "//a[contains(@href, '{}')]".format(code))).click()

    for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break


def retrieve_price(driver):
    price_symbol = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "//h2[contains(text(), 'R$')]"))
    parent = price_symbol.find_element(By.XPATH, "..")
    price = parent.find_elements(By.XPATH, '*')[1]
    priceText = price.text
    price = priceText.replace('.', '')
    price_number = int(price)
    return price_number



def find_product_property(driver, property):
    condominio_label = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.XPATH, "//span[text()='{}']".format(property)))
    parent = condominio_label.find_element(By.XPATH, "..")
    condominio_price_span = parent.find_elements(By.XPATH, '*')[1]
    condominio_price_text = condominio_price_span.text
    condominio_price_text = condominio_price_text.replace('$', '')
    condominio_price_text = re.sub('[a-zA-Z$. ]', '', condominio_price_text)
    return condominio_price_text


print(get_product_details_from_olx('1187613353', ['Condomínio', 'IPTU']))