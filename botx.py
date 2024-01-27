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

    if content_type == 'inline_query':
        query_id, query_text, _ = telepot.glance(msg, flavor='inline_query')
        results = search_youtube(query_text)
        answer_inline_query(query_id, results)

def search_youtube(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(q=query, part='id,snippet', maxResults=5).execute()

    results = []
    for item in search_response['items']:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        results.append(
            InlineQueryResultArticle(
                id=video_id,
                title=title,
                input_message_content=InputTextMessageContent(
                    message_text=f"Title: {title}\n"
                                 f"Video ID: {video_id}\n"
                                 f"Link: https://www.youtube.com/watch?v={video_id}"
                )
            )
        )

    return results

def answer_inline_query(query_id, results):
    bot.answerInlineQuery(query_id, results, cache_time=0)

bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
MessageLoop(bot, handle_messages).run_as_thread()

print('Bot is listening...')

while True:
    pass

