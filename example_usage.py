"""
Пример использования автоматизации тестов
Замените URL_САЙТА_С_ТЕСТАМИ на реальный URL
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from test_automation import TestAutomation
from utils import setup_logging, save_results
import time


def setup_chrome_driver():
    """Настройка Chrome драйвера"""
    chrome_options = Options()
    
    # Опциональные настройки
    # chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Автоматическая установка драйвера
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver


def main():
    """Основная функция для запуска автоматизации"""
    # Настройка логирования
    logger = setup_logging()
    
    # URL сайта с тестами (замените на реальный)
    test_url = "URL_САЙТА_С_ТЕСТАМИ"
    
    try:
        # Инициализация драйвера
        logger.info("Инициализация браузера...")
        driver = setup_chrome_driver()
        
        # Настройка таймаутов
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        
        # Переход на сайт с тестами
        logger.info(f"Переход на сайт: {test_url}")
        driver.get(test_url)
        
        # Ждем загрузки страницы
        time.sleep(3)
        
        # Создание экземпляра автоматизации
        automation = TestAutomation(driver)
        
        # Запуск автоматизации
        logger.info("Запуск автоматического прохождения теста...")
        automation.run_automation()
        
        # Ждем завершения
        time.sleep(5)
        
        logger.info("Автоматизация завершена успешно")
        
    except Exception as e:
        logger.error(f"Ошибка во время выполнения: {e}")
        
    finally:
        # Закрытие браузера
        try:
            driver.quit()
            logger.info("Браузер закрыт")
        except:
            pass


def example_with_custom_questions():
    """Пример с загрузкой вопросов из файла"""
    from utils import load_custom_questions
    
    # Загрузка вопросов из файла
    custom_questions = load_custom_questions("custom_questions.txt")
    
    if custom_questions:
        # Создание экземпляра с кастомными вопросами
        driver = setup_chrome_driver()
        automation = TestAutomation(driver)
        automation.questions_answers = custom_questions
        
        # Запуск автоматизации
        automation.run_automation()
        driver.quit()


def example_with_unknown_questions():
    """Пример с обработкой неизвестных вопросов"""
    from utils import merge_questions_with_unknown
    from questions import QUESTIONS_ANSWERS
    
    # Объединяем основные вопросы с неизвестными
    all_questions = merge_questions_with_unknown(QUESTIONS_ANSWERS)
    
    if all_questions:
        driver = setup_chrome_driver()
        automation = TestAutomation(driver)
        automation.questions_answers = all_questions
        
        # Запуск автоматизации
        automation.run_automation()
        driver.quit()


if __name__ == "__main__":
    print("Пример использования автоматизации тестов")
    print("=" * 50)
    print("1. Установите зависимости: pip install -r requirements.txt")
    print("2. Замените URL_САЙТА_С_ТЕСТАМИ на реальный URL в example_usage.py")
    print("3. Добавьте вопросы и ответы в questions.py")
    print("4. Запустите: python example_usage.py")
    print("\nИли используйте функцию main() для запуска автоматизации")
    print("\nДополнительные функции:")
    print("- example_with_custom_questions() - загрузка вопросов из файла")
    print("- example_with_unknown_questions() - обработка неизвестных вопросов") 