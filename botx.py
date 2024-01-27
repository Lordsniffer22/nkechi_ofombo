import os
import random
import json
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import telepot

# Set your Telegram bot API token
API_KEY = "6643175652:AAH6haOsyYIUmw6ql8U_5-Bmdocguwzwolc"
bot = telepot.Bot(API_KEY)

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

def process_document(update):
    file_name = update['document']['file_name']

    if '.hat' in file_name:
        file_id = update['document']['file_id']
        file_path = get_file(file_id)['file_path']
        r = str(random.randint(1111, 9999))
        with open(f"{r}.hat", "wb") as file:
            file.write(bot.download_file(file_path))

        with open(f"{r}.hat", "rb") as file:
            key = b64decode("zbNkuNCGSLivpEuep3BcNA==")
            data = json.loads(aes_ecb_decrypt(file.read(), key))

        caption = update['caption'] if 'caption' in update else "NuLL"
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

        bot.sendDocument(update['chat']['id'], document=open(f"{r}.hat", "rb"), caption=cp)

        os.remove(f"{r}.hat")

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

if __name__ == "__main__":
    # Token will be passed as a command-line argument when running the script
    token = os.getenv("6643175652:AAH6haOsyYIUmw6ql8U_5-Bmdocguwzwolc")  # You can set your bot token here or use an environment variable
    if not token:
        print("Error: Telegram bot token is missing.")
    else:
        bot = telepot.Bot(token)
        bot.message_loop(on_chat_message)

        print("Listening for messages...")
        import time
        while True:
            time.sleep(10)
