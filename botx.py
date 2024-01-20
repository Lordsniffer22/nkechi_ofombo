import telepot
from pytube import YouTube
from telepot.loop import MessageLoop
from io import BytesIO

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '6724007051:AAG_ZXO7N__TwMQlVFvJuuJmJ1ViBIRWchY'
bot = telepot.Bot(TOKEN)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        message_text = msg['text']

        # Check if the message contains a YouTube link
        if 'youtube.com/watch?v=' in message_text:
            try:
                # Extract the video ID from the link
                video_id = message_text.split('v=')[1].split('&')[0]

                # Create a YouTube object
                yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')

                # Get the highest resolution stream
                stream = yt.streams.get_highest_resolution()

                # Get the video as bytes
                video_bytes = BytesIO()
                stream.download(output_path=video_bytes)

                # Send the video back to the user
                video_bytes.seek(0)
                bot.sendVideo(chat_id, video_bytes)

                # Send a confirmation message
                bot.sendMessage(chat_id, f'Send complete for video with ID {video_id}')

            except Exception as e:
                bot.sendMessage(chat_id, f'Error: {str(e)}')

# Start the bot
MessageLoop(bot, handle).run_as_thread()

while True:
    pass
