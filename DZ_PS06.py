import time #### Импортируем модуль со временем
import csv #### Импортируем модуль csv
from selenium import webdriver #### Импортируем Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox() #### Инициализируем браузер
url = "https://www.divan.ru/volgograd/category/svet" #### В отдельной переменной указываем сайт, который будем просматривать
driver.get(url) #### Открываем веб-страницу

try:  #### Ожидаем загрузку карточек товаров
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'LlPhw'))
    )
except Exception as e:
    print(f"Ошибка при загрузке страницы: {str(e)}")
    driver.quit()
    exit()

#### Находим все карточки с помощью названия класса
svets = driver.find_elements(By.CLASS_NAME, 'LlPhw') #### Названия классов берём с кода сайта

print(svets) #### Выводим на экран товары

parsed_data = [] #### Создаём список, в который потом всё будет сохраняться

for svet in svets:
    try:
        name = svet.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]').text #### Находим названия товара
        price = svet.find_element(By.CSS_SELECTOR, 'span.ui-LD-ZU.KIkOH').text.replace('руб.', '').strip() #### Находим цену товара
        link = svet.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8.qUioe.ProductName.ActiveProduct').get_attribute('href') #### Находим ссылку с помощью атрибута 'href'

        print(f"Название: {name}, Цена: {price}, Ссылка: {link}") #### Выводим отладочную информацию

        parsed_data.append([name, price, link])  #### Вносим найденную информацию в список

    except:  #### Вставляем блок except на случай ошибки - в случае ошибки программа попытается продолжать
        print(f"Произошла ошибка при парсинге")
        continue


driver.quit() #### Закрываем подключение браузер

#### Прописываем открытие нового файла, задаём ему название и форматирование
#### 'w' означает режим доступа, мы разрешаем вносить данные в таблицу
with open("svet.csv", 'w',newline='', encoding='utf-8-sig') as file:
    #### Используем модуль csv и настраиваем запись данных в виде таблицы
    writer = csv.writer(file) #### Создаём объект
    writer.writerow(['Название товара', 'Цена товара', 'Ссылка на товар']) #### Создаём первый ряд
    writer.writerows(parsed_data) #### Прописываем использование списка как источника для рядов таблицы

print("Парсинг завершен. Данные сохранены в файл svet.csv.")  #### Отчет