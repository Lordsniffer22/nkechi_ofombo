import telepot
import os
import json
import base64
import random
import requests

# Define your Telegram bot's API token
TOKEN = '6710319141:AAE9XrEmt9-Vj6yBXDocq2Tmw9JMfch0i5A'
# Initialize the bot
bot = telepot.Bot(TOKEN)

# Function to handle incoming messages
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    # Check if the message is a document
    if content_type == 'document':
        file_name = msg['document']['file_name']

        # Check if the file has ".hat" extension
        if file_name.endswith('.hat'):
            # Get file_id
            file_id = msg['document']['file_id']

            # Download the file using custom logic
            file_path = download_file_from_telegram(file_id)

            if file_path:
                # Read the downloaded file
                with open(file_path, 'rb') as file:
                    file_data = file.read()

                # Decrypt the file
                key = base64.b64decode("zbNkuNCGSLivpEuep3BcNA==")
                decrypted_data = aes_ecb_decrypt(file_data, key)
                
                # Print decrypted data
                print("Decrypted data:", decrypted_data)

                try:
                    data = json.loads(decrypted_data)

                    # Update data according to certain conditions
                    caption = msg.get('caption', 'NuLL')
                    data['descriptionv5'] = caption
                    data['protextras'] = {
                        'password': False,
                        'expiry': False,
                        'id_lock': False,
                        'block_root': False,
                        'anti_sniff': False
                    }

                    # Encrypt the data
                    encrypted_data = aes_ecb_en(json.dumps(data), key)

                    # Save the encrypted data to a temporary file
                    r = str(random.randint(1111, 9999))
                    with open(f"{r}.hat", 'wb') as file:
                        file.write(encrypted_data.encode())

                    # Prepare caption
                    cp = f"""
├ • Developer :@BOOS_TOOLS
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • 💠 Expiry Time : Disabled
├ • 💠 ID_Lock : Disabled
├ • 💠 Password : Disabled
├ • 💠 Block_Root : Disabled
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • 💠 Description : {caption}
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • BoT ID : @derypterbot
"""

                    # Send the encrypted file to the user
                    with open(f"{r}.hat", 'rb') as file:
                        bot.sendDocument(chat_id, file, caption=cp)

                    # Remove the temporary file
                    os.remove(f"{r}.hat")

                    # Remove the downloaded file
                    os.remove(file_path)
                except json.JSONDecodeError as e:
                    print("Error decoding decrypted data as JSON:", e)
            else:
                print("Failed to download the file from Telegram.")

# Function to download the file from Telegram using file_id
def download_file_from_telegram(file_id):
    try:
        url = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'
        response = requests.get(url)
        if response.status_code == 200:
            file_path = json.loads(response.content)['result']['file_path']
            file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
            file_name = file_path.split('/')[-1]
            file_path = f'{file_name}'  # Specify the path to save the file
            response = requests.get(file_url)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return file_path
        else:
            return None
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

# Function to decrypt AES-ECB encrypted data
def aes_ecb_decrypt(data, key):
    # Implementation of AES decryption
    return data

# Function to encrypt data using AES-ECB
def aes_ecb_en(data, key):
    # Implementation of AES encryption
    return data

# Start the bot
bot.message_loop(handle)

# Keep the program running
while True:
    pass



# Keep the program running
while True:
    pass

