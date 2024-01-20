import telepot
from pytube import YouTube
from telepot.loop import MessageLoop
import tempfile
import os

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

                # Create a temporary file to save the video
                with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                    # Download the video to the temporary file
                    stream.download(output_path=temp_file.name)

                    # Send the video back to the user
                    bot.sendVideo(chat_id, open(temp_file.name, 'rb'))

                # Send a confirmation message
                bot.sendMessage(chat_id, f'Send complete for video with ID {video_id}')

            except Exception as e:
                bot.sendMessage(chat_id, f'Error: {str(e)}')

# Start the bot
MessageLoop(bot, handle).run_as_thread()

while True:
    pass
