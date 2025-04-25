import time #### Импортируем модуль со временем
import csv #### Импортируем модуль csv
from selenium import webdriver #### Импортируем Selenium
from selenium.webdriver.common.by import By

driver = webdriver.Firefox() #### Инициализируем браузер
url = "https://tomsk.hh.ru/vacancies/programmist" #### В отдельной переменной указываем сайт, который будем просматривать
driver.get(url) #### Открываем веб-страницу
time.sleep(3) #### Задаём 3 секунды ожидания, чтобы веб-страница успела прогрузиться

#### Находим все карточки с вакансиями с помощью названия класса
vacancies = driver.find_elements(By.CLASS_NAME, 'vacancy-card--H8LvOiOGPll0jZvYpxIF') # Названия классов берём с кода сайта

print(vacancies) #### Выводим вакансии на экран

parsed_data = [] #### Создаём список, в который потом всё будет сохраняться

#### Перебираем коллекцию вакансий
for vacancy in vacancies: #### Используем конструкцию try-except, чтобы "ловить" ошибки, как только они появляются
   try:
       #### Находим элементы внутри вакансий по значению
        title = vacancy.find_element(By.CSS_SELECTOR, 'span.vacancy-name--SYbxrgpHgHedVTkgI_cA').text #### Находим названия вакансии
        company = vacancy.find_element(By.CSS_SELECTOR, 'span.company-info-text--O32pGCRW0YDmp3BHuNOP').text #### Находим названия компаний
        salary = vacancy.find_element(By.CSS_SELECTOR, 'span.compensation-text--cCPBXayRjn5GuLFWhGTJ').text #### Находим зарплаты
        link = vacancy.find_element(By.CSS_SELECTOR, 'a.bloko-link').get_attribute('href') #### Находим ссылку с помощью атрибута 'href'
   except: #### Вставляем блок except на случай ошибки - в случае ошибки программа попытается продолжать
        print(f"Произошла ошибка при парсинге")
        continue

    parsed_data.append([title, company, salary, link]) #### Вносим найденную информацию в список

driver.quit() #### Закрываем подключение браузер

#### Прописываем открытие нового файла, задаём ему название и форматирование
#### 'w' означает режим доступа, мы разрешаем вносить данные в таблицу
with open("hh.csv", 'w',newline='', encoding='utf-8') as file:
    #### Используем модуль csv и настраиваем запись данных в виде таблицы
    writer = csv.writer(file) #### Создаём объект
    writer.writerow(['Название вакансии', 'название компании', 'зарплата', 'ссылка на вакансию']) #### Создаём первый ряд
    writer.writerows(parsed_data) #### Прописываем использование списка как источника для рядов таблицы