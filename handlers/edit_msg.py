from database.db import get_message

async def edited_handler(event):
    message_info = await get_message(event.id)
    if message_info:
        print(f"Сообщение {event.id} было изменено.\nБыло: {message_info['text_msg']}\nСтало: {event.text}")
        #TODO: complete edited handler later...