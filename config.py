# Конфигурация проекта

# Настройки браузера
BROWSER_CONFIG = {
    "implicit_wait": 10,
    "page_load_timeout": 30,
    "window_size": (1920, 1080)
}

# CSS селекторы для элементов на странице
SELECTORS = {
    "question": "p.question_text",  # Вопрос
    "answer_options": "span.white_color",  # Варианты ответов
    "answer_container": "section.orange_color.orange_bg",  # Контейнер для клика по ответу
    "submit_button": [
        "button[type='submit']",
        "input[type='submit']", 
        ".submit-btn",
        ".next-btn",
        "#submit",
        "#next"
    ]
}

# Настройки задержек
DELAYS = {
    "between_clicks": 0.5,  # Задержка между кликами по ответам
    "after_submit": 2,      # Задержка после отправки ответов
    "page_load": 1          # Задержка при загрузке страницы
}

# Настройки логирования
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s"
} 