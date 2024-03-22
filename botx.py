import telepot
from pytube import YouTube
import os

# Function to handle incoming messages
def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        query = msg['text']
        if is_youtube_link(query):
            # If the message is a YouTube link, ask user for download preference
            bot.sendMessage(chat_id, "Do you want to download the video as MP3 or MP4? (Reply with 'MP3' or 'MP4')")
        else:
            bot.sendMessage(chat_id, "Please send a valid YouTube link.")

# Function to check if a message is a YouTube link
def is_youtube_link(text):
    return text.startswith('https://www.youtube.com/')

# Function to download a YouTube video and convert it to MP3
def download_and_convert(video_url, format):
    yt = YouTube(video_url)
    video_title = yt.title
    if format == 'MP3':
        stream = yt.streams.filter(only_audio=True).first()
        if stream:
            file_path = stream.download()
            mp3_file = f"{video_title}.mp3"
            os.rename(file_path, mp3_file)
            return mp3_file
    elif format == 'MP4':
        stream = yt.streams.filter(file_extension='mp4').first()
        if stream:
            file_path = stream.download()
            mp4_file = f"{video_title}.mp4"
            os.rename(file_path, mp4_file)
            return mp4_file
    return None

# Function to send a file to the user
def send_file(chat_id, video_url, format):
    file_path = download_and_convert(video_url, format)
    if file_path:
        if format == 'MP3':
            with open(file_path, 'rb') as f:
                bot.sendAudio(chat_id, f)
        elif format == 'MP4':
            with open(file_path, 'rb') as f:
                bot.sendVideo(chat_id, f)
        os.remove(file_path)  # Remove the file after sending

# Set up the bot
TOKEN = '7021922965:AAHIt6RrH6Tw4mVHh_QLCe-OpakH03igMvk'  # Replace with your actual bot token
bot = telepot.Bot(TOKEN)

# Function to handle user's choice of download format
def handle_choice(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        choice = msg['text'].upper()
        if choice == 'MP3' or choice == 'MP4':
            send_file(chat_id, user_data[chat_id], choice)
        else:
            bot.sendMessage(chat_id, "Invalid choice. Please reply with 'MP3' or 'MP4'.")

bot.message_loop({'chat': handle_message,
                  'text': handle_choice})

print('Listening for messages...')

# Keep the program running
import time
while True:
    time.sleep(10)
