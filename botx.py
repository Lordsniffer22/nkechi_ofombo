import requests
import json
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

# Set your Telegram bot API token
API_KEY = "YOUR_TOKEN"

def bot(method, datas=None):
    url = f"https://api.telegram.org/bot{API_KEY}/{method}"
    response = requests.post(url, data=datas)
    return response.json()

def aes_ecb_decrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(b64decode(data))
    return decrypted.rstrip(b"\0").decode()

def aes_ecb_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(data)
    return b64encode(encrypted).decode()

def get_file(file_id):
    response = requests.get(f'https://api.telegram.org/bot{API_KEY}/getFile?file_id={file_id}')
    return response.json()['result']

def process_document(update):
    file_name = update['message']['document']['file_name']

    if '.hat' in file_name:
        file_id = update['message']['document']['file_id']
        file_path = get_file(file_id)['file_path']
        r = str(random.randint(1111, 9999))
        with open(f"{r}.hat", "wb") as file:
            file.write(requests.get(f'https://api.telegram.org/file/bot{API_KEY}/{file_path}').content)

        with open(f"{r}.hat", "rb") as file:
            key = b64decode("zbNkuNCGSLivpEuep3BcNA==")
            data = json.loads(aes_ecb_decrypt(file.read(), key))

        caption = update['message']['caption'] if 'caption' in update['message'] else "NuLL"
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

        bot('sendDocument', {
            'chat_id': update['message']['chat']['id'],
            'document': open(f"{r}.hat", "rb"),
            'caption': cp,
        })

        os.remove(f"{r}.hat")

if __name__ == "__main__":
    update = json.loads(input())  # Replace with actual input or webhook handling
    if 'message' in update and 'document' in update['message']:
        process_document(update)
    elif 'message' in update and 'text' in update['message'] and update['message']['text'] == '/start':
        bot('sendMessage', {
            'chat_id': update['message']['chat']['id'],
            'text': """
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
            """,
            'parse_mode': "html",
        })
