import asyncio
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode

# Bot token can be obtained via https://t.me/BotFather
#TOKEN = '7021922965:AAFgpeUCisXYM-s6rDbzhwBtTNZ62jL0x0o'

# Initialize the bot and dispatcher
bot = Bot(token='7021922965:AAFgpeUCisXYM-s6rDbzhwBtTNZ62jL0x0o')
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Your supporting functions can be integrated here

# Example of an aiogram message handler for the /start command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    start_message = ("♻️ WELCOME TO TESLA SSH BOT👌. \n"
                     "━━━━━━━━━━━━━━━━━━━━━━━━━ \n"
                     "\n"
                     "You can use me to manage users on your server!\n"
                     "\n"
                     "To reload the bot, Press /start\n"
                     "To see the usage guide, Press /help\n"
                     "To add user, Press the add user button \n"
                     "To remove user, Send /remove \n"
                     "To list users, Press /users \n"
                     "\n"
                     "🔰 Made with spirit. \n"
                     "========================= \n"
                     "By: @TESLASSH \n"
                     "Mastered by: @hackwell101 \n"
                     "Join @udpcustom")
    await message.answer(start_message)

# Other message handlers and functions can be integrated similarly

# Start polling
async def main():
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
