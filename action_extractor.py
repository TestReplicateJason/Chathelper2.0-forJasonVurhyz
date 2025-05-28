import re
from config import get_action_keywords

class ActionExtractor:
    def __init__(self):
        self.action_keywords = get_action_keywords()
        
    def detect_action(self, command_text):
        """Определяет тип действия в команде"""
        if not command_text:
            return "write"
            
        command_lower = command_text.lower()
        
        for action_type, keywords in self.action_keywords.items():
            for keyword in keywords:
                if keyword in command_lower:
                    return action_type
        return "write"  # Действие по умолчанию

    def extract_message_text(self, command_text, action_type):
        """Извлекает основной текст сообщения из команды"""
        if not command_text:
            return ""
            
        # Создаем паттерн для удаления ключевых слов
        patterns = []
        for keyword in self.action_keywords.get(action_type, []):
            # Экранируем специальные символы и добавляем границы слов
            patterns.append(r'\b' + re.escape(keyword) + r'\b')
        
        # Удаляем все ключевые слова
        clean_text = command_text
        for pattern in patterns:
            clean_text = re.sub(pattern, '', clean_text, flags=re.IGNORECASE)
        
        # Удаляем лишние пробелы
        return " ".join(clean_text.split()).strip()