# Made with love by Teslassh
# Stealing this source code is illegal as always.
# #You are allowed to use the tool in any way you wish
import telepot
import subprocess
import os
from pytube import YouTube
# import json
from datetime import datetime, timedelta
import time
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

with open('tokenz.txt', 'r') as file:
    bot_token = file.read().strip()
bot = telepot.Bot(bot_token)
# File path to store the secret key
# seckey_file_path = 'seckey.txt'
domain_file_path = 'pydomain.txt'


def save_domain(domain):
    with open(domain_file_path, 'w') as domain_file:
        domain_file.write(domain)

def nodomain(chat_id):
    try:
        with open('pydomain.txt', 'w') as file:
            file.write("")
            return "Domain has been removed."
    except Exception as e:
        return f"Failed to remove the domain"
def currentdomain(chat_id):
    try:
        with open('pydomain.txt', 'r') as info:
            domain = info.read().strip()
            if domain:
                return "Current domain is: " + domain
            else:
                return "This server has no domain yet"
    except Exception as e:
        return f"Failed to retrieve the current domain"



def check_bbr_status(chat_id):
    try:
        status = subprocess.check_output(['sysctl', 'net.ipv4.tcp_congestion_control']).decode('utf-8')
        return 'bbr' in status
    except subprocess.CalledProcessError as e:
        print(f"Error checking BBR status: {e}")
        return False


def enable_bbr(chat_id):
    try:
        if not check_bbr_status(chat_id):
            subprocess.run(['modprobe', 'tcp_bbr'])
            with open('/etc/sysctl.conf', 'r') as f:
                if 'net.ipv4.tcp_congestion_control=bbr' not in f.read():
                    with open('/etc/sysctl.conf', 'a') as f:
                        f.write('net.core.default_qdisc=fq \nnet.ipv4.tcp_congestion_control=bbr\n')
            subprocess.run(['sysctl', '-p'])
            bot.sendMessage(chat_id, 'BBR has been enabled successfully! Enjoy the better connections')
        else:
            bot.sendMessage(chat_id, 'BBR is already running. No need to activate it again.')
    except subprocess.CalledProcessError as e:
        print(f"Error enabling BBR: {e}")
        bot.sendMessage(chat_id, 'Failed to enable BBR. Contact the bot administrator.')
def get_domain():
    try:
        with open(domain_file_path, 'r') as domain_file:
            return domain_file.read().strip()
    except FileNotFoundError:
        return None


def add_user(username, password, days, user_info, chat_id):
    # Check if the user is verified
    # if not is_verified(chat_id):
    #    return "🔐 You need to verify yourself first by providing the secret key using /verify command."

    current_date = datetime.now()
    expiration_date = current_date + timedelta(days=int(days))
    expiration_date_str = expiration_date.strftime('%Y-%m-%d')

    # Check if the user already exists
    existing_users = subprocess.check_output(['cat', '/etc/passwd']).decode('utf-8')
    if f'{username}:' in existing_users and user_info.lower() not in existing_users.lower():
        return f"{username} already exists with a different info."

    # Generate hashed password
    osl_version = subprocess.check_output(['openssl', 'version']).decode('utf-8')
    osl_version = osl_version.split()[1][:5]
    password_option = '-6' if osl_version == '1.1.1' else '-1'
    passs = subprocess.check_output(['openssl', 'passwd', password_option, password]).decode('utf-8').strip()

    # Create user
    try:
        subprocess.run(
            ['sudo', 'useradd', '-M', '-s', '/bin/false', '-e', expiration_date_str, '-K', f'PASS_MAX_DAYS={days}',
             '-p', passs, '-c', f'{user_info},{password}', username], check=True)

        # Get server IP address or saved domain
        server_info = get_domain() or subprocess.check_output(['hostname', '-I']).decode('utf-8').strip().split()[0]

        # Send success message with details
        success_message = f" {username} has been added successfully!\n\nServer Details:\n{server_info}:1-65535@{username}:{password}"
        return success_message
    except subprocess.CalledProcessError as e:
        return f"Failed to add user {username} because He already exists."


def remove_user(username, chat_id):
    try:
        subprocess.run(['sudo', 'userdel', '--force', username], check=True)
        subprocess.run(['sudo', 'systemctl', 'restart', 'udp-custom'], check=True)
        return f"{username} Has been removed successfully!"
    except subprocess.CalledProcessError as e:
        return f"🤡 {username} seems to be a command or that user does not exist.\n✌️Try a different spelling"


def reboot_server(chat_id):
    try:
        time.sleep(4)
        subprocess.run(['reboot'], check=True)
    except subprocess.CalledProcessError as e:
        return f"Failed to reboot server. Error: {e}"


