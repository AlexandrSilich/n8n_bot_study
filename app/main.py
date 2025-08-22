import httpx

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
import asyncio
import os

#BOT_TOKEN = os.getenv("BOT_TOKEN") # экспортируйте переменную (пока что ошибка - разобраться)

bot = Bot(token="8299436300:AAEezdzZcEe-TKgQYDhkF6IBvAHYYIQ6J_k")
dp = Dispatcher()

# Inline клавиатуры вместо Reply
main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Список мероприятий", callback_data="events_list"), 
         InlineKeyboardButton(text="GET-Запрос", callback_data="get_request"), 
         InlineKeyboardButton(text="Мой профиль", callback_data="profile")]
    ]
)

blue_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Следующие 2 мероприятия", callback_data="next_events"), 
         InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ]
)

@dp.message(Command("start"))
async def start_menu(message: types.Message):
    welcome_text = """
⚡ Добро пожаловать в EventBot!

Привет, {name}! Я твой помощник по регистрации на мероприятия.

🗓️ Я помогу тебе:
• Показать доступные мероприятия
• Помочь зарегистрироваться на событие

Выбери нужное действие из меню ниже:
""".format(name=message.from_user.first_name or "гость")

    # Вариант с локальной картинкой (положи файл logo.jpg в папку с ботом)
    try:
        photo = FSInputFile("../images/logo.jpg")
        """
        # Вариант с ссылкой на файл в Google Drive
        photo_url = "https://drive.google.com/uc?id=YOUR_FILE_ID"
        """
        #photo_url = "https://drive.google.com/file/d/1HbapbEJzjDSnTt_iXtkuwNnjOwClj2xs/view?usp=drive_link"
        await message.answer_photo(
            #photo=convert_gdrive_url(photo_url),
            photo=photo,
            caption=welcome_text,
            reply_markup=main_menu_keyboard,
            parse_mode="HTML"
        )
    except FileNotFoundError:
        # Если картинки нет, отправляем просто текст
        await message.answer(
            text=welcome_text + "\n\n⚠️ (Картинка не найдена)",
            reply_markup=main_menu_keyboard,
            parse_mode="HTML"
        )

# Остальные обработчики изменены на callback_query...

# Обработчики для inline кнопок (вместо текстовых сообщений)
@dp.callback_query(F.data == "events_list")
async def blue_button_menu(callback: types.CallbackQuery):
    # Проверяем тип сообщения и используем соответствующий метод
    if callback.message.photo:
        # Если сообщение с фото - редактируем подпись
        await callback.message.edit_caption(
            caption="Выбери действие:",
            reply_markup=blue_menu_keyboard
        )
    else:
        # Если текстовое сообщение - редактируем текст
        await callback.message.edit_text(
            text="Выбери действие:",
            reply_markup=blue_menu_keyboard
        )
    await callback.answer()

@dp.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: types.CallbackQuery):
    welcome_text = """
⚡ Добро пожаловать в EventBot!

Привет, {name}! Я твой помощник по регистрации на мероприятия.

🗓️ Я помогу тебе:
• Показать доступные мероприятия
• Помочь зарегистрироваться на событие

Выбери нужное действие из меню ниже:
""".format(name=callback.from_user.first_name or "гость")
    
    # Проверяем тип сообщения
    if callback.message.photo:
        # Если сообщение с фото - редактируем подпись
        await callback.message.edit_caption(
            caption=welcome_text,
            reply_markup=main_menu_keyboard,
            parse_mode="HTML"
        )
    else:
        # Если текстовое сообщение - редактируем текст
        await callback.message.edit_text(
            text=welcome_text,
            reply_markup=main_menu_keyboard,
            parse_mode="HTML"
        )
    await callback.answer()

@dp.callback_query(F.data == "get_request")
async def handle_get_request(callback: types.CallbackQuery):
    await callback.answer("Выполняю GET-запрос...")
    
    url = "http://1237043-cs27722.tw1.ru:5678/webhook/start_page"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.text
            await callback.message.answer(f"Ответ сервера:\n{data}")
    except httpx.HTTPError as e:
        await callback.message.answer(f"Ошибка при GET-запросе:\n{e}")

@dp.callback_query(F.data == "profile")
async def profile_handler(callback: types.CallbackQuery):
    profile_text = f"Ваш профиль:\nИмя: {callback.from_user.first_name}\nID: {callback.from_user.id}"
    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]]
    )
    
    # Проверяем тип сообщения
    if callback.message.photo:
        # Если сообщение с фото - редактируем подпись
        await callback.message.edit_caption(
            caption=profile_text,
            reply_markup=back_keyboard
        )
    else:
        # Если текстовое сообщение - редактируем текст
        await callback.message.edit_text(
            text=profile_text,
            reply_markup=back_keyboard
        )
    await callback.answer()

@dp.callback_query(F.data == "next_events")
async def next_events_handler(callback: types.CallbackQuery):
    events_text = "Следующие мероприятия:\n• Мероприятие 1 - 25.08.2025\n• Мероприятие 2 - 30.08.2025"
    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="events_list")]]
    )
    
    # Проверяем тип сообщения
    if callback.message.photo:
        # Если сообщение с фото - редактируем подпись
        await callback.message.edit_caption(
            caption=events_text,
            reply_markup=back_keyboard
        )
    else:
        # Если текстовое сообщение - редактируем текст
        await callback.message.edit_text(
            text=events_text,
            reply_markup=back_keyboard
        )
    await callback.answer()

def convert_gdrive_url(share_url):
    """
    Преобразует обычную ссылку Google Drive в прямую ссылку для загрузки в TG
    """
    # Извлекаем FILE_ID из ссылки
    if "/file/d/" in share_url:
        file_id = share_url.split("/file/d/")[1].split("/")
        # Формируем прямую ссылку
        return f"https://drive.google.com/uc?id={file_id}"
    else:
        raise ValueError("Неверный формат ссылки Google Drive")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
