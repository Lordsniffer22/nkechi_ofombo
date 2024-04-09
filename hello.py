import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = '6486401647:AAGaY2kaQyPKkjVttkjUUeENFk5OxpaJXjE'

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Define the command handler
@dp.message_handler(commands=['greets'])
async def greet(message: types.Message):
    await message.reply("Hello, world!")


# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
