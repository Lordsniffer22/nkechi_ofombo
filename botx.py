import telepot
from telepot.loop import MessageLoop
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import os
import random
import json

# Set your Telegram bot API token
API_KEY = "6643175652:AAH6haOsyYIUmw6ql8U_5-Bmdocguwzwolc"

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'document':
        process_document(msg)

    elif content_type == 'text' and msg['text'] == '/start':
        bot.sendMessage(chat_id, """
            <strong>
            <u>🇪🇬This project was made by an Iranian 🇪🇬</u>

            💠 Send Me Ha Tunnel Plus Config and write Caption For Description

            ♻️ The tasks performed by this robot:

            🔹Only Ha Tunnel Plus - .HAT 🔹
            🔻Time makes the use of config unlimited
            🔻The number of users is unlimited
            🔻The password disables the file
            🔻Allows root users to use

            🔹Change the description as desired 🔹

            💠 Channel: @decrypt_file
            💠 Developer: @BOOS_TOOLS</strong>
        """, parse_mode="html")

def bot(method, datas=None):
    return bot.sendMessage(API_KEY, datas)

def aes_ecb_decrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(b64decode(data))
    return decrypted.rstrip(b"\0").decode()

def aes_ecb_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(data)
    return b64encode(encrypted).decode()

def get_file(file_id):
    return bot.getFile(file_id)

def process_document(msg):
    file_name = msg['document']['file_name']

    if '.hat' in file_name:
        file_id = msg['document']['file_id']
        file_path = get_file(file_id)['file_path']
        r = str(random.randint(1111, 9999))

        with open(f"{r}.hat", "wb") as file:
            file.write(requests.get(f'https://api.telegram.org/file/bot{API_KEY}/{file_path}').content)

        with open(f"{r}.hat", "rb") as file:
            key = b64decode("zbNkuNCGSLivpEuep3BcNA==")
            data = json.loads(aes_ecb_decrypt(file.read(), key))

        caption = msg['caption'] if 'caption' in msg else "NuLL"
        data['descriptionv5'] = caption
        data['protextras']['password'] = False
        data['protextras']['expiry'] = False
        data['protextras']['id_lock'] = False
        data['protextras']['block_root'] = False
        data['protextras']['anti_sniff'] = False
        encrypted_data = aes_ecb_encrypt(json.dumps(data), key)

        with open(f"{r}.hat", "wb") as file:
            file.write(encrypted_data.encode())

        cp = f"""
        ├ • Developer : @BOOS_TOOLS
        ├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
        ├ • 💠 Expiry Time  :  Disabled
        ├ • 💠 ID_Lock :  Disabled
        ├ • 💠 Password :  Disabled
        ├ • 💠 Block_Root :  Disabled
        ├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
        ├ • 💠 Description : {caption}
        ├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
        ├ • BoT ID : @derypterbot
        """

        bot.sendDocument(msg['chat']['id'], open(f"{r}.hat", "rb"), caption=cp, parse_mode="html")
        os.remove(f"{r}.hat")

if __name__ == "__main__":
    bot = telepot.Bot(API_KEY)
    MessageLoop(bot, on_chat_message).run_as_thread()

    print('Bot is listening...')
    while True:
        pass  # Keep the program running
