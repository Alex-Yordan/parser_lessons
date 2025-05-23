from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
import random

browser = webdriver.Firefox()
browser.get("https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D0%BB%D0%BD%D0%B5%D1%87%D0%BD%D0%B0%D1%8F_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0")

time.sleep(3)
hatnotes = []

for element in browser.find_elements(By.XPATH, "//div[contains(@class, 'hatnote')]"):
    if "navigation-not-searchable" in element.get_attribute("class"):
        hatnotes.append(element)
        print(f"Найден элемент: {element.text}")  # Отладочный вывод


print(hatnotes)

hatnote = random.choice(hatnotes)
link = hatnote.find_element(By.TAG_NAME, "a").get_attribute("href")
browser.get(link)