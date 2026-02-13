import logging
import pickle
import asyncio
from aiogram import Bot, Dispatcher, types
import os
from dotenv import load_dotenv 
API_TOKEN = os.getenv('BOT_TOKEN')

with open('skysense.pkl', 'rb') as f:
    pipeline_loaded = pickle.load(f)

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Register handlers
@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.reply(
        "Assalamu alaykum! Bu bot orqali Toshkent havosini zararlanish darajasi(PM2.5)ni sun'iy intellekt model orqali bashorat qilishingiz mumkin!\n\n"
        "Iltimos AQI indeksi, harorat, namlik qiymatlarini vergul bilan ajratilgan holatda kiriting.\n\n"
        "Masalan 0.1,0.2,0.3"
    )


@dp.message()
async def predict_pm25(message: types.Message):
    try:
        x = message.text.split(',')
        x_test = [[float(x[0]), float(x[1]), float(x[2])]]
        prediction = pipeline_loaded.predict(x_test)
        await message.answer(f"Predicted PM2.5: {prediction[0]}")
    except Exception as e:
        await message.answer("Xatolik yuz berdi! Iltimos, formatga e'tibor bering: 0.1,0.2,0.3")
        logging.error(e)

# Start polling
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

