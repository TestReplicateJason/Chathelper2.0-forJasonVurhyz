import speech_recognition as sr
from config import ACTIVATION_WORD, ENERGY_THRESHOLD, PAUSE_THRESHOLD, LANGUAGE
import time

class VoiceActivator:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.setup_microphone()
        self.active = False

    def setup_microphone(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        self.recognizer.energy_threshold = ENERGY_THRESHOLD
        self.recognizer.pause_threshold = PAUSE_THRESHOLD

    def listen_for_activation(self, callback):
        """Слушает активационное слово и вызывает callback при обнаружении"""
        print(f"🟡 Ожидаю активацию (скажите '{ACTIVATION_WORD}')...")
        
        while True:
            try:
                # Используем микрофон в контексте только для одного вызова
                with self.microphone as source:
                    audio = self.recognizer.listen(source, phrase_time_limit=3)
                
                text = self.recognizer.recognize_google(audio, language=LANGUAGE).lower()
                
                if ACTIVATION_WORD in text:
                    print("🟢 Активирован. Говорите команду...")
                    self.active = True
                    callback()
                else:
                    print(f"🔴 Не активация: '{text}'")
                    
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Ошибка сервиса распознавания: {e}")
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")
            
            # Пауза между проверками
            time.sleep(0.1)

    def listen_for_command(self):
        """Слушает команду после активации"""
        try:
            print("🎤 Слушаю команду...")
            # Создаем новый контекст для команды
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            return self.recognizer.recognize_google(audio, language=LANGUAGE)
        
        except sr.WaitTimeoutError:
            print("⏳ Время ожидания команды истекло")
            self.active = False
            return None
        except sr.UnknownValueError:
            print("🔇 Речь не распознана")
            self.active = False
            return None
        except sr.RequestError as e:
            print(f"Ошибка сервиса: {e}")
            self.active = False
            return None
        except Exception as e:
            print(f"Другая ошибка: {e}")
            self.active = False
            return None