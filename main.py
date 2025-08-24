import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from test_automation import TestAutomation
from config import LEVEL_UP_URL


def main():
    """
    Скрипт проходит тест "Царь горы".
    Отвечает на имеющиеся вопросы с ответами в question.py
    Сохраняет вопросы без ответов в custom_question.txt

    TODO: написать функционал для прохождения "Вопрос дня"
    """

    # настройки браузера (опционально)
    options = Options()

    # инициализация браузера и запуск основного функционала
    with webdriver.Chrome(options=options) as driver:
        driver.get(LEVEL_UP_URL)
        level_up = TestAutomation(driver)

        level_up.run_automation()


if __name__ == "__main__":
    main() 