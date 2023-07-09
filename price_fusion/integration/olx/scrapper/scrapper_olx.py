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


options = Options()
options.add_argument("--headless")
# options.page_load_strategy = 'none'
options.page_load_strategy = 'eager'
# options.page_load_strategy = 'normal'

options.add_argument("--window-size=1366,768")


driver = webdriver.Chrome(options=options)




# driver = webdriver.Chrome()
# driver.maximize_window()

url = 'https://sp.olx.com.br/sao-paulo-e-regiao/imoveis/apartamento-para-aluguel-oswaldo-cruz-1-quarto-40-m2-1203925481'



code = '1202138303'
url_main = 'https://www.olx.com.br/'


driver.get(url_main)

search = driver.find_element(By.ID, 'searchtext-input')
search.send_keys(code)
search.send_keys(Keys.RETURN)

# original_window = driver.current_window_handle


# content = driver.find_element(By.ID, 'content')

original_window = driver.current_window_handle

# driver.get_screenshot_as_file("screenshot.png")

WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "//a[contains(@href, '{}')]".format(code))).click()

# WebDriverWait(driver, timeout=2).until(EC.number_of_windows_to_be(2))

for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break



# div = content.
# driver.find_element(By.XPATH, "//*[starts-with(@id, 'profileCard') and contains(@id, 'EDUCATION-en-US')]").text
# price_symbol = driver.find_element(By.CSS_SELECTOR, "[id^='R$']")

price_symbol = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "//h2[contains(text(), 'R$')]"))


# price_symbol = driver.find_element(By.XPATH, "//h2[contains(text(), 'R$')]")
parent = price_symbol.find_element(By.XPATH, "..")

price = parent.find_elements(By.XPATH, '*')[1]

# print(price)

priceText = price.text
price = priceText.replace('.', '')

# driver.get_screenshot_as_file("screenshot.png")


# print(priceText)
priceNumber = int(price)
print(priceNumber)
# [starts-with(@id, 'frag-') and ends-with(@id, '-0')]



def find_flat_property(property):
    condominio_label = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.XPATH, "//span[text()='{}']".format(property)))

    # condominio_label = driver.find_element(By.XPATH, "//span[text()='{}']".format(property))
    parent = condominio_label.find_element(By.XPATH, "..")
    # print(condominio_label.text)
    condominio_price_span = parent.find_elements(By.XPATH, '*')[1]
    condominio_price_text = condominio_price_span.text
    condominio_price_text = condominio_price_text.replace('$', '')
    condominio_price_text = re.sub('[a-zA-Z$. ]', '', condominio_price_text)
    # print(condominio_price_text)
    return condominio_price_text


print(find_flat_property('Condomínio'))
print(find_flat_property('IPTU'))