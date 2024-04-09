import telepot
import requests
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

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
        records = [f"{record['name']}    -    {record['content']}" for record in data['result']]
        if records:
            return "A Records:\n" + "\n".join(records)
        else:
            return "No A records found."
    else:
        return f"Failed to retrieve DNS records. Status code: {response.status_code}\n{response.text}"

def remove_dns_record(record_name):
    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_API_KEY,
        'Content-Type': 'application/json',
    }

    response = requests.get(f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records?type=A&name={record_name}', headers=headers)

    if response.status_code == 200:
        data = response.json()
        if len(data['result']) == 0:
            return f"No A record found with name {record_name}"
        else:
            record_id = data['result'][0]['id']
            delete_response = requests.delete(f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records/{record_id}', headers=headers)
            if delete_response.status_code == 200:
                return f"A record {record_name} has been removed."
            else:
                return f"Failed to remove A record {record_name}. Status code: {delete_response.status_code}\n{delete_response.text}"
    else:
        return f"Failed to retrieve A record for removal. Status code: {response.status_code}\n{response.text}"

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
        # Define custom keyboard buttons with smaller size in a single row
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Add Record', resize_keyboard=True),
         KeyboardButton(text='Remove Record', resize_keyboard=True),
         KeyboardButton(text='List Records', resize_keyboard=True)],
    ], resize_keyboard=True)
    
    if content_type == 'text':
        command = msg['text']
        
        if command.lower() == 'add record':
            bot.sendMessage(chat_id, "Please enter the DNS record name and IP address in the format [name] [IP address] (e.g., example.com 192.0.2.1):", reply_markup=keyboard)
            pending_add_command[chat_id] = 'add record'

        elif command.lower() == 'list records':
            response = list_dns_records()
            bot.sendMessage(chat_id, response, reply_markup=keyboard)

        elif command.lower() == 'remove record':
            try:
                bot.sendMessage(chat_id, "Hey, to remove a record Please send me the command in the example format below:\n\n/remove john.teslassh.xyz", reply_markup=keyboard)
            except ValueError:
                return f"FAILED BOSS"
        elif command.startswith('/remove'):
            _, record_name = command.split(' ', 1)
            response = remove_dns_record(record_name)
            bot.sendMessage(chat_id, response, reply_markup=keyboard)

        elif chat_id in pending_add_command:
            record_name, record_content = command.split(' ', 1)
            response = add_dns_record(record_name, record_content)
            bot.sendMessage(chat_id, response, reply_markup=keyboard)
            del pending_add_command[chat_id]

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your Telegram Bot token
bot = telepot.Bot('6486401647:AAGaY2kaQyPKkjVttkjUUeENFk5OxpaJXjE')
bot.message_loop(handle)

print('Bot is listening...')

while True:
    pass

