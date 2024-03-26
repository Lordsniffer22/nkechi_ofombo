
import telepot
import time
import requests

# Replace with your Flutterwave API keys
# Replace with your Flutterwave API keys
FLUTTERWAVE_PUBLIC_KEY = 'FLWPUBK-0e4658e40b88a018d1451da348f9acab-X'
FLUTTERWAVE_SECRET_KEY = 'FLWSECK-2cfcb60ea041cb576453e651c9ee2e43-18e7acefd71vt-X'

# Telegram bot token
TELEGRAM_TOKEN = '6533833584:AAHPalg1HywEshspXgeGAYOjWRG95jx8X4Q'
# Replace with your Flutterwave API keys


# Function to handle incoming messages
def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        if msg['text'] == '/start':
            # Send welcome message and payment button
            bot.sendMessage(chat_id, "Welcome to our Telegram Bot! Click the button below to make a payment.",
                            reply_markup={'keyboard': [['Pay']],'one_time_keyboard': True})
        elif msg['text'] == 'Pay':
            bot.sendMessage(chat_id, "Please provide your real name, phone number (starting with 256), and email address in the format:\n\n"
                                      "Name: [Your Name]\n"
                                      "Phone: [256XXXXXXXXX]\n"
                                      "Email: [Your Email]")
        elif 'Name:' in msg['text'] and 'Phone:' in msg['text'] and 'Email:' in msg['text']:
            # Extract user information
            name = msg['text'].split('Name: ')[1].split('\n')[0].strip()
            phone = msg['text'].split('Phone: ')[1].split('\n')[0].strip()
            email = msg['text'].split('Email: ')[1].strip()

            # Prepare payload for Flutterwave
            payload = {
                "tx_ref": "test_transaction",
                "amount": "100",
                "currency": "UGX",
                "payment_options": "mobilemoneyuganda",
                "redirect_url": "https://your-redirect-url.com",
                "customer": {
                    "email": email,
                    "phone_number": phone,
                    "name": name
                },
                "customizations": {
                    "title": "Test Payment",
                    "description": "Payment for test purposes"
                }
            }

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {FLUTTERWAVE_SECRET_KEY}'
            }

            # Initiate payment
            response = requests.post('https://api.flutterwave.com/v3/payments', json=payload, headers=headers)

            if response.status_code == 200:
                payment_data = response.json()
                payment_link = payment_data['data']['link']
                bot.sendMessage(chat_id, f"Please complete your payment by clicking on the link below:\n{payment_link}")
            else:
                bot.sendMessage(chat_id, "Failed to initiate payment. Please try again later.")
        else:
            bot.sendMessage(chat_id, "Invalid command. Please click on the 'Pay' button to initiate a payment.")

# Replace 'your_bot_token' with your Telegram bot token
bot = telepot.Bot('your_bot_token6533833584:AAHPalg1HywEshspXgeGAYOjWRG95jx8X4Q')
MessageLoop(bot, handle_message).run_as_thread()

print('Bot is listening...')
