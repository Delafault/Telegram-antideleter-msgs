from telethon.sync import TelegramClient, events
from telethon.errors import PhoneNumberBannedError, PasswordHashInvalidError, UsernameInvalidError
import logging
import asyncio
import os

from config import API_ID, API_HASH, PHONE_NUMBER, DEVICE_MODEL, SYSTEM_VERSION, EDITED_MSG, USE_DATABASE
from utilities import logo, gd_print, bd_print
from handlers.edit_msg import edited_handler
from handlers.del_msg import delete_handler
from handlers.all_msg import all_handler#, album_handler
from database.db import connect, disconnect

async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)
    if USE_DATABASE:
        await connect()
        gd_print("База данных подключена.\n")
    else:
        bd_print("База данных не используется.\n")

    client = TelegramClient(
        session=f"tg_{PHONE_NUMBER}",
        api_id=API_ID,
        api_hash=API_HASH,
        device_model=DEVICE_MODEL,
        system_version=SYSTEM_VERSION,
        base_logger=logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING) # по совету из документации
    )

    try:
        await client.start(phone=PHONE_NUMBER); client.parse_mode = "html"
        gd_print(f"Успешно вошли в аккаунт {PHONE_NUMBER}.")

        #client.add_event_handler(album_handler, events.Album(chats=None, blacklist_chats=False))
        client.add_event_handler(all_handler, events.NewMessage(chats=None, blacklist_chats=False))
        client.add_event_handler(delete_handler, events.MessageDeleted(chats=None, blacklist_chats=False))
        if EDITED_MSG:
            client.add_event_handler(edited_handler, events.MessageEdited(chats=None, blacklist_chats=False))
        gd_print("Все обработчики запущены.\n")

        await client.run_until_disconnected()
    except PhoneNumberBannedError:
        bd_print(f"Аккаунт {PHONE_NUMBER} заблокирован.")
    except PasswordHashInvalidError:
        bd_print(f"Неверный пароль для аккаунта {PHONE_NUMBER}.")
    except UsernameInvalidError:
        pass
    except Exception as e:
        bd_print(f"Неизвестная ошибка: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        if USE_DATABASE:
            asyncio.run(disconnect())
        gd_print(f"Сессия {PHONE_NUMBER} завершена.")
