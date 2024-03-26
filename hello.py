import telepot
from telepot.loop import MessageLoop
import requests


# Replace with your Flutterwave API keys
# Replace with your Flutterwave API keys
FLUTTERWAVE_PUBLIC_KEY = 'FLWPUBK-0e4658e40b88a018d1451da348f9acab-X'
FLUTTERWAVE_SECRET_KEY = 'FLWSECK-2cfcb60ea041cb576453e651c9ee2e43-18e7acefd71vt-X'

# Telegram bot token
TELEGRAM_TOKEN = '6533833584:AAHPalg1HywEshspXgeGAYOjWRG95jx8X4Q'

# Function to handle incoming messages
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        command = msg['text']
        if command == '/start':
            bot.sendMessage(chat_id, "Welcome! Click on the pay button to initiate payment.")
        elif command == '/pay':
            bot.sendMessage(chat_id, "Please provide your real name, phone number (starting with 256), and email in the format: Name, 256XXXXXXXXX, email@example.com")
        else:
            bot.sendMessage(chat_id, "Invalid command. Click on the pay button to initiate payment.")

    # Handle user input for payment details
    elif content_type == 'contact':
        contact = msg['contact']
        name = contact['first_name']
        phone_number = contact['phone_number']
        email = msg['text']
        
        # Call Flutterwave API to initiate payment
        payment_url = 'https://api.flutterwave.com/v3/payments'
        payload = {
            "tx_ref": "test_transaction",
            "amount": "100",
            "currency": "UGX",
            "payment_options": "mobilemoneyuganda",
            "redirect_url": "https://your-redirect-url.com",
            "meta": {
                "consumer_id": 23,
                "consumer_mac": "92a3-912ba-1192a"
            },
            "customer": {
                "email": email,
                "phone_number": phone_number,
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
            payment_link = payment_data['data']['link']
            bot.sendMessage(chat_id, f"Payment link: {payment_link}")
        else:
            bot.sendMessage(chat_id, "Failed to initiate payment. Please try again later.")

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
bot = telepot.Bot('6533833584:AAHPalg1HywEshspXgeGAYOjWRG95jx8X4Q')
MessageLoop(bot, handle).run_as_thread()

print('Bot is listening...')
