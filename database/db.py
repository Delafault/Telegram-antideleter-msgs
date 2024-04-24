import asyncpg

from config import HOST, USER, PASSWORD, DB_NAME
from utilities import bd_print, gd_print

pool = None

async def connect():
    """
    Подключение к БД. Проверка на существование необходимой таблицы
    """
    global pool
    if pool:
        return pool
    try:
        pool = await asyncpg.create_pool(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        if not await check_table():
            await create_table()
            gd_print("База данных не была найдена. Создали новую.")
    except Exception as e:
        bd_print(f"\nОшибка подключения к базе данных: {e}")

async def disconnect():
    """
    Отключение БД
    """
    if pool:
        try:
            await pool.close()
        except Exception as e:
            bd_print(f"\nОшибка отключения от базы данных: {e}")


async def create_table():
    """
    Создание необходимой таблицы в БД
    """
    async with pool.acquire() as conn:
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    msg_id BIGINT NOT NULL,
                    user_id BIGINT NOT NULL,
                    chat_id BIGINT NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    text_msg TEXT,
                    type_msg TEXT,
                    extra TEXT,
                    send_time TIMESTAMP,
                    delete_time TIMESTAMP,
                    edit_time TIMESTAMP
                )
            """)
            print("\nТаблица создана")
        except Exception as e:
            bd_print(f"\nОшибка создания таблицы: {e}")

async def add_user(msg_id, user_id, chat_id, username, first_name, text_msg, extra, type_msg, send_time, delete_time, edit_time):
    """
    Добавление нового сообщения в таблицу "messages"
    """
    async with pool.acquire() as conn:
        try:
                await conn.execute("""
                    INSERT INTO messages (msg_id, user_id, chat_id, username, first_name, text_msg, extra, type_msg, send_time, delete_time, edit_time)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                """, msg_id, user_id, chat_id, username, first_name, text_msg, extra, type_msg, send_time, delete_time, edit_time)
                gd_print(f"Сообщение {msg_id} было записано в бд.")
        except Exception as e:
            bd_print(f"Ошибка добавления пользователя: {e}")

async def check_table():
    """
    Проверка существования необходимой таблицы в БД
    """
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchrow("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_name = 'messages'
                )
            """)
            return result[0]
        except Exception as e:
            bd_print(f"\nОшибка проверки таблицы: {e}")
            return False
    
async def get_message(msg_id):
    """
    Получение сообщения из таблицы "messages" по его message id.
    """
    async with pool.acquire() as conn:
        try:
            message = await conn.fetchrow("""
                SELECT * FROM messages
                WHERE msg_id = $1
            """, msg_id)
            if message:
                return message
            else:
                return None
        except Exception as e:
            bd_print(f"Ошибка поиска сообщения по msg_id: {e}")
            return None

async def set_delete_time(msg_id, delete_time):
    """
    Добавление времени удаления сообщения
    """
    async with pool.acquire() as conn:
        try:
            await conn.execute("""
                UPDATE messages
                SET delete_time = $1
                WHERE msg_id = $2
            """, delete_time, msg_id)
        except Exception as e:
            bd_print(f"Ошибка обновления времени удаления сообщения {msg_id}: {e}")