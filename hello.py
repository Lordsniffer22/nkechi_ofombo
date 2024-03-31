import aiogram
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters import CommandStart

# Bot token can be obtained via https://t.me/BotFather
TOKEN = '7021922965:AAFgpeUCisXYM-s6rDbzhwBtTNZ62jL0x0o'

# Initialize Bot instance
bot = Bot(token=TOKEN)
# Initialize Dispatcher instance
dp = Dispatcher(bot)


@dp.message_handler(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Send a welcome message using message.answer method
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message_handler()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward received message back to the sender
    """
    try:
        # Send a copy of the received message
        await message.copy_to(chat_id=message.chat.id)
    except TypeError:
        # Not all types are supported to be copied, handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Start polling for updates
    await dp.start_polling()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Run main function asynchronously
    asyncio.run(main())
