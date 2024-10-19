import os
import asyncio

from pathlib import Path
from aiogram import Bot, Dispatcher, types as t
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from loguru import logger

from config import config
from db import get_user_by_username
from cards.apple import generate_apple_wallet_card

CARDS_DIR = "wallet_cards"

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: t.Message):
    username = message.from_user.username

    logger.info(username)

    if not username:
        await message.answer("Вы пока не установили ник!")
        return 

    username = username.lower()
    user_in_base = get_user_by_username(username)
    builder = InlineKeyboardBuilder()
    response = None

    if user_in_base:
        personal_link = f'{config.web_app_link}{username}'
        web_app = t.WebAppInfo(url=personal_link)

        builder.row(
            t.InlineKeyboardButton(
                text='Смотреть акции тут',
                web_app=web_app
            )
        )

        builder.row(
            t.InlineKeyboardButton(
                text='Карта привелегий',
                url=config.card_link,
            )
        )

        response = """Это карта привилегий от канала @MoscowMap\nЧтобы воспользоваться акциями - нужна регистрация: t.me/moscowbenefit_bot/mosbotfit"""
    else:
        builder.row(
            t.InlineKeyboardButton(
                text='Cсылка',
                url=config.login_link
            )
        )

        response = "Зарегистрируйтесь по ссылке, далее перейдите в бота и напишите /start"

    await message.answer(response, reply_markup=builder.as_markup())

@dp.message(Command('create_apple_card'))
async def create_card(message: t.Message) -> None:
    username = message.from_user.username

    logger.info(f'Start creating card for {username}')
    
    generate_apple_wallet_card(username)
    card_path = Path(__file__).parent / CARDS_DIR / f'{username}.pkpass'

    logger.info(card_path)

    if os.path.exists(card_path):
        card = FSInputFile(card_path)
        await bot.send_document(chat_id=message.chat.id, document=card)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logger.info("Start polling...")
    asyncio.run(main()) 

