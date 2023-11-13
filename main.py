from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import smtplib
import os

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
AMAZON_URL = "https://www.amazon.com/dp/B08VKQPR7H/ref=twister_B0B16HQ7NW?_encoding=UTF8&psc=1"
BOI_URL = "https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/"
PRICE_TARGET = 750

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(AMAZON_URL)
product_price = float(driver.find_element(By.CSS_SELECTOR, ".a-price span[aria-hidden]").text.strip("$"))
product_title = driver.find_element(By.ID, "productTitle").text

boi_response = requests.get(BOI_URL)
boi_html = boi_response.text
soup = BeautifulSoup(boi_html, "html.parser")
exchange_rate = float(soup.select_one(selector="td[data-search='USD'] + td").getText())
product_price_nis = round(product_price * exchange_rate, 2)

if product_price_nis <= PRICE_TARGET:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL,
                            msg=f"Subject:Amazon Price Alert!\n\n"
                                f"{product_title} is now {product_price_nis} NIS!\n{AMAZON_URL}")
