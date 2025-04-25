import time #### Импортируем модуль со временем
import csv #### Импортируем модуль csv
from selenium import webdriver #### Импортируем Selenium
from selenium.webdriver.common.by import By

driver = webdriver.Firefox() #### Инициализируем браузер
url = "https://www.vseinstrumenti.ru/category/lyustry-4460/" #### В отдельной переменной указываем сайт, который будем просматривать
driver.get(url) #### Открываем веб-страницу
time.sleep(15) #### Задаём 5 секунды ожидания, чтобы веб-страница успела прогрузиться

#### Находим все карточки с помощью названия класса
svets = driver.find_elements(By.CLASS_NAME, 'dGMJLz') #### Названия классов берём с кода сайта

print(svets) #### Выводим на экран товары

parsed_data = [] #### Создаём список, в который потом всё будет сохраняться

for svet in svets:
    try:
        name = svet.find_element(By.CSS_SELECTOR, 'a[data-qa="product-name"]').get_attribute('title') #### Находим названия товара
        price = svet.find_element(By.CSS_SELECTOR, 'p[data-qa="product-price-current"]').text.strip() #### Находим цену товара
        link = svet.find_element(By.CSS_SELECTOR, 'a.-dp5Dd').get_attribute('href') #### Находим ссылку с помощью атрибута 'href'
    except:  #### Вставляем блок except на случай ошибки - в случае ошибки программа попытается продолжать
        print(f"Произошла ошибка при парсинге")
        continue

    parsed_data.append([name, price, link])  #### Вносим найденную информацию в список

driver.quit() #### Закрываем подключение браузер

#### Прописываем открытие нового файла, задаём ему название и форматирование
#### 'w' означает режим доступа, мы разрешаем вносить данные в таблицу
with open("svet.csv", 'w',newline='', encoding='utf-8-sig') as file:
    #### Используем модуль csv и настраиваем запись данных в виде таблицы
    writer = csv.writer(file) #### Создаём объект
    writer.writerow(['Название товара', 'Цена товара', 'Ссылка на товар']) #### Создаём первый ряд
    writer.writerows(parsed_data) #### Прописываем использование списка как источника для рядов таблицы

print("Парсинг завершен. Данные сохранены в файл svet.csv.")