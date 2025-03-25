import requests
import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from datetime import datetime
import re

from config import config
#from cards.apple import generate_apple_wallet_card, CARDS_DIR
from db import *
from db_models import User

# Initialize logging
logging.basicConfig(level=logging.INFO)

GET_CARD_TEXT = "Получить карту"
CHANGE_CARD_NAME = "Изменить имя карты"

# Initialize bot and dispatcher
bot = Bot(token=config.bot_token.get_secret_value())
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Create a router instance
router = Router()

# Define the states
class CreateAppleCard(StatesGroup):
    waiting_for_name = State()
    changing_name = State()

# Register the "start" command handler
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    response = "Привет и добро пожаловать! Чтобы посмотреть все акции и скидки, нужно сначала получить карту лояльности."

    keyboard = [
        [KeyboardButton(text=GET_CARD_TEXT)],
    ]
    reply_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    await message.answer(response, reply_markup=reply_keyboard)

@router.message(F.text == GET_CARD_TEXT)
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

    else:
        update_user_name(username, name)
    
    personal_link = f'{config.web_app_link}{username}'
    web_app = types.WebAppInfo(url=personal_link)

    keyboard = [
        [KeyboardButton(text="Меню")],
    ]

    reply_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Смотреть акции тут", web_app=web_app)],
        [InlineKeyboardButton(text="Показать карту", url=config.card_link)],
        [InlineKeyboardButton(text=CHANGE_CARD_NAME, callback_data='change_card_name_callback')]
    ])

    await state.update_data(user_name=name)
    await state.clear()
    await message.answer(f"Карта готовится...", reply_markup=reply_keyboard)

    await message.answer("Это карта привилегий от канала @MoscowMap", reply_markup=inline_keyboard)

@router.message(F.text == "Меню")
async def show_links(message: types.Message):
    username = message.from_user.username
    personal_link = f'{config.web_app_link}{username}'
    web_app = WebAppInfo(url=personal_link)
    
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Смотреть акции тут", web_app=web_app)],
        [InlineKeyboardButton(text="Показать карту", url=config.card_link)],
        [InlineKeyboardButton(text=CHANGE_CARD_NAME, callback_data='change_card_name_callback')]
    ])

    await message.answer("Это карта привилегий от канала @MoscowMap", reply_markup=inline_keyboard)

@router.callback_query(F.data == 'change_card_name_callback')
async def change_card_name_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите новое имя карты:")
    await state.set_state(CreateAppleCard.changing_name)

@router.message(CreateAppleCard.changing_name)
async def process_new_name(message: types.Message, state: FSMContext):
    new_name = message.text
    username = message.from_user.username

    # Call the function to update user's name
    update_user_name(username, new_name)

    await state.clear()
    await message.answer(f"Ваше имя успешно обновлено на {new_name}.")

# Константы
ADMIN_ID = (438096, 122080193)  # ID администратора
DELAY_BETWEEN_MESSAGES = 3600 / 998  # секунды/сообщения=3.6 секунды на сообщение

# Добавляем новое состояние для рассылки
class SpamStates(StatesGroup):
    wait_spam = State()

# Обработчик команды /send
@router.message(Command("send"))
async def cmd_send(message: types.Message, state: FSMContext):
    # Проверка прав доступа
    if message.from_user.id not in ADMIN_ID:
        logging.info(f"Попытка доступа к команде /send от неавторизованного пользователя: {message.from_user.id}")
        return
    
    # Получаем количество пользователей
    with Session() as session:
        users_count = session.query(User).filter(User.telegram_id.isnot(None)).count()
    
    await message.answer(f"О привет, Админ, готово – {users_count} пользователей к рассылке! Жду от тебя текста")
    await state.set_state(SpamStates.wait_spam)

