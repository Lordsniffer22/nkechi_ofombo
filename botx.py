import telepot
from pytube import YouTube
import os

# Function to handle incoming messages
def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        query = msg['text']
        if is_youtube_link(query):
            # If the message is a YouTube link, ask the user to choose format
            send_format_choice(chat_id)

# Function to check if a message is a YouTube link
def is_youtube_link(text):
    return text.startswith('https://www.youtube.com/')

# Function to send inline buttons for format choice
def send_format_choice(chat_id):
    keyboard = {'inline_keyboard': [[{'text': 'Video', 'callback_data': 'video'}, {'text': 'MP3', 'callback_data': 'mp3'}]]}
    bot.sendMessage(chat_id, 'Choose the format:', reply_markup=keyboard)

# Function to handle inline button callback
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    if query_data == 'video':
        bot.sendMessage(from_id, 'Downloading video in MP4 format (360p)...')
        send_mp4_file(from_id, msg['message']['text'])
    elif query_data == 'mp3':
        bot.sendMessage(from_id, 'Downloading audio in MP3 format...')
        send_mp3_file(from_id, msg['message']['text'])

# Function to download a YouTube video and convert it to MP3
def download_and_convert_to_mp3(video_url):
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
        print(f"Error downloading and converting to MP3: {e}")
        return None

# Function to download a YouTube video in MP4 format (360p)
def download_video(video_url):
    try:
        yt = YouTube(video_url)
        video_title = yt.title
        stream = yt.streams.filter(res="360p", mime_type="video/mp4").first()
        if stream:
            file_path = stream.download()
            return file_path
        else:
            return None
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None


# Function to send an MP3 file to the user
def send_mp3_file(chat_id, video_url):
    mp3_file = download_and_convert_to_mp3(video_url)
    if mp3_file:
        with open(mp3_file, 'rb') as f:
            bot.sendAudio(chat_id, f)
        os.remove(mp3_file)  # Remove the MP3 file after sending

# Function to send a video file to the user
def send_mp4_file(chat_id, video_url):
    mp4_file = download_video(video_url)
    if mp4_file:
        with open(mp4_file, 'rb') as f:
            bot.sendVideo(chat_id, f)
        os.remove(mp4_file)  # Remove the video file after sending

# Set up the bot
TOKEN = '7021922965:AAHIt6RrH6Tw4mVHh_QLCe-OpakH03igMvk'  # Replace with your actual bot token
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': handle_message,
                  'callback_query': on_callback_query})

print('Listening for messages...')

# Keep the program running
import time
while True:
    time.sleep(10)
