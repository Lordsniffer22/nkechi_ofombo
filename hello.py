import telepot
import requests

# Cloudflare API configuration
CLOUDFLARE_API_KEY = 'a4028ce12fc7e7467b950b69ca480df447ba2'
CLOUDFLARE_EMAIL = 'tariusblake@gmail.com'
CLOUDFLARE_ZONE_ID = 'c8b5f50e69aff8cd79d1fea03ad40146'

pending_add_command = {}

def get_domain(zone_id):
    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_API_KEY,
        'Content-Type': 'application/json',
    }

    response = requests.get(f'https://api.cloudflare.com/client/v4/zones/{zone_id}', headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['result']['name']
    else:
        return None

def add_dns_record(record_name, record_content):
    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_API_KEY,
        'Content-Type': 'application/json',
    }

    data = {
        'type': 'A',
        'name': record_name,
        'content': record_content,
        'proxied': False
    }

    response = requests.post(f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records', headers=headers, json=data)

    if response.status_code == 200:
        domain = get_domain(CLOUDFLARE_ZONE_ID)
        if domain:
            return f"DNS record {record_name}.{domain} has been created."
        else:
            return f"Failed to retrieve domain for zone ID: {CLOUDFLARE_ZONE_ID}"
    else:
        return f"Failed to add DNS record. Status code: {response.status_code}\n{response.text}"

def list_dns_records():
    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_API_KEY,
        'Content-Type': 'application/json',
    }

    response = requests.get(f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records?type=A', headers=headers)

    if response.status_code == 200:
        data = response.json()
        records = [f"{record['name']} - {record['content']}" for record in data['result']]
        if records:
            return "A Records:\n" + "\n".join(records)
        else:
            return "No A records found."
    else:
        return f"Failed to retrieve DNS records. Status code: {response.status_code}\n{response.text}"

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text':
        command = msg['text']
        
        if command.startswith('/addrecord'):
            bot.sendMessage(chat_id, "Please enter the DNS record name and IP address in the format [name] [IP address] (e.g., example.com 192.0.2.1):")
            pending_add_command[chat_id] = '/addrecord'

        elif command == '/list':
            response = list_dns_records()
            bot.sendMessage(chat_id, response)

        elif chat_id in pending_add_command:
            record_name, record_content = command.split(' ', 1)
            response = add_dns_record(record_name, record_content)
            bot.sendMessage(chat_id, response)
            del pending_add_command[chat_id]

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your Telegram Bot token
bot = telepot.Bot('6486401647:AAGaY2kaQyPKkjVttkjUUeENFk5OxpaJXjE')
bot.message_loop(handle)

print('Bot is listening...')

while True:
    pass

