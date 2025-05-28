import os
import json

# Пути к файлам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DB_FILE = os.path.join(BASE_DIR, 'user.json')
ACTION_KEYWORDS_FILE = os.path.join(BASE_DIR, 'action_keywords.json')

# Настройки голосового ввода
ACTIVATION_WORD = "джарвис"
ENERGY_THRESHOLD = 300
PAUSE_THRESHOLD = 0.5
LANGUAGE = "ru-RU"

# Загрузка базы пользователей
def load_users():
    try:
        with open(USER_DB_FILE, 'r', encoding='utf-8') as f:
            db = json.load(f)
            return db.get("users", {}), db.get("chats", {})
    except FileNotFoundError:
        print(f"❌ Файл {USER_DB_FILE} не найден!")
        return {}, {}

# Загрузка ключевых слов действий
def load_action_keywords():
    default_actions = {
        "ask": ["спроси", "узнай", "поинтересуйся"],
        "shout": ["крикни", "орни", "прокричи"],
        "write": ["напиши", "отправь", "скажи"]
    }
    
    try:
        with open(ACTION_KEYWORDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Файл {ACTION_KEYWORDS_FILE} не найден, используются значения по умолчанию")
        return default_actions

# Инициализация данных
USERS, CHATS = load_users()
ACTION_KEYWORDS = load_action_keywords()

# Функции доступа
def get_users():
    return USERS

def get_chats():
    return CHATS

def get_action_keywords():
    return ACTION_KEYWORDS