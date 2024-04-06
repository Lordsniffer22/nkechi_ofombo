import json
import requests
import os
from urllib.parse import urlencode

# Channel : @decrypt_file
# Developer : @BOOS_TOOLS 🇪🇬

# Need Edit Line 9
API_KEY = "6710319141:AAE9XrEmt9-Vj6yBXDocq2Tmw9JMfch0i5A"  # Put Token

def bot(method, datas=None):
    url = f"https://api.telegram.org/bot{API_KEY}/{method}"
    response = requests.post(url, data=datas)
    if response.status_code != 200:
        print(f"Error: {response.text}")
    else:
        return response.json()

# Channel : @decrypt_file
# Developer : @BOOS_TOOLS

def aes_ecb_decrypt(data, key):
    cipher = "aes-128-ecb"
    decrypted = ""
    try:
        decrypted = requests.post(f"https://api.telegram.org/bot{API_KEY}/decrypt", data={"data": data, "key": key}).text
    except Exception as e:
        print(f"Error in AES decryption: {e}")
    return decrypted

def aes_ecb_en(data, key):
    cipher = "aes-128-ecb"
    encrypted = ""
    try:
        encrypted = requests.post(f"https://api.telegram.org/bot{API_KEY}/encrypt", data={"data": data, "key": key}).text
    except Exception as e:
        print(f"Error in AES encryption: {e}")
    return encrypted

def get_file(file_id):
    response = requests.get(f"https://api.telegram.org/bot{API_KEY}/getFile?file_id={file_id}")
    return response.json()

# Channel : @decrypt_file
# Developer : @BOOS_TOOLS

def handle_message(update):
    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    caption = message.get("caption", "")
    if "document" in message:
        file_name = message["document"]["file_name"]
        if '.hat' in file_name:
            file_id = message["document"]["file_id"]
            file_info = get_file(file_id)["result"]
            file_path = file_info["file_path"]
            r = str(random.randint(1111, 9999))
            with open(f"{r}.hat", "wb") as file:
                file.write(requests.get(f"https://api.telegram.org/file/bot{API_KEY}/{file_path}").content)
            with open(f"{r}.hat", "rb") as file:
                file_data = file.read()
            key = base64.b64decode("zbNkuNCGSLivpEuep3BcNA==")
            decrypted_data = aes_ecb_decrypt(file_data, key)
            data = json.loads(decrypted_data)
            if caption == "":
                cap = "NuLL"
            else:
                cap = caption
            data["descriptionv5"] = cap
            data["protextras"]["password"] = False
            data["protextras"]["expiry"] = False
            data["protextras"]["id_lock"] = False
            data["protextras"]["block_root"] = False
            data["protextras"]["anti_sniff"] = False
            encrypted_data = aes_ecb_en(json.dumps(data), key)
            with open(f"{r}.hat", "wb") as file:
                file.write(encrypted_data.encode())
            cp = f"""
├ • Developer :@BOOS_TOOLS
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • 💠 Expiry Time : Disabled
├ • 💠 ID_Lock : Disabled
├ • 💠 Password : Disabled
├ • 💠 Block_Root : Disabled
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • 💠 Description : {cap}
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • BoT ID : @derypterbot
"""
            bot("sendDocument", {"chat_id": chat_id, "document": open(f"{r}.hat", "rb"), "caption": cp})
            os.unlink(f"{r}.hat")
    elif text == "/start":
        bot("sendMessage", {"chat_id": chat_id, "text": """
🇪🇬This project was made by an Iranian 🇪🇬

💠 Send Me Ha Tunnel Plus Config and write Caption For Description

♻️ The tasks performed by this robot:

🔹Only Ha Tunnel Plus - .HAT 🔹
🔻Time makes the use of config unlimited
🔻The number of users is unlimited
🔻The password disables the file
🔻Allows root users to use

🔹Change the description as desired 🔹

💠 Channel: @decrypt_file
💠 Developer: @BOOS_TOOLS
""", "parse_mode": "HTML"})

# Channel : @decrypt_file
# Developer : @BOOS_TOOLS

if __name__ == "__main__":
    handle_message(json.loads(input()))
