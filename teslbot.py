# Made with love by Teslassh
# Stealing this source code is illegal as always.
# #You are allowed to use the tool in any way you wish
import telepot
import subprocess
import os
#import json
from datetime import datetime, timedelta
import time
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

with open('tokenz.txt', 'r') as file:
    bot_token = file.read().strip()
bot = telepot.Bot(bot_token)
# File path to store the secret key
#seckey_file_path = 'seckey.txt'
domain_file_path = 'pydomain.txt'


def save_domain(domain):
    with open(domain_file_path, 'w') as domain_file:
        domain_file.write(domain)

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
    #if not is_verified(chat_id):
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
        subprocess.run(['sudo', 'useradd', '-M', '-s', '/bin/false', '-e', expiration_date_str, '-K', f'PASS_MAX_DAYS={days}', '-p', passs, '-c', f'{user_info},{password}', username], check=True)

        # Get server IP address or saved domain
        server_info = get_domain() or subprocess.check_output(['hostname', '-I']).decode('utf-8').strip()

        # Send success message with details
        success_message = f" {username} has been added successfully!\n\nServer Details:\n{server_info}:1-65535@{username}:{password}"
        return success_message
    except subprocess.CalledProcessError as e:
        return f"Failed to add user {username}. Error: {e}"

def remove_user(username, chat_id):
    try:
        subprocess.run(['sudo', 'userdel', '--force', username], check=True)
        return f"{username} Has been removed successfully!"
    except subprocess.CalledProcessError as e:
        return f"Failed to remove user {username}. Error: {e}"
def restart_udp_daemon(chat_id):

    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'udp-custom'], check=True)
        return f"\n Who else? 😳"
    except subprocess.CalledProcessError as e:
        return f"Failed to restart daemons. Error: {e}"
def reboot_server(chat_id):
    try:
        subprocess.run(['reboot'], check=True)
    except subprocess.CalledProcessError as e:
        return f"Failed to reboot server. Error: {e}"
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
                user_details = f"│ {username}  ⇿     {password}  ⇿  Expired\n│──────────────────────────│"
                users_details.append(user_details)

        users_message = "\n".join(users_details)
        organzn =  '│       ZERO ONE COMPUTING   @scriptx13  │ '
        return f"╭──────────────────────────╮\n{organzn} \n╰──────────────────────────╯\n╭──👩🏻‍🦰USERS───PASS──🕗EXPIRY───╮\n{users_message}\n╰──────────────────────────╯"
    except subprocess.CalledProcessError as e:
        return f"Failed to list users. Error: {e}"


