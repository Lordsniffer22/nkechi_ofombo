import telepot
from pytube import YouTube
from telepot.loop import MessageLoop

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

                # Download the video
                file_path = f'{video_id}.mp4'
                stream.download(filename=file_path)

                # Send the video back to the user
                with open(file_path, 'rb') as video_file:
                    bot.sendVideo(chat_id, video_file)

                # Send a confirmation message
                bot.sendMessage(chat_id, f'Download and send complete for video with ID {video_id}')

            except Exception as e:
                bot.sendMessage(chat_id, f'Error: {str(e)}')

# Start the bot
MessageLoop(bot, handle).run_as_thread()

while True:
    pass
