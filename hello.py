
import telepot
import time
import requests

# Replace with your Flutterwave API keys
# Replace with your Flutterwave API keys
FLUTTERWAVE_PUBLIC_KEY = 'FLWPUBK-0e4658e40b88a018d1451da348f9acab-X'
FLUTTERWAVE_SECRET_KEY = 'FLWSECK-2cfcb60ea041cb576453e651c9ee2e43-18e7acefd71vt-X'

# Telegram bot token
TELEGRAM_TOKEN = '6533833584:AAHPalg1HywEshspXgeGAYOjWRG95jx8X4Q'

# Initialize Telegram bot
bot = telepot.Bot(TELEGRAM_TOKEN)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    # Handle text messages
    if content_type == 'text':
        command = msg['text']

        # Start command
        if command == '/start':
            bot.sendMessage(chat_id, "Welcome to the Payment Bot! Click on the Pay button to proceed.",
                            reply_markup={'inline_keyboard': [[{'text': 'Pay', 'callback_data': 'pay'}]]})
        elif command == '/help':
            bot.sendMessage(chat_id, "This bot helps you make payments easily. Click on the Pay button to get started.")
        else:
            bot.sendMessage(chat_id, "I'm sorry, I don't understand that command.")

    # Handle inline button clicks
    elif command == '/pay':
            bot.sendMessage(chat_id, "Please provide your details in the format: Full Name, Phone Number (with country code), Email.")

def initiate_payment(full_name, phone_number, email):
    # Endpoint for initiating payment
    payment_url = 'https://api.flutterwave.com/v3/payments'

    # Sample payload for initiating payment
    payload = {
        "tx_ref": "test_transaction",
        "amount": "100",
        "currency": "UGX",
        "payment_options": "mobilemoneyuganda",
        "redirect_url": "https://your-redirect-url.com",
        "customer": {
            "email": email,
            "phone_number": phone_number,
            "name": full_name
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {FLUTTERWAVE_SECRET_KEY}'
    }

    # Initiate payment
    response = requests.post(payment_url, json=payload, headers=headers)

    # Check response
    if response.status_code == 200:
        payment_data = response.json()
        payment_details = payment_data['data']
        payment_link = payment_details['link']
        return payment_link
    else:
        return None

def on_close():
    print("Bot is closing...")

bot.message_loop({'chat': handle,
                  'callback_query': handle})

print('Listening...')

# Keep the program running
while True:
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        on_close()
        break
