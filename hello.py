import telepot
import asyncio
import logging
import sys
import os
from os import getenv
from pytube import YouTube
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils.markdown import hbold

# Initialize the bot

# Bot token can be obtained via https://t.me/BotFather
TOKEN = '7021922965:AAFgpeUCisXYM-s6rDbzhwBtTNZ62jL0x0o'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Function to check if a message is a YouTube link
def is_youtube_link(text):
    return text.startswith('https://www.youtube.com/') or text.startswith('https://youtu.be/')

# Function to download a YouTube video
async def download_video(video_url):
    yt = YouTube(video_url)
    video_title = yt.title
    streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if streams:
        file_path = streams.download()
        return file_path, video_title
    else:
        return None, None

# Function to download a YouTube video and convert it to MP3
async def download_and_convert_to_mp3(video_url):
    yt = YouTube(video_url)
    video_title = yt.title
    stream = yt.streams.filter(only_audio=True).first()
    if stream:
        file_path = stream.download()
        mp3_file = f"{video_title}.mp3"
        os.rename(file_path, mp3_file)
        return mp3_file, video_title
    else:
        return None, None

# Function to handle incoming messages
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    query = message.text
    if is_youtube_link(query):
        processing = "Processing... \n Hang on tight🤙"
        processing_message = await message.reply(processing)
        if query.startswith('/v'):
            await send_video(message.chat.id, query)
        else:
            await send_audio(message.chat.id, query)
        await asyncio.sleep(3)  # Sleep for 3 seconds
        await message.delete()
        await processing_message.delete()

# Function to send a video file to the user with a caption
async def send_video(chat_id, video_url):
    video_file, video_title = await download_video(video_url)
    if video_file:
        # Add a caption to the video file
        caption = "Hey, your video is here.\n\n➤Bot: @tubyDoo_Bot \n│\n╰┈➤Join @udpcustom"
        with open(video_file, 'rb') as f:
            await bot.send_video(chat_id, f, caption=caption)
        os.remove(video_file)  # Remove the video file after sending

# Function to send an MP3 file to the user with a caption
async def send_audio(chat_id, video_url):
    mp3_file, video_title = await download_and_convert_to_mp3(video_url)
    if mp3_file:
        # Add a caption to the audio file
        caption = "Hey, your music is here.\n\n➤Bot: @tubyDoo_Bot \n│\n╰┈➤Join @udpcustom"
        with open(mp3_file, 'rb') as f:
            await bot.send_audio(chat_id, f, caption=caption)
        os.remove(mp3_file)  # Remove the MP3 file after sending

# Start polling
async def main():
    await bot.start_polling()

if __name__ == '__main__':
    asyncio.run(main())

