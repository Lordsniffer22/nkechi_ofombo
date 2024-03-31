import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.middleware.logging import LoggingMiddleware
from aiogram.utils import executor

# Replace 'YOUR_TOKEN' with your actual bot token
API_TOKEN = '6533833584:AAHPalg1HywEshspXgeGAYOjWRG95jx8X4Q'

# Initialize the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Define a handler for the /start command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Reply with a welcome message
    await message.reply("Welcome to the Bot!")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
