import telepot
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from youtube_search import YoutubeSearch  # You can install it with: pip install youtube-search
import youtube_dl

# Telegram bot API token
TELEGRAM_API_TOKEN = '6724007051:AAG_ZXO7N__TwMQlVFvJuuJmJ1ViBIRWchY'

# Youtube DL options for downloading in mp3 format
ydl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(title)s.%(ext)s',
    'noplaylist': True,
}

# Function to handle inline queries
def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')

    # Search YouTube videos based on the user's query
    videos = YoutubeSearch(query_string, max_results=5).to_dict()

    results = []
    for video in videos:
        title = video['title']
        link = f"https://www.youtube.com/watch?v={video['id']}"
        thumb_url = video['thumbnails'][0]

        # Create an InlineQueryResultArticle with a button to download in mp3
        results.append(InlineQueryResultArticle(
            id=video['id'],
            title=title,
            input_message_content=InputTextMessageContent(
                message_text=f"Click the button to download [**{title}**]({link}) in mp3 format."),
            reply_markup={'inline_keyboard': [[{'text': 'Download Mp3', 'callback_data': video['id']}]]},
            thumb_url=thumb_url
        ))

    # Answer the inline query with the search results
    bot.answerInlineQuery(query_id, results)


# Function to handle callback queries (i.e., when the user clicks on the download button)
def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')

    # Download the selected video in mp3 format
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(f'https://www.youtube.com/watch?v={data}', download=True)
        audio_url = video_info['formats'][0]['url']

        # Send the mp3 file to the user
        bot.sendAudio(from_id, audio_url, title=video_info['title'])


# Create the Telegram bot
bot = telepot.Bot(TELEGRAM_API_TOKEN)

# Set the callback functions
bot.message_loop({'inline_query': on_inline_query, 'callback_query': on_callback_query})

print('Bot is listening...')
while True:
    pass
