import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton

API_KEY = "3943218d9c3bee486c5736064e1fd83d"
TG_BOT_TOKEN = "8126803494:AAENeGLaZ0IcoxoS00Cdan4FHJ1nRkH7hqw"

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def start_handler(message: Message):
    print("🔥 Получен /start")  # для отладки
    kb = InlineKeyboardBuilder()
    kb.button(text="🌍 Узнать погоду", callback_data="city")
    kb.button(text="📋 Список команд", callback_data="list")
    kb.adjust(1)
    await message.answer("Привет! Я помогу узнать погоду 🌦️", reply_markup=kb.as_markup())

@dp.callback_query(F.data == "list")
async def show_commands(callback: CallbackQuery):
    await callback.message.answer("/start - Запуск\n/listCity - Быстрый выбор города\nИли просто отправь название города!")

@dp.callback_query(F.data == "city")
async def ask_city(callback: CallbackQuery):
    await callback.message.answer("Напиши название города 🌍")

@dp.message(F.text == "/listCity")
async def list_city(message: Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
        [KeyboardButton(text="Warszawa"), KeyboardButton(text="Kyiv")],
        [KeyboardButton(text="Berlin"), KeyboardButton(text="London")],
        [KeyboardButton(text="New York")]
    ])
    await message.answer("Выбери город или напиши свой:", reply_markup=kb)

@dp.message()
async def get_weather(message: Message):
    city = message.text.strip()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            await message.answer("❌ Город не найден. Попробуй снова.")
            return

        name = data["name"]
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        msg = (
            f"🌍 Город: {name}\n"
            f"🌡 Температура: {temp}°C\n"
            f"🌥 Погода: {description.capitalize()}\n"
            f"💧 Влажность: {humidity}%\n"
            f"🌬 Ветер: {wind} м/с"
        )
        await message.answer(msg)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        await message.answer("⚠️ Ошибка при получении данных.")
