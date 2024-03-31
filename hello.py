import aiogram
import asyncio
import logging
import sys
from os import getenv
from pytube import YouTube
from pytube.exceptions import RegexMatchError

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Bot token can be obtained via https://t.me/BotFather
TOKEN = '7021922965:AAFgpeUCisXYM-s6rDbzhwBtTNZ62jL0x0o'

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Check if the message is a YouTube link
        if message.text.startswith("https://www.youtube.com/") or message.text.startswith("https://youtu.be/"):
            # Download the video
            await download_mp3(message)
        else:
            # Send a copy of the received message
            await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def download_mp3(message: types.Message) -> None:
    """
    Download the YouTube video as MP3 and send it to the user
    """
    try:
        # Get YouTube video
        yt = YouTube(message.text)
        # Get the best audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        # Download the audio stream
        audio_stream.download(output_path=".", filename="temp_audio")
        # Convert to MP3
        mp3_file = audio_stream.download(filename="temp_audio.mp3")
        # Send the MP3 file to the user
        with open(mp3_file, 'rb') as file:
            await message.answer_document(types.InputFile(file))
    except RegexMatchError:
        await message.answer("Invalid YouTube link!")
    except Exception as e:
        await message.answer(f"Error: {e}")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