# Function to check if a message is a YouTube link
def is_youtube_link(text):
    return text.startswith('https://www.youtube.com/') or text.startswith('https://youtu.be/')


# Function to download a YouTube video and convert it to MP3
def download_and_convert_to_mp3(video_url):
    yt = YouTube(video_url)
    video_title = yt.title
    stream = yt.streams.filter(only_audio=True).first()
    if stream:
        file_path = stream.download()
        mp3_file = f"{video_title}.mp3"
        os.rename(file_path, mp3_file)
        return mp3_file
    else:
        return None


# Function to send an MP3 file to the user with a caption
def send_mp3_file(chat_id, video_url):
    mp3_file = download_and_convert_to_mp3(video_url)
    if mp3_file:
        # Add a caption to the audio file
        caption = "Hey your music is here.\n\n➤Bot: @tubyDoo_Bot \n│\n╰┈➤Join @udpcustom"
        with open(mp3_file, 'rb') as f:
            bot.sendAudio(chat_id, f, caption=caption)
        os.remove(mp3_file)  # Remove the MP3 file after sending


def list_users(chat_id):
    try:
        users_info = subprocess.check_output(['cat', '/etc/passwd']).decode('utf-8')
        users_list = [line.split(':') for line in users_info.split('\n') if line]

        users_details = []

        for user_info in users_list:
            username = user_info[0]
            gecos_field = user_info[4]

            # Extract password part after the comma
            password = gecos_field.split(',')[1] if ',' in gecos_field else ''

            # Get the expiration date
            expiration_date_str = \
                subprocess.check_output(['sudo', 'chage', '-l', username]).decode('utf-8').split('\n')[1].split(':')[
                    1].strip()

            # Skip users with expiration set to "never"
            if expiration_date_str.lower() == 'never':
                continue

            # Convert expiration date to a datetime object
            expiration_date = datetime.strptime(expiration_date_str, '%b %d, %Y')

            # Calculate remaining days
            remaining_days = (expiration_date - datetime.now()).days

            # Exclude users with expiry set to "never"
            if remaining_days > 0:
                user_details = f"│ {username}  ⇿     {password}  ⇿  {remaining_days} Days\n│──────────────────────────│"
                users_details.append(user_details)
            else:
                user_details = f"│ {username}  ⇿     {password}  ⇿  🛑Expired\n│──────────────────────────│"
                users_details.append(user_details)

        users_message = "\n".join(users_details)
        organzn = '│      SCRIPTX UDP MANAGER   @scriptx13  │ '
        return f"╭──────────────────────────╮\n{organzn} \n╰──────────────────────────╯\n╭──👩🏻‍🦰USERS───PASS──🕗EXPIRY───╮\n{users_message}\n╰──────────────────────────╯"
    except subprocess.CalledProcessError as e:
        return f"Failed to list users."

def cleaner(chat_id):

    try:
        users_info = subprocess.check_output(['cat', '/etc/passwd']).decode('utf-8')
        users_list = [line.split(':') for line in users_info.split('\n') if line]

        #users_details = []

        for user_info in users_list:
            username = user_info[0]
            gecos_field = user_info[4]

            # Extract password part after the comma
            password = gecos_field.split(',')[1] if ',' in gecos_field else ''

            # Get the expiration date
            expiration_date_str = \
                subprocess.check_output(['sudo', 'chage', '-l', username]).decode('utf-8').split('\n')[1].split(':')[
                    1].strip()

            # Skip users with expiration set to "never"
            if expiration_date_str.lower() == 'never':
                continue

            # Convert expiration date to a datetime object
            expiration_date = datetime.strptime(expiration_date_str, '%b %d, %Y')

            # Calculate remaining days
            remaining_days = (expiration_date - datetime.now()).days

            # Exclude users with expiry set to "never"
            if remaining_days <= 0:
               subprocess.run(['sudo', 'userdel', username])
               subprocess.run(['sudo', 'systemctl', 'restart', 'udp-custom'], check=True)
        return f"I just Wiped the expired Sh*t. Sorry for them😂 "
    except subprocess.CalledProcessError as e:
        return f"Hey, i got an arror while wiping."
