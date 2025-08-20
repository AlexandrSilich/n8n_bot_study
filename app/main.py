import httpx
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")          # экспортируйте переменную 

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Список мероприятий"), KeyboardButton(text="Новости")]
    ],
    resize_keyboard=True
)

blue_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="GET-Запрос"), KeyboardButton(text="Главное меню")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_menu(message: types.Message):
    welcome_text = """
⚡ <b>Добро пожаловать в EventBot!</b>

Привет, {name}! Я твой помощник по регистрации на мероприятия.

🗓️ <b>Я помогу тебе:</b>

• Показать доступные мероприятия
• Помочь зарегистрироваться на событие  

<b>Выбери нужное действие из меню ниже:</b> 
    """.format(name=message.from_user.first_name or "гость")
    
    # Вариант с локальной картинкой (положи файл logo.jpg в папку с ботом)
    try:
        photo = FSInputFile("logo.jpg")  
        await message.answer_photo(
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

# Остальные обработчики остаются без изменений...
@dp.message(F.text == "Список мероприятий")
async def blue_button_menu(message: types.Message):
    await message.answer("Выбери действие:", reply_markup=blue_menu_keyboard)

@dp.message(F.text == "Главное меню")  
async def back_to_main_menu(message: types.Message):
    await message.answer("Вы вернулись в главное меню. Выбери кнопку:", reply_markup=main_menu_keyboard)

@dp.message(F.text == "GET-Запрос")
async def handle_get_request(message: types.Message):
    url = "http://1237043-cs27722.tw1.ru:5678/webhook/start_page"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.text
        await message.answer(f"Ответ сервера:\n{data}")
    except httpx.HTTPError as e:
        await message.answer(f"Ошибка при GET-запросе:\n{e}")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