# Обработчик состояния wait_spam
@router.message(SpamStates.wait_spam)
async def process_spam_message(message: types.Message, state: FSMContext):
    photo = None
    text = message.text or message.caption or "Новое сообщение от MoscowMap"
    
    # Если есть фото в сообщении
    if message.photo:
        photo = message.photo[-1].file_id
    
    await state.clear()
    await message.answer("Начинаю массовую рассылку. Это займет некоторое время.")
    
    # Запускаем рассылку в фоновом режиме
    asyncio.create_task(broadcast_messages(text, photo, message.from_user.id))

# Функция для массовой рассылки сообщений
async def broadcast_messages(text: str, photo=None, admin_id: int = None):
    start_time = datetime.now()
    
    # Получаем всех пользователей из базы данных, у которых есть telegram_id
    users = []
    with Session() as session:
        db_users = session.query(User).filter(User.telegram_id.isnot(None)).all()
        for user in db_users:
            if user.telegram_id:
                users.append(user.telegram_id)
    
    total_users = len(users)
    successful_sends = 0
    failed_sends = 0
    skipped_users = []
    
    logging.info(f"Начинаю рассылку для {total_users} пользователей")
    
    try:
        for i, user_id in enumerate(users):
            try:
                if photo:
                    # Отправляем сообщение с фото
                    await bot.send_photo(chat_id=user_id, photo=photo, caption=text)
                else:
                    # Отправляем текстовое сообщение
                    await bot.send_message(chat_id=user_id, text=text)
                    
                successful_sends += 1
                logging.info(f"Отправлено сообщение пользователю {user_id} ({i+1}/{total_users})")
                
                # Если это не последний пользователь, ждем перед отправкой следующего сообщения
                if i < total_users - 1:
                    await asyncio.sleep(DELAY_BETWEEN_MESSAGES)
            
            except Exception as e:
                failed_sends += 1
                skipped_users.append(user_id)
                logging.error(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
                
                # Делаем небольшую паузу при ошибке
                await asyncio.sleep(1)
                continue
                
            # Периодически сохраняем прогресс (например, каждые 50 сообщений)
            if (i + 1) % 50 == 0:
                # Можно сохранить прогресс в базу данных или файл
                logging.info(f"Прогресс рассылки: {i+1}/{total_users}")
                
                # Опционально: отправлять промежуточный отчет администратору
                progress_percent = round((i + 1) / total_users * 100, 2)
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"Прогресс рассылки: {progress_percent}% ({i+1}/{total_users})"
                )
    
    except Exception as e:
        # Обработка критической ошибки во время рассылки
        logging.error(f"Критическая ошибка во время рассылки: {e}")
    
    finally:
        # Этот блок выполнится в любом случае - при нормальном завершении или при ошибке
        end_time = datetime.now()
        duration = end_time - start_time
        
        report = f"""
Отчет о рассылке:
Начало: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
Окончание: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
Продолжительность: {duration}
Всего пользователей: {total_users}
Успешно отправлено: {successful_sends}
Ошибок отправки: {failed_sends}
"""
        
        if failed_sends > 0:
            report += f"\nКоличество пользователей с ошибками: {failed_sends}"
            if len(skipped_users) <= 20:  # Ограничиваем вывод ID пользователей с ошибками
                report += f"\nПользователи с ошибками: {', '.join(map(str, skipped_users))}"
        
        # Проверяем, была ли рассылка завершена полностью или прервана
        if successful_sends + failed_sends < total_users:
            remaining = total_users - (successful_sends + failed_sends)
            report += f"\n\nВНИМАНИЕ: Рассылка была прервана! Осталось отправить: {remaining} сообщений."
        
        try:
            # Отправляем полный отчет администратору
            await bot.send_message(
                chat_id=admin_id, 
                text=report
            )
            logging.info("Отчет о рассылке отправлен администратору.")
        except Exception as e:
            logging.error(f"Не удалось отправить отчет администратору: {e}")

dp.include_router(router)

async def main():
    # Initialize the bot and dispatcher
    await dp.start_polling(bot)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
