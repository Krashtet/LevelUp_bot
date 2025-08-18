from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from questions import QUESTIONS_ANSWERS


class TestAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.questions_answers = QUESTIONS_ANSWERS
    
    def get_current_question(self):
        """Получает текущий вопрос со страницы"""
        try:
            question_element = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "question_text"))
            )
            return question_element.text.strip()
        except TimeoutException:
            print("Не удалось найти вопрос на странице")
            return None
    
    def get_answer_options(self):
        """Получает все варианты ответов со страницы"""
        try:
            answer_elements = self.driver.find_elements(By.CSS_SELECTOR, "span.white_color")
            return [elem.text.strip() for elem in answer_elements if elem.text.strip()]
        except NoSuchElementException:
            print("Не удалось найти варианты ответов")
            return []
    
    def select_answer(self, answer_text):
        """Выбирает ответ по тексту"""
        try:
            # Ищем span с нужным текстом
            answer_spans = self.driver.find_elements(By.CSS_SELECTOR, "span.white_color")
            
            for span in answer_spans:
                if span.text.strip() == answer_text:
                    # Ищем родительский section с классом orange_color orange_bg для клика
                    parent_section = span.find_element(By.XPATH, "./ancestor::section[contains(@class, 'orange_color') and contains(@class, 'orange_bg')]")
                    parent_section.click()
                    print(f"Выбран ответ: {answer_text}")
                    return True
            
            print(f"Ответ '{answer_text}' не найден на странице")
            return False
            
        except Exception as e:
            print(f"Ошибка при выборе ответа '{answer_text}': {e}")
            return False
    
    def answer_question(self, question_text):
        """Отвечает на конкретный вопрос"""
        if question_text not in self.questions_answers:
            print(f"Вопрос '{question_text}' не найден в базе ответов")
            # Сохраняем неизвестный вопрос
            self.save_unknown_question(question_text)
            return False
        
        correct_answers = self.questions_answers[question_text]
        print(f"Вопрос: {question_text}")
        print(f"Правильные ответы: {correct_answers}")
        
        # Получаем варианты ответов со страницы
        available_answers = self.get_answer_options()
        print(f"Доступные ответы: {available_answers}")
        
        # Выбираем правильные ответы
        selected_count = 0
        for correct_answer in correct_answers:
            if correct_answer in available_answers:
                if self.select_answer(correct_answer):
                    selected_count += 1
                    time.sleep(0.5)  # Небольшая пауза между кликами
        
        print(f"Выбрано {selected_count} из {len(correct_answers)} правильных ответов")
        return selected_count > 0
    
    def process_current_page(self):
        """Обрабатывает текущую страницу с вопросом"""
        question = self.get_current_question()
        if question:
            return self.answer_question(question)
        return False
    
    def submit_answers(self):
        """Отправляет ответы (если есть кнопка отправки)"""
        try:
            # Ищем кнопку отправки (может быть разная на разных сайтах)
            submit_buttons = [
                "button[type='submit']",
                "input[type='submit']",
                ".submit-btn",
                ".next-btn",
                "#submit",
                "#next"
            ]
            
            for selector in submit_buttons:
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    submit_button.click()
                    print("Ответы отправлены")
                    time.sleep(2)  # Ждем загрузки следующей страницы
                    return True
                except NoSuchElementException:
                    continue
            
            print("Кнопка отправки не найдена")
            return False
            
        except Exception as e:
            print(f"Ошибка при отправке ответов: {e}")
            return False
    
    def run_automation(self):
        """Основной метод для запуска автоматизации"""
        print("Начинаем автоматическое прохождение теста...")
        
        try:
            while True:
                # Обрабатываем текущую страницу
                if not self.process_current_page():
                    print("Не удалось обработать текущую страницу")
                    break
                
                # Небольшая пауза
                time.sleep(1)
                
                # Пытаемся отправить ответы
                if not self.submit_answers():
                    print("Не удалось отправить ответы или тест завершен")
                    break
                
                # Проверяем, есть ли еще вопросы
                try:
                    next_question = self.get_current_question()
                    if not next_question:
                        print("Тест завершен")
                        break
                except:
                    print("Тест завершен")
                    break
            
            print("Автоматизация завершена")
            
        except Exception as e:
            print(f"Ошибка во время автоматизации: {e}")
    
    def save_unknown_question(self, question_text):
        """Сохраняет неизвестный вопрос и варианты ответов в файл"""
        try:
            # Получаем варианты ответов со страницы
            available_answers = self.get_answer_options()
            
            # Формируем строку для записи
            question_line = f"{question_text}: {', '.join(available_answers)}\n"
            
            # Записываем в файл
            with open("unknown_questions.txt", "a", encoding="utf-8") as f:
                f.write(question_line)
            
            print(f"Неизвестный вопрос сохранен в unknown_questions.txt")
            print(f"Вопрос: {question_text}")
            print(f"Варианты ответов: {available_answers}")
            
        except Exception as e:
            print(f"Ошибка при сохранении неизвестного вопроса: {e}")


def main():
    """
    Основная функция для запуска автоматизации
    Здесь нужно будет добавить инициализацию драйвера
    """
    print("Функция main() - здесь нужно будет добавить инициализацию драйвера")
    print("Пример использования:")
    print("driver = webdriver.Chrome()  # или другой браузер")
    print("driver.get('URL_САЙТА_С_ТЕСТАМИ')")
    print("automation = TestAutomation(driver)")
    print("automation.run_automation()")


if __name__ == "__main__":
    main() 