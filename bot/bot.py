import asyncio

from aiogram import Bot, Dispatcher, types as t
from aiogram.filters.command import Command
from loguru import logger

from config import config

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: t.Message):
    await message.answer("Hello!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logger.info("Start polling...")
    asyncio.run(main()) 

