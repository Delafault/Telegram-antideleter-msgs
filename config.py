# Description: Конфигурация для юзербота.
API_ID = 0 # API_ID и API_HASH можно получить на my.telegram.org
API_HASH = "" # ↑
PHONE_NUMBER = "+7" # Номер телефона для юзербота
DEVICE_MODEL = "Pixel 3 XL" # Модель устройства (можно не менять)
SYSTEM_VERSION = "Android 10.0" # Версия системы (можно не менять)

EDITED_MSG = False # Следить ли за изменением сообщений
ONLY_PRIVATE = True # Следить только за личными сообщениями. Если False, то следит за всеми сообщениями (включая группы и каналы)
VIEW_UNKNOWN_MSG = True # Уведомлять о сообщениях, которые не удалось распознать (не были занесены в базу данных)
DISPLAY_CONSOLE_MSG = True # Отображать сообщения (всю информацию: текст, отправитель и т.д.) в консоли. Если False, то подробности сообщений не будут показываться в консоли
SAVE_FILES = True # Сохранять ли файлы в папку 'temp_files'

USE_DATABASE = True # Использовать ли базу данных для хранения сообщений. Если False, то сообщения хранятся в оперативной памяти (не рекомендуется. Используйте базу данных!)
# -
HOST = "localhost" # Хост базы данных
USER = "postgres" # Пользователь базы данных
PASSWORD = "pirild" # Пароль базы данных
DB_NAME = "history_msgs" # Название базы данных