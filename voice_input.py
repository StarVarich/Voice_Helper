# Импортируем библиотеку для распознавания речи
import speech_recognition as sr
import webbrowser
import sys
import time

def list_microphones():
    """Выводит список доступных микрофонов"""
    print("Доступные микрофоны:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Микрофон {index}: {name}")

# Создаем объект распознавателя речи
r = sr.Recognizer()

# Устанавливаем параметры для лучшего распознавания
r.energy_threshold = 3000  # Уменьшаем порог энергии
r.dynamic_energy_threshold = True
r.dynamic_energy_adjustment_damping = 0.15
r.dynamic_energy_ratio = 1.5
r.pause_threshold = 0.5
r.phrase_threshold = 0.3
r.non_speaking_duration = 0.3

# Ключевые фразы для активации помощника
WAKE_WORDS = [
    "привет помощник",
    "эй компьютер",
    "слушай помощник",
    "внимание компьютер"
]

def open_yandex_music():
    print("Открытие яндекс музыки...")
    webbrowser.open("https://music.yandex.ru")

def open_youtube():
    print("Открытие youtube...")
    webbrowser.open("https://www.youtube.com")

commands = {
    "открой яндекс музыку": open_yandex_music,
    "включи яндекс музыку": open_yandex_music,
    "запусти яндекс музыку": open_yandex_music,
    "открой youtube": open_youtube,
    "включи youtube": open_youtube,
    "запусти youtube": open_youtube
}

def listen_for_wake_word(source):
    """Слушает ключевую фразу для активации помощника"""
    print("Ожидаю ключевую фразу...")
    try:
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language="ru-RU").lower()
            print(f"Распознано: {text}")
            return any(wake_word in text for wake_word in WAKE_WORDS)
        except sr.UnknownValueError:
            return False
    except sr.WaitTimeoutError:
        return False

def execute_command(source):
    """Выполняет одну команду и возвращает управление"""
    print("Помощник активирован! Слушаю команду...")
    try:
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        print("Готово, обрабатываю...")
        
        try:
            text = r.recognize_google(audio, language="ru-RU")
            print(f"Вы сказали: {text}")
            
            if text.lower() in commands:
                commands[text.lower()]()
                print("Команда выполнена. Ожидаю ключевую фразу для следующей команды.")
            else:
                print("Неизвестная команда. Доступные команды:")
                for command in commands.keys():
                    print(f"- {command}")
                print("Ожидаю ключевую фразу для следующей команды.")
                
        except sr.UnknownValueError:
            print("Не удалось распознать команду. Пожалуйста, повторите.")
            print("Убедитесь, что вы говорите четко и в микрофон.")
            print("Ожидаю ключевую фразу для следующей команды.")
            
    except sr.WaitTimeoutError:
        print("Время ожидания истекло. Ожидаю ключевую фразу для следующей команды.")

def main():
    # Выводим список доступных микрофонов
    list_microphones()
    
    print("\nНачинаю работу с голосовым управлением...")
    print("Ключевые фразы для активации:")
    for wake_word in WAKE_WORDS:
        print(f"- {wake_word}")
    print("\nДоступные команды:")
    for command in commands.keys():
        print(f"- {command}")
    print("\nДля выхода нажмите Ctrl+C\n")

    while True:
        try:
            with sr.Microphone() as source:
                print("Настраиваю микрофон...")
                # Калибруем микрофон под окружающий шум
                r.adjust_for_ambient_noise(source, duration=2)
                
                while True:
                    # Ждем ключевую фразу
                    if not listen_for_wake_word(source):
                        continue
                    
                    # Выполняем одну команду
                    execute_command(source)
                    
        except sr.RequestError as e:
            print(f"Ошибка подключения к сервису Google: {e}")
            print("Проверьте подключение к интернету.")
            sys.exit(1)
            
        except KeyboardInterrupt:
            print("\nПрограмма завершена.")
            sys.exit(0)
            
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            print("Попробуйте перезапустить программу.")

if __name__ == "__main__":
    main()
 



