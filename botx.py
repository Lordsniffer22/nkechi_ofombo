import telepot
from pytube import YouTube
import os

# Function to handle incoming messages
def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        query = msg['text']
        if is_youtube_link(query):
            processing = "Processing...\nHang on tight🤙"
            processing_message = bot.sendMessage(chat_id, processing)
            if query.startswith('/v'):
                send_video(chat_id, query)
            else:
                send_audio(chat_id, query)
            bot.deleteMessage((chat_id, msg['message_id']))
            bot.deleteMessage((chat_id, processing_message['message_id']))

# Function to check if a message is a YouTube link
def is_youtube_link(text):
    return text.startswith('https://www.youtube.com/') or text.startswith('https://youtu.be/')

# Function to download a YouTube video
def download_video(video_url):
    yt = YouTube(video_url)
    video_title = yt.title
    stream = yt.streams.first()
    if stream:
        file_path = stream.download()
        video_file = f"{video_title}.{stream.subtype}"
        os.rename(file_path, video_file)
        return video_file
    else:
        return None

# Function to send a video to the user
def send_video(chat_id, video_url):
    video_file = download_video(video_url)
    if video_file:
        with open(video_file, 'rb') as f:
            bot.sendVideo(chat_id, f)
        os.remove(video_file)  # Remove the video file after sending

# Function to download a YouTube video and convert it to MP3
def download_and_convert_to_mp3(video_url):
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

# Function to send an MP3 audio to the user with a caption
def send_audio(chat_id, video_url):
    mp3_file = download_and_convert_to_mp3(video_url)
    if mp3_file:
        # Add a caption to the audio file
        caption = "Hey your music is here.\n\n➤Bot: @tubyDoo_Bot \n│\n╰┈➤Join @udpcustom"
        with open(mp3_file, 'rb') as f:
            bot.sendAudio(chat_id, f, caption=caption)
        os.remove(mp3_file)  # Remove the MP3 file after sending

# Set up the bot
TOKEN = '7167940962:AAGFe2jy93eZSTuLuR0wR9SngQmk6vi2FNg'  # Replace with your actual bot token
bot = telepot.Bot(TOKEN)
bot.message_loop(handle_message)

print('Listening for messages...')

# Keep the program running
import time
while True:
    time.sleep(10)
