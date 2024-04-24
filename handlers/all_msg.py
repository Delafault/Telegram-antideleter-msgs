from config import ONLY_PRIVATE, USE_DATABASE, DISPLAY_CONSOLE_MSG, SAVE_FILES
from telethon.types import DocumentAttributeFilename
from utilities import check_type_msg
from database.db import add_user


async def album_handler(event):
    pass

async def all_handler(event):
    #TODO: add album processing...
    # if event.message.grouped_id is not None:
    #     return
    if ONLY_PRIVATE:
        if not event.is_private:
            return

    sender = await event.get_sender()
    chat_id = event.chat_id
    sender_id = event.sender_id
    date = event.date.replace(tzinfo=None)

    if DISPLAY_CONSOLE_MSG:
        print(f"{'-'*17}\n@{sender.username} ({sender.first_name})\nнаписал(а) в {date}:\n{event.text if event.text != '' else '(без текста)'}\nmessage_id: {event.id}; chat_id: {chat_id}\n{'-'*37}\n")

    type_msg = await check_type_msg(event)
    if type_msg != "TEXT" and SAVE_FILES:
        if type_msg != "PHOTO" and type_msg != "TEXT_PHOTO":
            print(type_msg)
            file_name = next((x.file_name for x in event.message.document.attributes if isinstance(x, DocumentAttributeFilename)), None)
            print(file_name)
            extra=await event.download_media(f"temp_files/{chat_id}/{event.id}_{file_name}")
        else:
            extra=await event.download_media(f"temp_files/{chat_id}/{event.id}.png")
    else:
        extra=None

    if USE_DATABASE:
        await add_user(
            msg_id=event.id,
            user_id=sender_id,
            chat_id=chat_id,
            username = sender.username,
            first_name=sender.first_name,
            text_msg=event.text,
            extra=extra,
            type_msg=type_msg,
            send_time=date,
            delete_time=None,
            edit_time=None
        )
    else:
        #TODO: without database
        pass