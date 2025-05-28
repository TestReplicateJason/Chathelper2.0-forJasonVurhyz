from fuzzy_matcher import FuzzyMatcher
from action_extractor import ActionExtractor
from config import get_users, get_chats
import re

class CommandProcessor:
    def __init__(self):
        self.matcher = FuzzyMatcher()
        self.extractor = ActionExtractor()
        self.users = get_users()
        self.chats = get_chats()
    
    @staticmethod
    def normalize_text(text):
        """Приводит текст к нижнему регистру, заменяет ё на е, удаляет пунктуацию"""
        if not text:
            return ""
        text = text.lower().replace('ё', 'е').replace('Ё', 'е')
        return re.sub(r'[^\w\s]', '', text)
    
    def find_recipient(self, command_text):
        """Находит получателя в команде"""
        # Объединяем пользователей и чаты
        all_names = list(self.users.keys()) + list(self.chats.keys())
        
        # Ищем лучшее совпадение
        best_match, score, index = self.matcher.find_best_match(
            command_text, 
            all_names,
            threshold=70  # Более низкий порог для лучшего распознавания
        )
        
        if not best_match:
            return None, None, None
            
        # Определяем тип сущности
        if best_match in self.users:
            entity_type = "user"
            entity_id = self.users[best_match]
        else:
            entity_type = "chat"
            entity_id = self.chats[best_match]
            
        return entity_type, best_match, entity_id

    def process(self, command_text):
        if not command_text:
            return None

        print(f"🔍 Обработка команды: {command_text}")
        
        # Определяем действие
        action_type = self.extractor.detect_action(command_text)
        print(f"⚡ Действие: {action_type}")
        
        # Извлекаем текст сообщения
        message = self.extractor.extract_message_text(command_text, action_type)
        print(f"📝 Текст сообщения: {message}")
        
        # Находим получателя
        recipient_type, recipient_name, recipient_id = self.find_recipient(command_text)
        
        if not recipient_name:
            # Диагностика: выводим все доступные имена для сравнения
            all_names = list(self.users.keys()) + list(self.chats.keys())
            normalized_command = self.normalize_text(command_text)
            normalized_names = [self.normalize_text(name) for name in all_names]
            
            print("❌ Получатель не найден. Доступные имена:")
            print(f"Оригинальные: {all_names}")
            print(f"Нормализованные: {normalized_names}")
            print(f"Нормализованная команда: {normalized_command}")
            return None
        
        print(f"👤 Получатель: {recipient_name} ({recipient_type}, ID: {recipient_id})")
        
        return {
            "action": action_type,
            "message": message,
            "recipient_type": recipient_type,
            "recipient_id": recipient_id,
            "recipient_name": recipient_name,
            "original_command": command_text
        }