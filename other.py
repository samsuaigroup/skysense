import logging
import pickle
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command  # Add this import
import os
from dotenv import load_dotenv 

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

# Load the model
with open('skysense.pkl', 'rb') as f:
    pipeline_loaded = pickle.load(f)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
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
        # Validate input length
        if len(x) != 3:
            await message.answer("Iltimos, 3 ta qiymat kiriting: AQI, harorat, namlik (vergul bilan ajratilgan)")
            return
            
        x_test = [[float(x[0]), float(x[1]), float(x[2])]]
        prediction = pipeline_loaded.predict(x_test)
        await message.answer(f"Predicted PM2.5: {prediction[0]:.2f}")
    except ValueError:
        await message.answer("Xatolik! Iltimos, faqat sonlarni kiriting. Masalan: 0.1,0.2,0.3")
    except Exception as e:
        await message.answer("Xatolik yuz berdi! Iltimos, formatga e'tibor bering: 0.1,0.2,0.3")
        logging.error(f"Error: {e}")

# Start polling
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
