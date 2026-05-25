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
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_messages (
    user_id INT,
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


@dp.message()
async def handler(msg: types.Message):
    pass


async def main():
    print('Бот запущен')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())