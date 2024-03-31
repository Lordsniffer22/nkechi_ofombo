import asyncio
import logging
import sys
from os import getenv
from pytube import YouTube
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils.markdown import hbold
# Bot token can be obtained via https://t.me/BotFather
TOKEN = '7021922965:AAFgpeUCisXYM-s6rDbzhwBtTNZ62jL0x0o'

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

async def download_and_convert_to_mp3(video_url: str) -> str:
    """
    Download a YouTube video and convert it to MP3
    """
    try:
        yt = YouTube(video_url)
        video_title = yt.title
        stream = yt.streams.filter(only_audio=True).first()
        if stream:
            file_path = stream.download()
            mp3_file = f"{video_title}.mp3"
            os.rename(file_path, mp3_file)
            return mp3_file
        else:
            return None
    except Exception as e:
        logging.error(f"Error downloading and converting to MP3: {e}")
        return None

async def send_mp3_file(chat_id: int, video_url: str) -> None:
    """
    Send an MP3 file to the user with a caption
    """
    mp3_file = await download_and_convert_to_mp3(video_url)
    if mp3_file:
        # Add a caption to the audio file
        caption = "Hey your music is here.\n\n➤Bot: @tubyDoo_Bot \n│\n╰┈➤Join @udpcustom"
        # Create an instance of InputFile using the mp3_file path
        input_file = InputFile(mp3_file)
        # Send the audio with the caption
        await bot.send_audio(chat_id, input_file, caption=caption)
        # Remove the MP3 file after sending
        os.remove(mp3_file)



@dp.message()
async def message_handler(message: types.Message) -> None:
    """
    Handler to process incoming messages
    """
    try:
        # Check if the message is a YouTube link
        if message.text.startswith("https://www.youtube.com/") or message.text.startswith("https://youtu.be/"):
            # Download the video and send the MP3 file
            await send_mp3_file(message.chat.id, message.text)
        else:
            # Send a copy of the received message
            await message.copy_to(message.chat.id)
    except Exception as e:
        logging.error(f"Error handling message: {e}")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
