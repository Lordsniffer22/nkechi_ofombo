import telepot
from telepot.loop import MessageLoop
import requests


# Replace with your Flutterwave API keys
# Replace with your Flutterwave API keys
FLUTTERWAVE_PUBLIC_KEY = 'FLWPUBK-0e4658e40b88a018d1451da348f9acab-X'
FLUTTERWAVE_SECRET_KEY = '`FLWSECK-2cfcb60ea041cb576453e651c9ee2e43-18e7acefd71vt-X`'

# Telegram bot token
#TELEGRAM_TOKEN = '7021922965:AAFgpeUCisXYM-s6rDbzhwBtTNZ62jL0x0o'
import telepot
import requests

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
bot = telepot.Bot('7021922965:AAFgpeUCisXYM-s6rDbzhwBtTNZ62jL0x0o')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        try:
            amount = float(msg['text'])
            payment_link = generate_payment_link(amount)
            bot.sendMessage(chat_id, payment_link)
        except ValueError:
            bot.sendMessage(chat_id, "Please enter a valid amount.")

def generate_payment_link(amount):
    # Replace 'YOUR_FLUTTERWAVE_API_KEY' with your actual Flutterwave API key
    headers = {
        'Authorization': 'Bearer FLWPUBK-0e4658e40b88a018d1451da348f9acab-X',
        'Content-Type': 'application/json',
    }
    data = {
        'amount': amount,
        'currency': 'UGX',  # Assuming Ugandan Shilling
        'tx_ref': 'your_transaction_reference',
        'redirect_url': 'your_redirect_url',
        'payment_options': 'mobilemoneyuganda',
        # Add other necessary parameters according to Flutterwave API documentation
    }
    response = requests.post('https://api.flutterwave.com/v3/payments', headers=headers, json=data)
    payment_link = response.json()['data']['link']
    return payment_link

bot.message_loop(handle)

while True:
    pass  # Keep the program running
