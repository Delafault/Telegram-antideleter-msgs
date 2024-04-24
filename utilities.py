logo = """
▄▀█ █▄░█ ▀█▀ █ █▀▄ █▀▀ █░░ █▀▄▀█ █▀ █▀▀|ᵇʸ ᵈᵉˡᵃᶠᵃᵘˡᵗ
█▀█ █░▀█ ░█░ █ █▄▀ ██▄ █▄▄ █░▀░█ ▄█ █▄█
      FOR TELEGRAM (version 0.2)"""

def gd_print(value):
    green_color = '\033[32m'
    reset_color = '\033[0m'
    result = f"\n>{green_color} {value} {reset_color}"
    print(result)

def bd_print(value):
    red_color = '\033[31m'
    reset_color = '\033[0m'
    result = f"\n>{red_color} {value} {reset_color}"
    print(result)

async def check_type_msg(event):
    if event.photo:
        msg_type = "PHOTO" if event.text is None or event.text == "" else "TEXT_PHOTO"
    if event.document:
        mime_type = event.document.mime_type if hasattr(event.document, 'mime_type') else None
        
        if mime_type and mime_type != "audio/ogg" and mime_type != "application/x-tgsticker" and mime_type != "video/mp4":
            msg_type = "DOCUMENT" if event.text is None or event.text == "" else "TEXT_DOCUMENT"
        elif mime_type == "audio/ogg":
            msg_type = "AUDIO"
        elif mime_type == "application/x-tgsticker":
            msg_type = "STICKER"
        elif mime_type == "video/mp4":
            msg_type = "VIDEO"
    if event.text and not event.document and not event.photo and not event.video:
        msg_type = "TEXT"

    return msg_type if msg_type else "Неизвестный тип сообщения"