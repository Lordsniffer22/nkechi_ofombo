import telepot
from pytube import YouTube
import os

# Function to handle incoming messages
def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        query = msg['text']
        if is_youtube_link(query):
            # If the message is a YouTube link, download and send the MP4 video file
            send_mp4_file(chat_id, query)

# Function to check if a message is a YouTube link
def is_youtube_link(text):
    return text.startswith('https://www.youtube.com/')

# Function to download a YouTube video in MP4 format
def download_video(video_url):
    yt = YouTube(video_url)
    video_title = yt.title.replace('"', '')  # Remove quotes from the title
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    if stream:
        file_path = stream.download()
        mp4_file = f"{video_title}.mp4"
        os.rename(file_path, mp4_file)
        return mp4_file
    else:
        return None


# Function to send an MP4 video file to the user
def send_mp4_file(chat_id, video_url):
    mp4_file = download_video(video_url)
    if mp4_file:
        with open(mp4_file, 'rb') as f:
            bot.sendVideo(chat_id, f)
        os.remove(mp4_file)  # Remove the MP4 file after sending

# Set up the bot
TOKEN = '7021922965:AAHIt6RrH6Tw4mVHh_QLCe-OpakH03igMvk'  # Replace with your actual bot token
bot = telepot.Bot(TOKEN)
bot.message_loop(handle_message)

print('Listening for messages...')

# Keep the program running
import time
while True:
    time.sleep(10)
