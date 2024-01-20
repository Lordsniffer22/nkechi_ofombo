import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from youtube_dl import YoutubeDL

TOKEN = '6724007051:AAG_ZXO7N__TwMQlVFvJuuJmJ1ViBIRWchY'

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        search_query = msg['text']

        # Perform YouTube search
        videos = search_youtube(search_query)

        if videos:
            # Create inline keyboard with video options
            keyboard = create_inline_keyboard(videos)

            # Send message with inline keyboard
            bot.sendMessage(chat_id, 'Select a video:', reply_markup=keyboard)
        else:
            bot.sendMessage(chat_id, 'No videos found for the given query.')

def search_youtube(query):
    # Use youtube_dl to search for videos
    ydl_opts = {'format': 'best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}
    with YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(f'ytsearch:{query}', download=False)
            if 'entries' in result:
                return result['entries']
        except Exception as e:
            print(f'Error searching YouTube: {e}')
    return None

def create_inline_keyboard(videos):
    # Create inline keyboard with video options
    keyboard = []
    for video in videos:
        title = video.get('title', 'Unknown Title')
        video_id = video.get('id', '')
        keyboard.append([InlineKeyboardButton(text=title, callback_data=f'download_{video_id}')])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    if query_data.startswith('download_'):
        video_id = query_data.split('_')[1]
        download_and_send_audio(from_id, video_id)

def download_and_send_audio(chat_id, video_id):
    # Download and send the audio file to the user
    ydl_opts = {'format': 'best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}
    with YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(video_id, download=True)
            if 'entries' in result:
                audio_file = result['entries'][0]['title'] + '.mp3'
                bot.sendAudio(chat_id, open(audio_file, 'rb'))
        except Exception as e:
            print(f'Error downloading audio: {e}')

# Initialize the bot and set callback function
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': handle, 'callback_query': on_callback_query})

print('Listening for messages...')
import time
while 1:
    time.sleep(10)
