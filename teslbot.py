import telepot
import subprocess
from datetime import datetime, timedelta
import time
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

# File path to store the secret key
seckey_file_path = 'seckey.txt'

# Dictionary to store user verification status
user_verification_status = {}

with open('tokenz.txt', 'r') as file:
    bot_token = file.read().strip()
bot = telepot.Bot(bot_token)

def add_user(username, password, days, user_info, chat_id):
    # Check if the user is verified
    if not user_verified(chat_id):
        return "🔐 You need to verify yourself first by providing the secret key using /verify command."

    current_date = datetime.now()
    expiration_date = current_date + timedelta(days=int(days))
    expiration_date_str = expiration_date.strftime('%Y-%m-%d')

    # Check if the user already exists
    existing_users = subprocess.check_output(['cat', '/etc/passwd']).decode('utf-8')
    if f'{username}:' in existing_users and user_info.lower() not in existing_users.lower():
        return f"User {username} already exists with a different info."

    # Generate hashed password
    osl_version = subprocess.check_output(['openssl', 'version']).decode('utf-8')
    osl_version = osl_version.split()[1][:5]
    password_option = '-6' if osl_version == '1.1.1' else '-1'
    passs = subprocess.check_output(['openssl', 'passwd', password_option, password]).decode('utf-8').strip()

    # Create user
    try:
        subprocess.run(['sudo', 'useradd', '-M', '-s', '/bin/false', '-e', expiration_date_str, '-K', f'PASS_MAX_DAYS={days}', '-p', passs, '-c', f'{user_info},{password}', username], check=True)

        # Get server IP address
        server_ip = subprocess.check_output(['hostname', '-I']).decode('utf-8').strip()

        # Send success message with details
        success_message = f"User {username} added successfully!\n\nServer Details:\n{server_ip}:1-65535@{username}:{password}"
        return success_message
    except subprocess.CalledProcessError as e:
        return f"Failed to add user {username}. Error: {e}"

def user_verified(chat_id):
    # Check if the user is verified
    return user_verification_status.get(chat_id, False)

def verify_user(chat_id, secret_key):
    # Verify the secret key against the stored key
    with open(seckey_file_path, 'r') as seckey_file:
        stored_secret_key = seckey_file.read().strip()

    if secret_key == stored_secret_key:
        user_verification_status[chat_id] = True
        return "Verification successful! You can now use /add command."
    else:
        return "Verification failed. Please provide the correct secret key."

