from datetime import datetime

from config import VIEW_UNKNOWN_MSG, ONLY_PRIVATE, DISPLAY_CONSOLE_MSG
from database.db import get_message, set_delete_time

async def delete_handler(event):
    for msg_id in event.deleted_ids:
        message_info = await get_message(msg_id)
        if message_info:
            print("---Было удалено сообщение---")
            chat_info = f"В чате с id {event.chat_id}" if event.chat_id else "в приватном чате"
            if ONLY_PRIVATE and chat_info == "в приватном чате":
                if DISPLAY_CONSOLE_MSG:
                    print(f"> Сообщение {msg_id} было удалено {chat_info}.")
                    print("Message Details:")
                    print(f"  Username: {message_info['username'] if message_info['username'] else 'Unknown'}")
                    print(f"  Ник: {message_info['first_name'] if message_info['first_name'] else 'Unknown'}")
                    print(f"  Отправлено в: {message_info['send_time'].strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"  Тип: {message_info['type_msg']}")
                    print(f"  Текст: {message_info['text_msg'][:50]}...")
                    if message_info['extra'] is not None: print(f"(Файл был сохранен в '{message_info['extra']}')")
                    print(f"(Удалено в {datetime.now().replace(microsecond=0)})")
                    print("------------------------------------------------")
                else:
                    print(f"> Сообщение {msg_id} было удалено {chat_info}.")
                    print(f"(Удалено в {datetime.now().replace(microsecond=0)})")
                    print("------------------------------------------------")
                await set_delete_time(msg_id, datetime.now().replace(microsecond=0))
        else:
            if VIEW_UNKNOWN_MSG is True:
                print(f"Удалено неопознанное сообщение в {event.chat_id if event.chat_id else 'в приватном чате'}")
                print(f"ID сообщения: {msg_id}")