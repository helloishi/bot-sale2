import requests
import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import logging

from config import config
#from cards.apple import generate_apple_wallet_card, CARDS_DIR
from db import *

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.bot_token.get_secret_value())
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Create a router instance
router = Router()

# Define the states
class CreateAppleCard(StatesGroup):
    waiting_for_name = State()

# Register the "start" command handler
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    response = "Привет и добро пожаловать! Чтобы посмотреть все акции и скидки, нужно сначала получить карту лояльности."

    keyboard = [
        [KeyboardButton(text="Карта привилегий")],
    ]
    reply_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    await message.answer(response, reply_markup=reply_keyboard)

@router.message(F.text == "Карта привилегий")
async def create_apple_card_request(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше имя карты:")
    await state.set_state(CreateAppleCard.waiting_for_name)

@router.message(CreateAppleCard.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    username = message.from_user.username
    telegram_id = message.from_user.id

    user = get_user_by_username(username)

    if not user:
        create_user(
            username=username,
            name=name, 
            telegram_id=telegram_id,
        )

    personal_link = f'{config.web_app_link}{username}'
    web_app = types.WebAppInfo(url=personal_link)
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='Смотреть акции тут',
            web_app=web_app
        )
    )
    
    builder.row(
        types.InlineKeyboardButton(
            text='Карта привелегий',
            url=config.card_link,
        )
    )

    await state.update_data(user_name=name)
    await state.clear()
    await message.answer(f"Спасибо, {name}. Процесс создания карты начат.", reply_markup=builder.as_markup())


dp.include_router(router)

async def main():
    # Initialize the bot and dispatcher
    await dp.start_polling(bot)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
