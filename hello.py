import aiogram
import asyncio
import logging
import sys
from os import getenv
from pytube import YouTube

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

# Bot token can be obtained via https://t.me/BotFather
TOKEN = '7021922965:AAFgpeUCisXYM-s6rDbzhwBtTNZ62jL0x0o'
# All handlers should be attached to the Dispatcher
dp = Dispatcher()


@dp.message_handler(content_types=['text'])
async def handle_message(message: Message) -> None:
    """
    Function to handle incoming messages
    """
    query = message.text
    if is_youtube_link(query):
        processing = "Processing...\nHang on tight🤙"
        processing_message = await message.reply(processing)
        await send_mp3_file(message.chat.id, query)
        await message.delete()
        await processing_message.delete()


def is_youtube_link(text):
    """
    Function to check if a message is a YouTube link
    """
    return text.startswith('https://www.youtube.com/') or text.startswith('https://youtu.be/')


async def download_and_convert_to_mp3(video_url):
    """
    Function to download a YouTube video and convert it to MP3
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
        logging.error(f"Error downloading/converting video: {e}")
        return None


async def send_mp3_file(chat_id, video_url):
    """
    Function to send an MP3 file to the user with a caption
    """
    mp3_file = await download_and_convert_to_mp3(video_url)
    if mp3_file:
        # Add a caption to the audio file
        caption = "Hey your music is here.\n\n➤Bot: @tubyDoo_Bot \n│\n╰┈➤Join @udpcustom"
        with open(mp3_file, 'rb') as f:
            await bot.send_audio(chat_id, f, caption=caption)
        os.remove(mp3_file)  # Remove the MP3 file after sending


async def main() -> None:
    """
    Main function to initialize and start the bot
    """
    # Initialize Bot instance
    bot = Bot(TOKEN)
    # Start long-polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