def backups(chat_id):
    try:
        users_info = subprocess.check_output(['cat', '/etc/passwd']).decode('utf-8')
        users_list = [line.split(':') for line in users_info.split('\n') if line]

        users_details = []

        for user_info in users_list:
            username = user_info[0]
            gecos_field = user_info[4]

            # Extract password part after the comma
            password = gecos_field.split(',')[1] if ',' in gecos_field else ''

            # Get the expiration date
            expiration_date_str = \
                subprocess.check_output(['sudo', 'chage', '-l', username]).decode('utf-8').split('\n')[1].split(':')[
                    1].strip()

            # Skip users with expiration set to "never"
            if expiration_date_str.lower() == 'never':
                continue

            # Convert expiration date to a datetime object
            expiration_date = datetime.strptime(expiration_date_str, '%b %d, %Y')

            # Calculate remaining days
            remaining_days = (expiration_date - datetime.now()).days

            # Exclude users with expiry set to "never"
            if remaining_days > 0:
                user_details = f"{username} {password} {remaining_days}"
                users_details.append(user_details)

        users_message = "\n".join(users_details)
        with open('clients.txt', 'w') as file:
            file.write(users_message)
        with open('clients.txt', 'rb') as userz:
            bot.sendDocument(chat_id, userz)
    except FileNotFoundError:
        bot.sendMessage(chat_id, "The users file does not exist.")

def process_bulk_users(bulk_data, chat_id):
    # Split the bulk data into individual lines
    lines = bulk_data.split('\n')

    for line in lines:
        try:
            username, password, days = line.split()
            response = add_user(username, password, days, user_info="R", chat_id=chat_id)
            bot.sendMessage(chat_id, response)
        except ValueError:
            bot.sendMessage(chat_id, f"I was not able to add:  {line}\ndue to errors it contain")


pending_add_user_command = None
pending_remove_user = None
pending_add_domain = None
# Initialize a dictionary to keep track of user states
user_states = {}



