import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация браузера
driver = webdriver.Firefox()
url = "https://www.divan.ru/volgograd/category/svet"
driver.get(url)

# Ожидаем загрузку карточек товаров
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'LlPhw'))
    )
except Exception as e:
    print(f"Ошибка при загрузке страницы: {str(e)}")
    driver.quit()
    exit()

# Находим все карточки товаров
svets = driver.find_elements(By.CLASS_NAME, '_Ud0k')

if not svets:
    print("Товары не найдены!")
    driver.quit()
    exit()

parsed_data = []

for svet in svets:
    try:
        # Извлекаем название товара
        name = svet.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]').text

        # Извлекаем цену товара
        price = svet.find_element(By.CSS_SELECTOR, 'span[data-testid="price"]').text

        # Извлекаем ссылку на товар
        link = svet.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8.qUioe.ProductName.ActiveProduct').get_attribute('href')

        # Выводим отладочную информацию
        print(f"Название: {name}, Цена: {price}, Ссылка: {link}")

        # Добавляем данные в список
        parsed_data.append([name, price, link])

    except Exception as e:
        print(f"Ошибка при парсинге элемента: {str(e)}")
        continue

# Сохранение данных в CSV с кодировкой UTF-8 и BOM
with open("svet.csv", 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Название товара', 'Цена товара', 'Ссылка на товар'])
    writer.writerows(parsed_data)

# Закрываем браузер
driver.quit()

print("Парсинг завершен. Данные сохранены в файл svet.csv.")