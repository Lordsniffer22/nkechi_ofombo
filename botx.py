import telepot
from pytube import YouTube
import os

# Function to handle incoming messages
def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        query = msg['text']
        if is_youtube_link(query):
            # If the message is a YouTube link, download and send the video in 360p MP4 format
            send_video_file(chat_id, query)

# Function to check if a message is a YouTube link
def is_youtube_link(text):
    return text.startswith('https://www.youtube.com/')

# Function to download a YouTube video in 360p MP4 format
def download_video(video_url):
    yt = YouTube(video_url)
    video_title = yt.title
    stream = yt.streams.filter(res="360p", file_extension="mp4").first()
    if stream:
        file_path = stream.download()
        video_file = f"{video_title}.mp4"
        os.rename(file_path, video_file)
        return video_file
    else:
        return None

# Function to send a video file to the user
def send_video_file(chat_id, video_url):
    video_file = download_video(video_url)
    if video_file:
        with open(video_file, 'rb') as f:
            bot.sendVideo(chat_id, f)
        os.remove(video_file)  # Remove the video file after sending

# Set up the bot
TOKEN = '7021922965:AAHIt6RrH6Tw4mVHh_QLCe-OpakH03igMvk'  # Replace with your actual bot token
bot = telepot.Bot(TOKEN)
bot.message_loop(handle_message)

print('Listening for messages...')

# Keep the program running
import time
while True:
    time.sleep(10)
