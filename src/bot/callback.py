from aiogram import Bot, types
from aiogram import F

# Обработка callback для кнопки "Menu"
async def handle_menu_callback(callback: types.CallbackQuery, bot: Bot):
    # Импорт главной страницы
    from main import show_start_menu

    # Вызываем обработчик главного меню
    await show_start_menu(callback.message.chat.id, callback.from_user, bot)
    await callback.answer()

# Обработка callback для кнопки "About"
async def handle_about_callback(callback: types.CallbackQuery):
    # Импорт страницы описания
    from main import handle_about

    # Вызываем обработчик главного меню
    await handle_about(callback.message)
    await callback.answer()

# Регистрация коллбеков
def register_callbacks(dp):
    dp.callback_query.register(handle_menu_callback, F.data == "menu")
    dp.callback_query.register(handle_about_callback, F.data == "about")