pending_add_user_command = None
def handle(msg):
    global pending_add_user_command
    content_type, chat_type, chat_id = telepot.glance(msg)

    # Define custom keyboard buttons with smaller size in a single row
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Add User', resize_keyboard=True),
         KeyboardButton(text='Remove User', resize_keyboard=True),
         KeyboardButton(text='List Users', resize_keyboard=True)],
        [KeyboardButton(text='Enable BBR', resize_keyboard=True),
         KeyboardButton(text='Add RAM', resize_keyboard=True),
         KeyboardButton(text='Power I/O', resize_keyboard=True)],

        [KeyboardButton(text='Region', resize_keyboard=True),
         KeyboardButton(text='Help', resize_keyboard=True),
         KeyboardButton(text='Dev Team', resize_keyboard=True)],

    ], resize_keyboard=True)

    if content_type == 'text':
        command = msg['text']

        if command.lower() == 'start' or command == '/start':
            start_message = ("♻️ WELCOME TO TESLA SSH BOT👌. \n"
                             "━━━━━━━━━━━━━━━━━━━━━━━━━ \n"
                             "\n"
                             "You can use me to manage users on your server!\n"
                             "\n"
                             "To reload the bot, Press /start\n"
                             "To see the usage guide, Press /help\n"
                             "To add user, Press the add user button \n"
                             "To remove user, Send /remove \n"
                             "To list users, Press /users \n"
                             "\n"
                             "🔰 Made with spirit. \n"
                             "========================= \n"
                             "By: @TESLASSH \n"
                             "Mastered by: @hackwell101 \n"
                             "Join @udpcustom")

            # Send the start message with the custom keyboard

            bot.sendMessage(chat_id, start_message, reply_markup=keyboard)

        elif command.lower() == '/update':
            updet=subprocess.run(['./shell.sh'], stdout=subprocess.PIPE)
            updater=updet.stdout.decode('utf-8').strip()
            bot.sendMessage(chat_id, f"Your bot {updater}")
        elif command.lower() == 'power i/o':
            reboot_msg = (
                f"😳You pressed the Power ON/OFF switch. \nCurrently running services will stop running if you reboot. \nThis will disturb your udp clients for about 60 seconds but it will be good for them afterwards. \nTo continue rebooting the server, send me this command: /reboot "
            )
            bot.sendMessage(chat_id, reboot_msg, reply_markup=keyboard)
        elif command.lower() == '/reboot':
            try:
                response_reboot = reboot_server(chat_id)
                bot.sendMessage(chat_id, response_reboot, reply_markup=keyboard)
            except ValueError:
                bot.sendMessage(chat_id,
                                f"😳 Oh Oooh...! VPS Reboot command didn't work. You must install bot as a sudoer",
                                reply_markup=keyboard)
        elif command.lower() == 'enable bbr':
            try:
                enable_bbr(chat_id)
            except ValueError:
                bot.sendMessage(chat_id,
                                f"😳 Oh Oooh...! BBR was not enabled. Contact my Master @teslassh",
                                reply_markup=keyboard)
        elif command.lower() =='region':
            result = subprocess.run(['wget', '-qO-', 'ipinfo.io/region'], stdout=subprocess.PIPE)
            region = result.stdout.decode('utf-8').strip()
            # Define the path to the bash script
            #bash_script_path = "/etc/hsm/toxic/ham.sh"
            command = ["neofetch", "|", "grep", "\"Memory\"", "|", "cut", "-d:", "-f2", "|", "sed", "'s/ //g'"]

            # Execute the bash script and capture stdout
            result1 = subprocess.run(command, stdout=subprocess.PIPE)

            # Decode the stdout bytes to a string
            output = result1.stdout.decode('utf-8').strip()
            bot.sendMessage(chat_id, f"╭──── ⋅ ⋅ ── ── ⋅ ⋅── ──╮\n   LOCATION: {region}\n  ─────────────\n   USAGE: {output}\n╰──── ⋅ ⋅ ── ── ⋅ ⋅ ────╯")


        elif command.lower() == 'add ram':
            os.system("sudo fallocate -l 1024M /swapfile")
            os.system("sudo chmod 600 /swapfile")
            os.system("sudo mkswap /swapfile")
            os.system("sudo swapon /swapfile")
            with open('/etc/fstab', 'a') as f:
                f.write('/swapfile none swap sw 0 0\n')

            os.system('sysctl vm.swappiness=10')
            bot.sendMessage(chat_id, f"You have added 1GB Virtual RAM. Its a swap memory my Boss!")

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

        elif command.lower() == 'help' or command == '/help':
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

        elif command.lower() == 'verify':
            # Prompt user to enter the secret key for verification
            bot.sendMessage(chat_id, "Please enter the secret key🔑 for verification. \n Get it from the Bot manager on your server. \n\n SSH into your server and type: 👉 bot , \n and then press enter")
         #   verified_users[chat_id] = False

        elif command.lower().startswith('/verify'):
            try:
                _, secret_key = command.split()
           #     response = verify_user(chat_id, secret_key)
          #      bot.sendMessage(chat_id, response, reply_markup=keyboard)
            except ValueError:
                bot.sendMessage(chat_id, "😳 Oh Oooh...! You entered it wrongly. \n\n ✳️ To verify, Use this format: \n \n👉   /verify XXXXXXXXXXX \n \n Where XXXXXXXXXX is your SECRET KEY you got from your VPS server 💻", reply_markup=keyboard)


        if command.lower().startswith('/domain'):

            try:

                _, domain = command.split(maxsplit=1)

                save_domain(domain)

                bot.sendMessage(chat_id, f"Domain '{domain}' saved successfully!")

            except ValueError:

                bot.sendMessage(chat_id, "😳 Oh Oooh...! You entered it wrongly. \n\n Try:  /domain [your_domain]")

        if command.lower() == 'add user':
                pending_add_user_command = command
                bot.sendMessage(chat_id, "Gat it!👌 Now Send me the user details to add in the format [username] [password] [days]. \n\n Example: Nicholas passwad 30", reply_markup=keyboard)

        elif pending_add_user_command:
            # Process the pending "Add User" command
            try:
                _, username, password, days = (pending_add_user_command + ' ' + command).split()[1:]
                response = add_user(username, password, days, user_info="bot", chat_id=chat_id)
                bot.sendMessage(chat_id, response, reply_markup=keyboard)
            except ValueError:
                bot.sendMessage(chat_id, "😳 Oh Oooh...! Something went wrong Try checking the /help section.", reply_markup=keyboard)
            finally:
                # Reset the pending command after processing
                pending_add_user_command = None

        elif command.lower() == 'remove user':
            # Check if the user is verified before allowing to use /remove command
           # if not is_verified(chat_id):
            #    bot.sendMessage(chat_id, "🔐 You need to verify yourself first in order to be a super user! Pass your secret key to the  /verify command.")
          #  else:
                bot.sendMessage(chat_id, "To remove a user, send:\n  /remove [username] \n\n Example:\n /remove Nicolas \n", reply_markup=keyboard)

        elif command.lower().startswith('/remove'):
            # Check if the user is verified before allowing to use /remove command
           # if not is_verified(chat_id):
            #    bot.sendMessage(chat_id, "🔐 You need to verify yourself first in order to be a super user! \n\n Pass your secret key to the  /verify command.")
           # else:
                try:
                    _, username = command.split()
                    response = remove_user(username, chat_id)
                    bot.sendMessage(chat_id, response, reply_markup=keyboard)
                    # Restart the UDP daemon immediately after removing the user
                    response_restart = restart_udp_daemon(chat_id)
                    bot.sendMessage(chat_id, response_restart, reply_markup=keyboard)
                except ValueError:
                    bot.sendMessage(chat_id, "😳 Oh Oooh...! You entered it wrongly. \n\n Try:  /remove [username] \n\n Example:\n /remove Nicolas \n", reply_markup=keyboard)

        elif command.lower() == 'list users' or command == '/users':
            response = list_users(chat_id)
            bot.sendMessage(chat_id, response, reply_markup=keyboard)

# Set the command handler
bot.message_loop(handle)

# Keep the program running
while True:
    pass
