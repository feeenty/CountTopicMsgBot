import os
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

connection = sqlite3.connect('user_messages.db')
cursor = connection.cursor()
cursor.execute(
"""
CREATE TABLE IF NOT EXISTS user_messages (
    user_id INT PRIMARY KEY,
    username TEXT,
    message_count INT
)
""")
connection.commit()


@dp.message(Command("topic_id"))
async def topic_id(msg: types.Message):
    topic_id = msg.message_thread_id
    print(topic_id)
    await msg.reply(f"ID темы: {topic_id}")


@dp.message(Command("top"))
async def top(msg: types.Message):
    connection = sqlite3.connect('user_messages.db')
    cursor = connection.cursor()

    top = cursor.execute(
        """
        SELECT user_id, username, message_count
        FROM user_messages
        ORDER BY message_count DESC
        """
    ).fetchall()

    if not top:
        await msg.reply("Нет ни одного сообщения")

    text = "Топ пользователей в чате\n"
    for i, (user_id, username, count) in enumerate(top, 1):
        text += f"{username} - {count}"

    connection.commit()


@dp.message()
async def handler(msg: types.Message):
    if msg.message_thread_id:
        return

    connection = sqlite3.connect('user_messages.db')
    cursor = connection.cursor()

    user = msg.from_user
    cursor.execute(
        """
        INSERT INTO user_messages (user_id, username, message_count)
        VALUES (?, ?, 1)
        ON CONFLICT (user_id) DO UPDATE SET
        username = EXCLUDED.username,
        message_count = message_count + 1
        """,
        (user.id, user.username or user.first_name)
    )

    connection.commit()


async def main():
    print('Бот запущен')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