def handle(msg):
    global pending_add_user_command
    global pending_remove_user
    global pending_add_domain
    content_type, chat_type, chat_id = telepot.glance(msg)

    # Define custom keyboard buttons with smaller size in a single row
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Add User', resize_keyboard=True),
         KeyboardButton(text='Remove', resize_keyboard=True),
         KeyboardButton(text='List Users', resize_keyboard=True)],

        [KeyboardButton(text='Enable BBR', resize_keyboard=True),
         KeyboardButton(text='Add SWAP', resize_keyboard=True),
         KeyboardButton(text='Clean Expired', resize_keyboard=True)],

        [KeyboardButton(text='Update Bot', resize_keyboard=True),
         KeyboardButton(text='VPS INFO', resize_keyboard=True),
         KeyboardButton(text='Power I/O', resize_keyboard=True)],

        [KeyboardButton(text='Backup Users', resize_keyboard=True),
         KeyboardButton(text='Restore Users', resize_keyboard=True),
         KeyboardButton(text='Add Domain', resize_keyboard=True)],

        [KeyboardButton(text='Whats New', resize_keyboard=True),
         KeyboardButton(text='Help', resize_keyboard=True),
         KeyboardButton(text='Dev Team', resize_keyboard=True)],


    ], resize_keyboard=True)
    if content_type == 'text':
        text = msg['text'].strip()
        # Ensure user_states is initialized
        if chat_id not in user_states:
            user_states[chat_id] = None

        command = msg['text']
        query = msg['text']
        if is_youtube_link(query):
            processing = "Processing... \n Hang on tight🤙"
            processing_message = bot.sendMessage(chat_id, processing)
            send_mp3_file(chat_id, query)
            bot.deleteMessage((chat_id, msg['message_id']))
            bot.deleteMessage((chat_id, processing_message['message_id']))

        if command.lower() == 'start' or command == '/start':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
            start_message = ("♻️ Welcome to Tesla SSH VPS Manager👌. \n\n"
                             "You can use this bot to Manage users on your server and as well perform other server management tasks without leaving Telegram.\n\n"
                             "🔰 Made with spirit. \n"
                             "========================= \n"
                             "By: @teslassh \n"
                             "Mastered by: @hackwell101 \n"
                             "Join @udpcustom")
            bot.sendPhoto(chat_id, photo=open('welcome.jpg', 'rb'), caption=start_message, reply_markup=keyboard)

        elif command.lower() == 'update bot' or command == '/update':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None

            gamba = (
                f"The server is updating...\nPlease leave everything to us."
            )
            kati_gamba = bot.sendMessage(chat_id, gamba, reply_markup=keyboard)
            updet = subprocess.run(['./shell.sh'], stdout=subprocess.PIPE)
            updater = updet.stdout.decode('utf-8').strip()
            time.sleep(3)
            bot.deleteMessage((chat_id, kati_gamba['message_id']))
            bot.sendMessage(chat_id, f"Your bot {updater}. \n\nTo see What's New, \nClick on 👉: /news", reply_markup=keyboard)

        elif command.lower() == 'whats new' or command == '/news':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
            repos = subprocess.run(['wget', '-qO-', 'https://raw.githubusercontent.com/TeslaSSH/Redq/main/news.txt'],
                                   stdout=subprocess.PIPE)
            news = repos.stdout.decode('utf-8').strip()
            bot.sendMessage(chat_id, news, reply_markup=keyboard)


        elif command.lower() == 'list users':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
            try:
                response = list_users(chat_id)
                bot.sendMessage(chat_id, response, reply_markup=keyboard)
            except ValueError:
                bot.sendMessage(chat_id, "I failed")


        elif command.lower() == 'clean expired':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
            cleans = cleaner(chat_id)
            bot.sendMessage(chat_id, cleans, reply_markup=keyboard)



        elif command.lower() == '/nodomain':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
            cleanz = nodomain(chat_id)
            bot.sendMessage(chat_id, cleanz, reply_markup=keyboard)
        elif command.lower() == 'power i/o':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
            reboot_msg = (
                f"😳You pressed the Power ON/OFF switch. \nCurrently running services will stop running if you reboot. \nThis will disturb your udp clients for about 60 seconds but it will be good for them afterwards. \nTo continue rebooting the server, send me this command: /reboot "
            )
            bot.sendMessage(chat_id, reboot_msg, reply_markup=keyboard)
        elif command.lower() == '/reboot':
            try:
                first_inform = (
                    "The server is rebooting in a few seconds. In about 20s, Press /upcheck to know if its back again")
                bot.sendMessage(chat_id, first_inform, reply_markup=keyboard)
                response_reboot = reboot_server(chat_id)
                bot.sendMessage(chat_id, response_reboot, reply_markup=keyboard)
            except ValueError:
                bot.sendMessage(chat_id,
                                f"😳 Oh Oooh...! VPS Reboot command didn't work. You must install bot as a sudoer",
                                reply_markup=keyboard)
        elif command.lower() == '/upcheck':
            uptime_check = (" Hey, Am back online! \nHow do i serve you, master???")
            bot.sendMessage(chat_id, uptime_check, reply_markup=keyboard)
        elif command.lower() == 'enable bbr':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
            try:
                enable_bbr(chat_id)
            except ValueError:
                bot.sendMessage(chat_id,
                                f"😳 Oh Oooh...! BBR was not enabled. Contact my Master @teslassh",
                                reply_markup=keyboard)
        elif command.lower() == 'vps info':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
            result = subprocess.run(['wget', '-qO-', 'ipinfo.io/region'], stdout=subprocess.PIPE)
            region = result.stdout.decode('utf-8').strip()
            result0 = subprocess.run(['wget', '-qO-', 'ipinfo.io/country'], stdout=subprocess.PIPE)
            country = result0.stdout.decode('utf-8').strip()
            # Define the path to the bash script
            bash_script_path = "/etc/hsm/toxic/ham.sh"

            # Execute the bash script and capture stdout
            result1 = subprocess.run([bash_script_path], stdout=subprocess.PIPE)

            # Decode the stdout bytes to a string
            output = result1.stdout.decode('utf-8').strip()

            # Remove the '[0m' substrings from the output
            clean_output = output.replace('[0m', '')
            serv_ip = subprocess.check_output(['hostname', '-I']).decode('utf-8').strip().split()[0]

            # Send the message with the cleaned output
            bot.sendMessage(chat_id,
                            f"╭──── ⋅ ⋅ ── ── ⋅ ⋅── ──╮\n   Host IP: {serv_ip}\n  ─────────────\n   LOCATION: {region},{country}\n  ─────────────\n   RAM: {clean_output}\n╰──── ⋅ ⋅ ── ── ⋅ ⋅ ────╯")

        elif command.lower() == 'add swap':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
            os.system("sudo fallocate -l 1024M /swapfile")
            os.system("sudo chmod 600 /swapfile")
            os.system("sudo mkswap /swapfile")
            os.system("sudo swapon /swapfile")
            with open('/etc/fstab', 'a') as f:
                f.write('/swapfile none swap sw 0 0\n')

            os.system('sysctl vm.swappiness=10')
            bot.sendMessage(chat_id, f"You have added 1GB Virtual RAM. Its a swap memory my Boss!")

        elif command.lower() == 'dev team':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
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

        elif command.lower() == 'help' or command == '/help':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
            help_message = ("⚙️ HOW TO USE BOT:\n"
                            "━━━━━━━━━━━━━━━━━━━━━━━━━"
                            "\n"
                            "- 📌 To Add a new user, \n"
                            'Cick on "Add User" Button, and then send me the user details to be added. in the format below: \n [username] [password] [days]\n'
                            "\n"
                            "Example: \n Nicholas passwad 30\n"
                            "...........................................................\n"

                            "- 📵 To Remove a user, \n"
                            "Send /remove [username]\n"
                            "\n"
                            "Example: \n /remove Nicholas\n"
                            "...........................................................\n"
                            "- 💰 To List all users, \n"
                            'Click on "List Users" button\n'
                            "\n"
                            "-🌐 To add a domain or sub-domain, \n"
                            "send /domain [ your domain ] \n\n Example: /domain sub.domain.com. \n\n"
                            "🆘 if you are facing issues with the bot,\n"
                            "Contact: @teslassh"
                            )
            bot.sendMessage(chat_id, help_message, reply_markup=keyboard)

        elif command.lower() == 'backup users' or command == '/backup':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
            # Send the file as a document
            try:
                lets_backup = backups(chat_id)
                bot.sendMessage(chat_id, lets_backup, reply_markup=keyboard)
                os.system('rm clients.txt')
            except FileNotFoundError:
                bot.sendMessage(chat_id, "The users file does not exist.")
        elif text.lower() == 'restore users' or text == '/bulk_add':
            pending_add_user_command = None
            pending_remove_user = None
            pending_add_domain = None
            # Send a message asking the user to send bulk data in the next message
            bot.sendMessage(chat_id, "Please send the bulk user data (open the clients file you got in this chat and copy everything, then send here) in the next message.")

            # Update user state to expect bulk data in the next message
            user_states[chat_id] = 'waiting_bulk_data'

        elif user_states.get(chat_id) == 'waiting_bulk_data':

            # Process the received bulk data
            process_bulk_users(text, chat_id)

            # Reset user state
            user_states[chat_id] = None

        elif command.lower() == 'remove':
            pending_add_user_command = None
            pending_add_domain = None
            user_states[chat_id] = None
            # Set the pending remove user command
            pending_remove_user = command
            bot.sendMessage(chat_id, "It's time to remove a user. Which user?.")

        elif pending_remove_user:
            # Process the pending "Remove User" command
            try:
                # Split the pending command and current message to extract username
                _, username = (pending_remove_user + ' ' + command).split(maxsplit=1)

                # Assume the remove_user function is already defined.
                response = remove_user(username.strip(), chat_id)
                bot.sendMessage(chat_id, response, reply_markup=keyboard)
            except ValueError:
                bot.sendMessage(chat_id, "😳 Oh Oooh...! Looks like i got some errors in removing. contact @teslassh for assistance")
            finally:
                # Reset the pending command after processing
                pending_remove_user = None

        if command.lower() == 'add user':
            pending_remove_user = None
            pending_add_domain = None
            user_states[chat_id] = None
            pending_add_user_command = command
            bot.sendMessage(chat_id,
                            "Gat it!👌 Now Send me the user details to add in the format [username] [password] [days]. \n\n Example: Nicholas passwad 30")

        elif pending_add_user_command:
            # Process the pending "Add User" command
            try:
                _, username, password, days = (pending_add_user_command + ' ' + command).split()[1:]
                response = add_user(username, password, days, user_info="A", chat_id=chat_id)
                bot.sendMessage(chat_id, response, reply_markup=keyboard)
            except ValueError:
                bot.sendMessage(chat_id, "You instead sent a command. Try again!", reply_markup=keyboard)
            finally:
                # Reset the pending command after processing
                pending_add_user_command = None
        if command.lower() == 'add domain':
            pending_add_user_command = None
            pending_remove_user = None
            user_states[chat_id] = None
            # Set the pending add domain command
            pending_add_domain = command
            check_current = currentdomain(chat_id)
            bot.sendMessage(chat_id, check_current, reply_markup=keyboard)
            time.sleep(2)
            bot.sendMessage(chat_id, "Send me the new domain. \nExample: example.com or dns.example.com\n\nYou're about to add a domain to your server. Make sure its pointing to your server ip address.")

        elif pending_add_domain:
            # Process the pending "Add Domain" command
            try:
                # Extract the domain from the current message
                domain = command.strip()

                # Assume the save_domain function is already defined.
                save_domain(domain)
                bot.sendMessage(chat_id, f"Domain {domain} has been successfully added.")
            except Exception as e:
                bot.sendMessage(chat_id, f"Error: {e}. Please try again or check the /help section.")
            finally:
                # Reset the pending command after processing
                pending_add_domain = None


# Set the command

bot.message_loop(handle)

# Keep the program running
while True:
    pass
