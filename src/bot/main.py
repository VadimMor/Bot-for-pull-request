import asyncio
import os
import logging

from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

# Импорт коллбеков
from callback import register_callbacks
from user_manager import UserManager



"""============== Инициализация данных/переменных =============="""
load_dotenv()

tokenTg=os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=tokenTg)
dp = Dispatcher()
user_manager = UserManager()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)



"""============== Рабочии функции =============="""
# Подключение к RabbitMQ
async def on_startup():
    # Выполняется при старте бота
    await user_manager.connect()
    logging.info("RabbitMQ подключен")

# Отключение к RabbitMQ
async def on_shutdown():
    # Выполняется при остановке бота
    await user_manager.close()
    logging.info("RabbitMQ отключен")

# Меню для главного экрана
async def show_start_menu(chat_id: int, user: types.User, bot: Bot):
    # Получение сущесвтования пользователя и его роль
    is_admin, role = await user_manager.check_user(f'@{user.username}' or "")
    logger.info(f"Проверка пользователя: {user.username} - is_admin={is_admin}. Его роль - {role}")

    # Создание кнопок
    button_about = InlineKeyboardButton(
        text='Описание',
        callback_data='about'
    )
    buttons_row = [button_about]

    # Создание кнопок для администратора
    if role == 'ADMIN':
        button_users = InlineKeyboardButton(
            text='Пользователи',
            callback_data='users'
        )
        buttons_row.insert(0, button_users)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[buttons_row],
        resize_keyboard=True
    )

    await bot.send_message(
        chat_id=chat_id,
        text=f"Привет, {user.full_name}! \nЯ твой помощник. Выбери нужный пункт из меню",
        reply_markup=markup
    )



"""============== Хендлы для бота =============="""
# Главный экран
@dp.message(Command("start", "menu"))
@dp.message(F.text == "⬅️ Menu")
async def handle_start(message: types.Message):
    await show_start_menu(message.chat.id, message.from_user, bot)

# Обработка кнопки "Описание"
@dp.message(Command("about"))
@dp.message(F.text == 'Описание')
async def handle_about(message: types.Message):
    button_url = InlineKeyboardButton(
        text="Полное описание",
        url="https://github.com/VadimMor/Bot-for-pull-request"
    )
    button_menu = InlineKeyboardButton(
        text='⬅️ Menu',
        callback_data="menu"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [button_url, button_menu]
        ]
    )
    
    await message.answer(
        text="Bot for pull requests 🤖 — это удобный бот для GitHub, который автоматически отправляет уведомления о новых Pull Request в выбранных репозиториях. Полное описание можно прочитать по ссылке ниже. 🔗👇",
        reply_markup=markup
    )

# Обработка прочих сообщений
@dp.message()
async def other_text(message: types.Message):
    button_menu = KeyboardButton(text='⬅️ Menu')
    markup = ReplyKeyboardMarkup(keyboard=[[button_menu]], resize_keyboard=True)

    await message.answer(
        text="❌ Ошибка! Вернитесь в меню.",
        reply_markup=markup
    )


# Регистрируем callback-обработчики
register_callbacks(dp)

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    await on_startup()  # Инициализация RabbitMQ
    
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()

if __name__ == '__main__':
    asyncio.run(main())