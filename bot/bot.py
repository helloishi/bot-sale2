import asyncio

from aiogram import Bot, Dispatcher, types as t
from aiogram.filters.command import Command
from loguru import logger

from config import config
from db import get_user_by_username

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: t.Message):
    username = message.from_user.username

    logger.info(username)

    if not username:
        await message.answer("Вы пока не установили ник!")
        return 

    user_in_base = get_user_by_username(username)

    if user_in_base:
        await message.answer("Ник найден!")
    else:
        await message.answer("Ник не найден")

    

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logger.info("Start polling...")
    asyncio.run(main()) 

