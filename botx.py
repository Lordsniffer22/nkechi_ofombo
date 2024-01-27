import telepot
from telepot.loop import MessageLoop, InlineUserHandler
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from googleapiclient.discovery import build

TELEGRAM_BOT_TOKEN = '6643175652:AAH6haOsyYIUmw6ql8U_5-Bmdocguwzwolc'
YOUTUBE_API_KEY = 'AIzaSyAa-43K1ZF6xYlbPW7A7ufHTpgzkUwsGas'

def handle_messages(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        username = bot.getMe()['username']
        if f'@{username}' in msg['text']:
            search_query = msg['text'].replace(f'@{username}', '').strip()
            results = search_youtube(search_query)
            send_youtube_results(chat_id, results)

def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    results = search_youtube(query_string)
    articles = []

    for idx, result in enumerate(results):
        title = result['title']
        video_id = result['video_id']
        link = f"https://www.youtube.com/watch?v={video_id}"
        content = f"{title}\n{link}"

        articles.append(
            InlineQueryResultArticle(
                id=str(idx),
                title=title,
                input_message_content=InputTextMessageContent(
                    message_text=content
                )
            )
        )

    bot.answerInlineQuery(query_id, articles)

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

bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
MessageLoop(bot, {'chat': handle_messages, 'inline_query': on_inline_query}).run_as_thread()

print('Bot is listening...')

while True:
    pass
