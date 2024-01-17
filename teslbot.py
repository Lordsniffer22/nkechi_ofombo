import telepot
import subprocess
from datetime import datetime, timedelta
import time
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

with open('tokenz.txt', 'r') as file:
    bot_token = file.read().strip()
bot = telepot.Bot(bot_token)

# File path to store the secret key
seckey_file_path = 'seckey.txt'

# Dictionary to store user verification status
user_verification_status = {}
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

def remove_user(username, chat_id):
    # Check if the user is verified
    if not user_verified(chat_id):
        return "🔐 You need to verify yourself first by providing the secret key using /verify command."

    try:
        subprocess.run(['sudo', 'userdel', '--force', username], check=True)
        return f"User {username} removed successfully!"
    except subprocess.CalledProcessError as e:
        return f"Failed to remove user {username}. Error: {e}"

def list_users(chat_id):
    # Check if the user is verified
    if not user_verified(chat_id):
        return "🔐 You need to verify yourself first by providing the secret key using /verify command."

    try:
        users_info = subprocess.check_output(['cat', '/etc/passwd']).decode('utf-8')
        users_list = [line.split(':')[0] for line in users_info.split('\n') if line]
        users_days_remaining = []

        for user in users_list:
            remaining_days = subprocess.check_output(['sudo', 'chage', '-l', user]).decode('utf-8').split('\n')[1].split(':')[1].strip()

            # Exclude users with expiry set to "never"
            if remaining_days.lower() != 'never':
                users_days_remaining.append(f"│ {user}  ⇿     {remaining_days}")

        users_message = "\n".join(users_days_remaining)
        return f"╭─👩🏻‍🦰USERS────🕗EXPIRY DATES─╮\n{users_message} \n╰───────────────────────╯"
    except subprocess.CalledProcessError as e:
        return f"Failed to list users. Error: {e}"

def user_verified(chat_id):
    # Check if the user is verified
    return user_verification_status.get(chat_id, False)

def verify_user(chat_id, secret_key):
    # Verify the secret key against the stored key
    with open(seckey_file_path, 'r') as seckey_file:
        stored_secret_key = seckey_file.read().strip()

    if secret_key == stored_secret_key:
        user_verification_status[chat_id] = True
        return "Verification successful! You can now use /add, /remove, and /users commands."
    else:
        return "Verification failed. Please provide the correct secret key."
    
pending_add_user_command = None
def handle(msg):
    global pending_add_user_command
    content_type, chat_type, chat_id = telepot.glance(msg)

    # Define custom keyboard buttons with smaller size in a single row
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Add User', resize_keyboard=True),
         KeyboardButton(text='Remove User', resize_keyboard=True),
         KeyboardButton(text='List Users', resize_keyboard=True)],
        [KeyboardButton(text='Restart', resize_keyboard=True),
         KeyboardButton(text='Help', resize_keyboard=True),
         KeyboardButton(text='Dev Team', resize_keyboard=True)],
    ], resize_keyboard=True)

    if content_type == 'text':
        command = msg['text']

        if command.lower() == 'start' or command == '/start':
            bot.sendMessage(chat_id, "Welcome to Tesla SSH Bot👽\n\n This is a server administration Tool. To use the Bot as a SUPER USER, please verify your server ownership using /verify command.")
            user_verification_status[chat_id] = False

        elif command.lower() == 'restart':
            start_message = ("♻️ WELCOME TO TESLA SSH BOT👌. \n"
                             "━━━━━━━━━━━━━━━━━━━━━━━━━ \n"
                             "\n"
                             "You can use me to manage users on your server!\n"
                             "\n"
                             "To reload the bot, Press /start\n"
                             "To see the usage guide, Press /help\n"
                             "To add user, Press /add \n"
                             "To remove user, Press /remove \n"
                             "To list users, Press /users \n"
                             "\n"
                             "🔰 Made with spirit. \n"
                             "========================= \n"
                             "By: @TESLASSH \n"
                             "Mastered by: @hackwell101 \n"
                             "Join @udpcustom")

            # Send the start message with the custom keyboard
            bot.sendMessage(chat_id, start_message, reply_markup=keyboard)
            
        elif command.lower() == 'dev team':
            start_message = ("♻️ ZERO ONE LLC 💻. \n"
                             "━━━━━━━━━━━━━━━━ \n"
                             "\n"
                             "Hello, thanks for choosing our cloud projects!\n"
                             "\n"
                             "This Tool was an imagination from @hackwell101, our Team member and founder of @udpcustom\n\n"
                             "Super thanks to the developers:\n"
                             "=============================== \n"
                             "Bot Logic: Ted ( @hackwell101 ) \n"
                             "Program Lang: Tesla SSH ( @teslassh ) \n"
                             "To list users, Press /users \n"
                             "\n"
                             "💖Made with spirit. \n"
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
                            "- To Remove a user, \n"
                            "Send /remove [username]\n"
                            "\n"
                            "- To List all users, \n"
                            "Send /users\n"
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
###########
        if command.lower() == 'add user':
            # Check if the user is verified before allowing to use /add command
            if not user_verified(chat_id):
                bot.sendMessage(chat_id, "🔐 You need to verify yourself first to be a super user! Pass your secret key to the /verify command.")
            else:
                # Set the pending "Add User" command
                pending_add_user_command = command
                bot.sendMessage(chat_id, "Please provide [username] [password] [days] in the next message.", reply_markup=keyboard)

        elif pending_add_user_command:
            # Process the pending "Add User" command
            try:
                _, username, password, days = (pending_add_user_command + ' ' + command).split()[1:]
                response = add_user(username, password, days, user_info="bot", chat_id=chat_id)
                bot.sendMessage(chat_id, response, reply_markup=keyboard)
            except ValueError:
                bot.sendMessage(chat_id, "😳 Oh Oooh...! Something went wrong with processing the 'Add User' command.", reply_markup=keyboard)
            finally:
                # Reset the pending command after processing
                pending_add_user_command = None

        elif command.lower() == 'remove user':
            # Check if the user is verified before allowing to use /remove command
            if not user_verified(chat_id):
                bot.sendMessage(chat_id, "🔐 You need to verify yourself first to be a super user! Pass your secret key to the /verify command.")
            else:
                # Set the pending "Remove User" command
                bot.sendMessage(chat_id, "Please send the [username] to be removed.", reply_markup=keyboard)
                pending_remove_user_command[chat_id] = command

        elif pending_remove_user_command.get(chat_id):
            # Process the pending "Remove User" command
            try:
                _, username = command.split()
                response = remove_user(username, chat_id)
                bot.sendMessage(chat_id, response, reply_markup=keyboard)
            except ValueError:
                bot.sendMessage(chat_id, "😳 Oh Oooh...! Something went wrong with processing the 'Remove User' command.", reply_markup=keyboard)
            finally:
                # Reset the pending command after processing
                pending_remove_user_command.pop(chat_id, None)
        elif command.lower() == 'list users' or command == '/users':
            response = list_users(chat_id)
            bot.sendMessage(chat_id, response, reply_markup=keyboard)

# Set the command handler
bot.message_loop(handle)

# Keep the program running
while True:
    pass
