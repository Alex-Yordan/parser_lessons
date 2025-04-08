from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time


def search_wikipedia(query):
    return f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"


def get_paragraphs(driver):
    return driver.find_elements(By.CSS_SELECTOR, "#mw-content-text p")


def get_internal_links(driver):
    # Используем явное ожидание для загрузки ссылок
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#mw-content-text a"))
    )
    return [
        {
            "text": a.text,
            "href": a.get_attribute("href")
        }
        for a in driver.find_elements(By.CSS_SELECTOR, "#mw-content-text a[href^='/wiki/']")
        if a.text.strip()  # Фильтруем пустые ссылки
    ]


def show_menu():
    print("\nВыберите действие:")
    print("1. Листать параграфы текущей статьи")
    print("2. Перейти на связанную страницу")
    print("3. Выйти из программы")


def show_paragraphs(paragraphs):
    for i, p in enumerate(paragraphs, 1):
        print(f"\n--- Параграф {i} ---")
        print(p.text)
        if i < len(paragraphs):
            input("Нажмите Enter для следующего параграфа...")


def choose_link(links):
    print("\nДоступные ссылки:")
    for idx, link in enumerate(links[:10], 1):
        print(f"{idx}. {link['text']}")

    while True:
        try:
            choice = int(input("Введите номер ссылки: "))
            if 1 <= choice <= len(links[:10]):
                return links[choice - 1]['href']
            else:
                print("Неверный номер!")
        except ValueError:
            print("Введите число!")


def main():
    driver = webdriver.Firefox()

    try:
        query = input("Введите поисковый запрос для Википедии: ")
        driver.get(search_wikipedia(query))

        if "Страница не существует" in driver.page_source:
            print("Статья не найдена!")
            return

        while True:
            show_menu()
            action = input("Ваш выбор: ")

            if action == '1':
                paragraphs = get_paragraphs(driver)
                if not paragraphs:
                    print("Параграфы не найдены!")
                    continue
                show_paragraphs(paragraphs)

            elif action == '2':
                links = get_internal_links(driver)
                if not links:
                    print("Ссылки не найдены!")
                    continue

                url = choose_link(links)
                if url:
                    print(f"Переход на: {url}")
                    driver.get(url)
                    # Ждем полной загрузки новой страницы
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )

            elif action == '3':
                print("Завершение работы...")
                break

            else:
                print("Неверный ввод!")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()