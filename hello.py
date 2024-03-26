
import telepot
import time
import requests

# Replace with your Flutterwave API keys
# Replace with your Flutterwave API keys
FLUTTERWAVE_PUBLIC_KEY = 'FLWPUBK-0e4658e40b88a018d1451da348f9acab-X'
FLUTTERWAVE_SECRET_KEY = 'FLWSECK-2cfcb60ea041cb576453e651c9ee2e43-18e7acefd71vt-X'

# Telegram bot token
TELEGRAM_TOKEN = '6533833584:AAHPalg1HywEshspXgeGAYOjWRG95jx8X4Q'

# Function to handle messages from Telegram users
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        command = msg['text']

        # Respond to user's greetings
        if command == '/start':
            bot.sendMessage(chat_id, "Welcome! Click on the 'Pay' button below to initiate the payment process.")

        # Handle payment button click
        elif command == 'Pay':
            bot.sendMessage(chat_id, "Please provide your real names, phone number (starting with 256), and email in the following format:\n\nName: [Your Name]\nPhone: [256XXXXXXXXX]\nEmail: [Your Email]")

        # Handle user information submission
        elif command.startswith('Name:') and 'Phone:' in command and 'Email:' in command:
            # Extract user information
            name = command.split('Name:')[1].split('Phone:')[0].strip()
            phone = command.split('Phone:')[1].split('Email:')[0].strip()
            email = command.split('Email:')[1].strip()

            # Initiate payment using Flutterwave API
            payment_details = initiate_payment(name, phone, email)

            # Send payment link to the user
            if payment_details:
                bot.sendMessage(chat_id, f"Payment link: {payment_details['link']}")
            else:
                bot.sendMessage(chat_id, "Failed to initiate payment. Please try again later.")

# Function to initiate payment using Flutterwave API
def initiate_payment(name, phone, email):
    payment_url = 'https://api.flutterwave.com/v3/payments'

    payload = {
        "tx_ref": "test_transaction",
        "amount": "100",
        "currency": "UGX",
        "payment_options": "mobilemoneyuganda",
        "meta": {
            "consumer_id": 23,
            "consumer_mac": "92a3-912ba-1192a"
        },
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

    response = requests.post(payment_url, json=payload, headers=headers)

    if response.status_code == 200:
        payment_data = response.json()
        return payment_data['data']
    else:
        return None

# Telegram bot token
TOKEN = 'your_telegram_bot_token'

# Create a bot instance
bot = telepot.Bot(TOKEN)

# Attach the handle function to the bot to handle messages
bot.message_loop(handle)

print('Listening for messages...')

# Keep the program running
while True:
    time.sleep(10)
