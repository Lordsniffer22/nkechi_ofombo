import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import youtube_dl

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '6724007051:AAG_ZXO7N__TwMQlVFvJuuJmJ1ViBIRWchY'

# Function to handle inline queries
def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')

    # Create a list of InlineKeyboardButton for each search result
    inline_keyboard = []
    
    # Use youtube_dl to search for videos based on the query
    with youtube_dl.YoutubeDL({}) as ydl:
        search_results = ydl.extract_info(f"ytsearch:{query_string}", download=False)
        
        for result in search_results.get('entries', []):
            title = result.get('title', 'Unknown Title')
            video_id = result.get('id', '')
            inline_keyboard.append([InlineKeyboardButton(text=title, callback_data=f'download:{video_id}')])

    # Create InlineKeyboardMarkup with the list of buttons
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    # Answer the inline query with the InlineKeyboardMarkup
    bot.answerInlineQuery(query_id, markup)

# Function to handle callback queries (when a button is clicked)
def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    
    # Check if the callback data starts with 'download:'
    if data.startswith('download:'):
        video_id = data.split(':')[1]
        
        # Use youtube_dl to download the video in mp3 format
        with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
            info = ydl.extract_info(video_id, download=False)
            url = info['formats'][0]['url']  # Get the URL of the best audio format
            bot.sendAudio(from_id, url, title=info['title'])

# Function to handle regular messages
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    # Respond only to text messages
    if content_type == 'text':
        bot.sendMessage(chat_id, "To search for YouTube videos, please use inline mode. Start your message with @YourBotName.")

# Create the bot and set the event handlers
bot = telepot.Bot(TOKEN)
bot.message_loop({'inline_query': on_inline_query, 'callback_query': on_callback_query, 'chat': on_chat_message})

print('Bot is listening...')

# Keep the program running
import time
while True:
    time.sleep(10)
