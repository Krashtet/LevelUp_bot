import random

# Конфигурация проекта
LEVEL_UP_URL = 'https://levelup.t2.ru/'

# Настройки браузера
BROWSER_CONFIG = {
    "implicit_wait": 10,
    "page_load_timeout": 30,
    "window_size": (1920, 1080)
}

# CSS селекторы для элементов на странице
SELECTORS = {
    "start_game": "//div[@class='inlay']/b[text()='Начать игру']",      # Начать игру
    "question": "div.question_text > p",                                # Вопрос
    "answer_options": "//span[@class='white_color']",                   # Варианты ответов
    "answer_container": "section.orange_color.orange_bg",               # Контейнер для клика по ответу
    "submit_button": "//div[@class='inlay']/b[text()='Ответить']",      # Ответить
    "complete_button": "//div[@class='inlay']/b[text()='Завершить']",   # Завершить тест
}

# Настройки логирования
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s"
}


# Настройки задержек
class RandomDelays:
    def __getitem__(self, key):
        delays = {
            "between_clicks": random.uniform(1.0, 3.0),  # Задержка между кликами по ответам
            "after_submit": random.uniform(1.0, 3.0),    # Задержка после отправки ответов
            "page_load": random.uniform(1.0, 3.0),       # Задержка при загрузке страницы
            "scrol": random.uniform(1.0, 3.0),           # Задержка при прокрутке страницы
        }
        return delays.get(key, 0.5)                            # Значение по умолчанию, если ключ не найден
