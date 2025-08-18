import logging
from typing import List, Dict, Optional
from config import LOGGING


def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=getattr(logging, LOGGING["level"]),
        format=LOGGING["format"]
    )
    return logging.getLogger(__name__)


def normalize_text(text: str) -> str:
    """Нормализует текст для сравнения (убирает лишние пробелы, приводит к нижнему регистру)"""
    return " ".join(text.strip().lower().split())


def find_best_match(question_text: str, questions_dict: Dict[str, List[str]]) -> Optional[str]:
    """Находит наиболее подходящий вопрос в словаре по тексту"""
    normalized_input = normalize_text(question_text)
    
    best_match = None
    best_score = 0
    
    for question in questions_dict.keys():
        normalized_question = normalize_text(question)
        
        # Простое сравнение по включению
        if normalized_input in normalized_question or normalized_question in normalized_input:
            score = len(set(normalized_input.split()) & set(normalized_question.split()))
            if score > best_score:
                best_score = score
                best_match = question
    
    return best_match


def validate_answers(question: str, answers: List[str], available_options: List[str]) -> List[str]:
    """Проверяет, какие из правильных ответов доступны на странице"""
    valid_answers = []
    
    for answer in answers:
        normalized_answer = normalize_text(answer)
        
        for option in available_options:
            normalized_option = normalize_text(option)
            
            if normalized_answer == normalized_option:
                valid_answers.append(option)
                break
    
    return valid_answers


def format_question_display(question: str, max_length: int = 80) -> str:
    """Форматирует вопрос для отображения в логах"""
    if len(question) <= max_length:
        return question
    
    return question[:max_length-3] + "..."


def save_results(results: Dict[str, bool], filename: str = "test_results.txt"):
    """Сохраняет результаты прохождения теста в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Результаты прохождения теста:\n")
            f.write("=" * 50 + "\n\n")
            
            total_questions = len(results)
            correct_answers = sum(results.values())
            
            for question, is_correct in results.items():
                status = "✓" if is_correct else "✗"
                f.write(f"{status} {format_question_display(question)}\n")
            
            f.write(f"\nИтого: {correct_answers}/{total_questions} правильных ответов")
            f.write(f"\nПроцент правильных ответов: {(correct_answers/total_questions)*100:.1f}%")
        
        print(f"Результаты сохранены в файл: {filename}")
        
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")


def load_custom_questions(filename: str) -> Dict[str, List[str]]:
    """Загружает вопросы из внешнего файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Простой парсер для формата "вопрос: ответ1, ответ2, ответ3"
        questions = {}
        lines = content.strip().split('\n')
        
        for line in lines:
            if ':' in line and not line.startswith('#'):
                parts = line.split(':', 1)
                question = parts[0].strip()
                answers = [ans.strip() for ans in parts[1].split(',')]
                questions[question] = answers
        
        return questions
        
    except Exception as e:
        print(f"Ошибка при загрузке вопросов из файла {filename}: {e}")
        return {}


def process_unknown_questions(filename: str = "unknown_questions.txt") -> Dict[str, List[str]]:
    """Обрабатывает файл с неизвестными вопросами и возвращает их в формате словаря"""
    try:
        questions = load_custom_questions(filename)
        if questions:
            print(f"Загружено {len(questions)} неизвестных вопросов из {filename}")
        return questions
    except Exception as e:
        print(f"Ошибка при обработке неизвестных вопросов: {e}")
        return {}


def merge_questions_with_unknown(main_questions: Dict[str, List[str]], unknown_file: str = "unknown_questions.txt") -> Dict[str, List[str]]:
    """Объединяет основные вопросы с неизвестными вопросами"""
    unknown_questions = process_unknown_questions(unknown_file)
    
    # Объединяем словари
    merged_questions = main_questions.copy()
    merged_questions.update(unknown_questions)
    
    print(f"Объединено {len(main_questions)} основных и {len(unknown_questions)} неизвестных вопросов")
    return merged_questions 