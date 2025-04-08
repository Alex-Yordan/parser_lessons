import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import asyncio

def get_english_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        return {
            "english_word": soup.find("div", id="random_word").text.strip(),
            "word_definition": soup.find("div", id="random_word_definition").text.strip()
        }
    except Exception as e:
        print(f"Ошибка получения данных: {e}")
        return None

async def translate_to_russian(text):
    translator = Translator()
    try:
        # Используем асинхронный вызов
        translation = await translator.translate(text, src='en', dest='ru')
        return translation.text
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return None

def word_game():
    print("Добро пожаловать в игру!")
    while True:
        word_data = get_english_words()
        if not word_data:
            print("Ошибка получения слова. Повторная попытка...")
            continue

        en_word = word_data["english_word"]
        en_def = word_data["word_definition"]

        # Запускаем асинхронный перевод в синхронном коде
        ru_word = asyncio.run(translate_to_russian(en_word))
        ru_def = asyncio.run(translate_to_russian(en_def))

        if not ru_word or not ru_def:
            print("Ошибка перевода. Повторная попытка...")
            continue

        print(f"\nЗначение: {ru_def}")
        guess = input("Какое это слово? ").strip().lower()

        if guess == ru_word.lower():
            print("Правильно!")
        else:
            print(f"Неверно! Правильный ответ: {ru_word}")

        if input("\nЕщё раз? (y/n): ").lower() != 'y':
            print("Спасибо за игру!")
            break

word_game()