def detail_user(chat_id):
    active_users = subprocess.check_output(['cat', '/etc/passwd']).decode('utf-8').split('\n')
    user_details = []

    for user_info in active_users:
        if 'home' in user_info and 'false' in user_info and '::/' not in user_info and 'hwid' not in user_info and 'token' not in user_info:
            user = user_info.split(':')[0]
            expiration_info = subprocess.check_output(['chage', '-l', user]).decode('utf-8').split('\n')[3]
            password_info = user_info.split(':')[5]
            status_info = subprocess.check_output(['passwd', '--status', user]).decode('utf-8').split()[1]

            user_details.append({
                'user': user,
                'expiration_info': expiration_info,
                'password_info': password_info,
                'status_info': status_info
            })

    if not user_details:
        return "No registered users."

    message = "Details of registered users:\n"
    for user_info in user_details:
        message += f"{user_info['user']} :: {user_info['expiration_info']} days\n"

    return message

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    # Define custom keyboard buttons with smaller size in a single row
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Restart', resize_keyboard=True),
         KeyboardButton(text='Add User', resize_keyboard=True),
         KeyboardButton(text='Help', resize_keyboard=True)],
    ], resize_keyboard=True)

    if content_type == 'text':
        command = msg['text']

        if command.lower() == 'start' or command == '/start':
            bot.sendMessage(chat_id, "Welcome to Tesla SSH Bot👽\n\n This is a server administration Tool. To use the Bot as a SUPER USER, please verify your server ownership using /verify command.")
            user_verification_status[chat_id] = False

        elif command.lower() == 'restart':
            start_message = ("🔰 WELCOME TO TESLA SSH BOT 🔰. \n"
                             "━━━━━━━━━━━━━━━━━━━━━━━━━ \n"
                             "\n"
                             "You can use me to add users to your server!\n"
                             "\n"
                             "To reload the bot, Press /start\n"
                             "To see the usage guide, Press /help\n"
                             "To add user, Press /add \n"
                             "\n"
                             "🔰 Made with spirit. \n"
                             "========================= \n"
                             "By: @TESLASSH \n"
                             "Mastered by: @hackwell101 \n"
                             "Join @udpcustom")

            # Send the start message with the custom keyboard
            bot.sendMessage(chat_id, start_message, reply_markup=keyboard)

        elif command.lower() == 'help':
            help_message = ("HOW TO USE BOT:\n"
                            "━━━━━━━━━━━━━━━━━━━━━━━━━"
                            "\n"
                            "- To Add a new user, \n"
                            "Send /add [username] [password] [days]\n"
                            "\n"
                            "Example:\n" "/add Nicolas passwad 30\n"
                            "\n"
                            "if you are facing issues with the bot,\n"
                            "press /start\n"
                            "\n"
                            "Contact: @teslassh"
                            )
            bot.sendMessage(chat_id, help_message, reply_markup=keyboard)

        elif command.lower() == 'verify':
            # Prompt user to enter the secret key for verification
            bot.sendMessage(chat_id, "Please enter the secret key🔑 for verification. \n Get it from the Bot manager on your server. \n\n SSH into your server and type: 👉 bot , \n and then press enter")
            user_verification_status[chat_id] = False

        elif command.lower().startswith('/verify'):
            try:
                _, secret_key = command.split()
                response = verify_user(chat_id, secret_key)
                bot.sendMessage(chat_id, response, reply_markup=keyboard)
            except ValueError:
                bot.sendMessage(chat_id, "😳 Oh Oooh...! You entered it wrongly. \n\n ✳️ To verify, Use this format: \n \n👉   /verify XXXXXXXXXXX \n \n Where XXXXXXXXXX is your SECRET KEY you got from your VPS server 💻", reply_markup=keyboard)

        elif command.lower() == 'add user':
            # Check if the user is verified before allowing to use /add command
            if not user_verified(chat_id):
                bot.sendMessage(chat_id, "🔐 You need to verify yourself first in order to be a super user! Pass your secret key to the  /verify command.")
            else:
                bot.sendMessage(chat_id, "To add a user, send:\n  /add [username] [password] [days] \n\n Example:\n /add Nicolas passwad 30\n", reply_markup=keyboard)

        elif command.startswith('/add'):
            # Check if the user is verified before allowing to use /add command
            if not user_verified(chat_id):
                bot.sendMessage(chat_id, "🔐 You need to verify yourself first in order to be a super user! \n\n Pass your secret key to the  /verify command.")
            else:
                try:
                    _, username, password, days = command.split()
                    # Introduce a sleep of 3 seconds
                    time.sleep(3)
                    response = add_user(username, password, days, user_info="bot", chat_id=chat_id)
                    bot.sendMessage(chat_id, response, reply_markup=keyboard)
                except ValueError:
                    bot.sendMessage(chat_id, "😳 Oh Oooh...! You entered it wrongly. \n\n Try:  /add [username] [password] [days] \n\n Example:\n /add Nicolas passwad 30\n", reply_markup=keyboard)

        elif command.lower() == 'users':
            # Check if the user is verified before allowing to use /users command
            if not user_verified(chat_id):
                bot.sendMessage(chat_id, "🔐 You need to verify yourself first in order to use /users command.")
            else:
                response = detail_user(chat_id)
                bot.sendMessage(chat_id, response, reply_markup=keyboard)

# Set the command handler
bot.message_loop(handle)

# Keep the program running
while True:
    pass
