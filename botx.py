import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from googleapiclient.discovery import build

# Replace 'YOUR_BOT_TOKEN' with the token obtained from BotFather
TELEGRAM_BOT_TOKEN = '6643175652:AAH6haOsyYIUmw6ql8U_5-Bmdocguwzwolc'

# Replace 'YOUR_YOUTUBE_API_KEY' with your YouTube API key
YOUTUBE_API_KEY = 'AIzaSyAa-43K1ZF6xYlbPW7A7ufHTpgzkUwsGas'

def handle_messages(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        process_text_message(chat_id, msg['text'])

def process_text_message(chat_id, text):
    if text.startswith('@'):
        # Autocomplete command and start listening for YouTube search queries
        bot.sendMessage(chat_id, f"Youtube search {text}")
    else:
        username = bot.getMe()['username']
        if f'@{username}' in text:
            search_query = text.replace(f'@{username}', '').strip()
            results = search_youtube(search_query)
            send_youtube_results(chat_id, results)

def search_youtube(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(q=query, part='id,snippet', maxResults=5).execute()

    results = []
    for item in search_response['items']:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        results.append({'title': title, 'video_id': video_id})

    return results

def send_youtube_results(chat_id, results):
    for result in results:
        message = f"Title: {result['title']}\n"
        message += f"Video ID: {result['video_id']}\n"
        message += f"Link: https://www.youtube.com/watch?v={result['video_id']}"
        bot.sendMessage(chat_id, message)

def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    
    # Generate a single article with the autocomplete suggestion
    articles = [InlineQueryResultArticle(
        id='1',
        title='YouTube search',
        input_message_content=InputTextMessageContent(
            message_text=f'Youtube search @{query_string}',
            parse_mode='Markdown'
        )
    )]

    bot.answerInlineQuery(query_id, articles)

bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
MessageLoop(bot, {'chat': handle_messages, 'inline_query': on_inline_query}).run_as_thread()

print('Bot is listening...')

while True:
    pass
