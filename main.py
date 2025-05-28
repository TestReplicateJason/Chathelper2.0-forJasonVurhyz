from voice_activator import VoiceActivator
from command_processor import CommandProcessor
import threading
import time
from config import ACTIVATION_WORD

def main():
    activator = VoiceActivator()
    processor = CommandProcessor()
    
    def on_activation():
        command = activator.listen_for_command()
        if command:
            result = processor.process(command)
            if result:
                print("\n✅ Результат обработки:")
                print(f"Кому: {result['recipient_name']} (ID: {result['recipient_id']})")
                print(f"Действие: {result['action']}")
                print(f"Сообщение: {result['message']}")
                print("---\n")
        # Возврат в режим ожидания активации
        print(f"🟡 Ожидаю активацию (скажите '{ACTIVATION_WORD}')...")
    
    # Запуск в отдельном потоке
    activation_thread = threading.Thread(
        target=lambda: activator.listen_for_activation(on_activation),
        daemon=True
    )
    activation_thread.start()
    
    print("Система активации запущена. Для выхода нажмите Ctrl+C\n")
    
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nЗавершение работы...")

if __name__ == "__main__":
    main()