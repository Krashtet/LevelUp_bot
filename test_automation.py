import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from questions import QUESTIONS_ANSWERS
from config import RandomDelays, SELECTORS

DELAYS = RandomDelays()


class TestAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.questions_answers = QUESTIONS_ANSWERS

    def start_every_day_quest(self):
        """ Нажатие на 'Начать игру' """
        try:
            start_game = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS['start_game']))
            )

            # Прокрутим до найденного элемента
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_game)
            time.sleep(DELAYS['scrol'])

            start_game.click()
            print('🚀 Ракетка запущена...')
        except TimeoutException:
            print('🛑 Игра еще не доступна, побереги бота!')

    def get_current_question(self):
        """Получает текущий вопрос со страницы"""
        try:
            # TODO: проверить селектор
            question_element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS['question']))
            )
            return question_element.text.strip()
        except TimeoutException:
            print("🌚 Не удалось найти вопрос на странице")
            return None

    def get_answer_options(self):
        """Получает все варианты ответов со страницы"""
        try:
            answer_elements = self.driver.find_elements(By.XPATH, SELECTORS['answer_options'])
            print([elem.text.strip() for elem in answer_elements if elem.text.strip()])
            return [elem.text.strip() for elem in answer_elements if elem.text.strip()]
        except NoSuchElementException:
            print("🌚 Не удалось найти варианты ответов")
            return []

    def select_answer(self, answer_text):
        """Выбирает ответ по тексту"""
        try:
            # Ищем span с нужным текстом
            answer_spans = self.driver.find_elements(By.XPATH, SELECTORS['answer_options'])

            for span in answer_spans:
                print(span.text)
                if span.text.strip() == answer_text:

                    # Ищем родительский section с классом orange_color orange_bg для клика
                    div = span.find_element(By.XPATH, "./../section[@class='orange_color orange_bg']/div")
                    div.click()
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
            print(f"ಠ_ಠ Вопрос '{question_text}' не найден в базе ответов")
            # Сохраняем неизвестный вопрос
            self.save_unknown_question(question_text)

            # выберем рандомный ответ для перехода к след вопросу:
            parent_section = self.driver.find_element(By.CSS_SELECTOR, 'SELECTORS["answer_container"]')
            print('Вариантов ответов: ', len(parent_section))
            parent_section[random.uniform(0, len(parent_section))].click()
            # Ищем кнопку отправки
            submit_button = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["submit_button"])
            submit_button.click()

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

            print(f"🧷 Неизвестный вопрос сохранен в unknown_questions.txt")

        except Exception as e:
            print(f"Ошибка при сохранении неизвестного вопроса: {e}")

    def process_current_page(self):
        """Обрабатывает текущую страницу с вопросом"""
        question = self.get_current_question()
        if question:
            return self.answer_question(question)
        return False

    def submit_answers(self):
        """Отправляет ответы (если есть кнопка отправки)"""
        try:
            # Ищем кнопку отправки
            submit_button = self.driver.find_element(By.XPATH, SELECTORS["submit_button"])
            submit_button.click()
            print("✅ Ответ отправлен")
            time.sleep(2)  # Ждем загрузки следующей страницы
            return True
        except Exception as e:
            print(f"Ошибка при отправке ответов: {e}")
            return False

    def run_automation(self):
        """Основной метод для запуска автоматизации"""

        # self.start_every_day_quest()
        time.sleep(10)
        # try:
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

        # except Exception as e:
        #     print(f"Ошибка во время автоматизации: {e}")