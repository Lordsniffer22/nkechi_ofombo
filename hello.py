import telepot
import requests

# Cloudflare API configuration
CLOUDFLARE_API_KEY = 'a4028ce12fc7e7467b950b69ca480df447ba2'
CLOUDFLARE_EMAIL = 'tariusblake@gmail.com'
CLOUDFLARE_ZONE_ID = 'c8b5f50e69aff8cd79d1fea03ad40146'

def add_dns_record(record_name, record_type, record_content, proxied=False):
    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_API_KEY,
        'Content-Type': 'application/json',
    }

    data = {
        'type': record_type,
        'name': record_name,
        'content': record_content,
        'proxied': proxied
    }

    response = requests.post(f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records', headers=headers, json=data)

    if response.status_code == 200:
        return "DNS record added successfully."
    else:
        return f"Failed to add DNS record. Status code: {response.status_code}\n{response.text}"

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text':
        command = msg['text']
        
        if command.startswith('/addrecord'):
            _, record_name, record_type, record_content, proxied_str = command.split()
            proxied = True if proxied_str.lower() == 'true' else False
            
            response = add_dns_record(record_name, record_type, record_content, proxied)
            bot.sendMessage(chat_id, response)

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your Telegram Bot token
bot = telepot.Bot('6486401647:AAGaY2kaQyPKkjVttkjUUeENFk5OxpaJXjE')
bot.message_loop(handle)

print('Bot is listening...')

while True:
    pass
