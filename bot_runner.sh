#!/bin/bash
#Prepare the environment
print_blue() {
    echo -e "\e[1;34m$1\e[0m"
}
print_blu() {
    echo -e "\e[34m$1\e[0m"
}
print_yellow() {
    echo -e "\e[1;33m$1\e[0m"
}
print_pink() {
    echo -e "\e[1;95m$1\e[0m"
}
print_viola() {
    echo -e "\e[1;35m$1\e[0m"
}
see_key() {
    ban_me
    msg -bar
    print_center -ama "SERVER KEY Manager"
    msg -bar0
    echo ""
    
  # print options menu
    print_center -ama "${a12:-BOT SECRET KEY}"
    msg -bar3
    gamba="Bot secret:"
    echo ""
    while read -r line; do
      echo -e "\e[1;33m$gamba\e[0m \e[1;95m$line\e[0m"
      echo ""
      print_blu "You can use it to verify your bot ownership on Telegram."
      print_center -ama " Made By TeslaSSH, t.me/teslassh"
      sleep 4

   done < plugins/telbots/seckey.txt
   press_back
}
press_back() {
 echo ""
 read -p "Press Enter to go back" confm
 sleep 1
 case $confm in
   [Yy]* ) bot_menu ;;
   [Nn]* ) bot_menu ;;
   * ) bot_menu ;;
 esac
}

run_bot() {
    #Run the bot
    ban_me
    print_center -ama "RESTARTING THE BOT".....
    sleep 4
    if screen -ls | grep -q "udpbot"; then
      screen -ls | grep udpbot | cut -d. -f1 | awk '{print $1}' | xargs kill
    else
      echo ""
    fi
    sudo pip install telepot --upgrade &>/dev/null
    cd plugins/telbots/
    screen -dmS Tesla_SSH_BOT /usr/bin/python3 teslbot.py
    echo "Cheers! Your bot is now running."
    echo ""
    sleep 4
    bot_menu

}
bot_install() {
    sudo apt update && apt upgrade -y
    sudo apt-get install screen
    clear
    sudo apt install python3-pip
    sudo pip install telepot -y &>/dev/null
    touch tokenz.txt
    touch seckey.txt
   # Download teslbot from git
   teslbot_fetch() {
      wget -O teslbot.py https://raw.githubusercontent.com/Lordsniffer22/nkechi_ofombo/main/teslbot.py &&

   # Create the directory with sudo
      sudo mkdir -p plugins/telbots/ &&

   # Move the teslbot.py to the directory
      sudo rm -f plugins/telbots/teslbot.py
      sudo mv teslbot.py plugins/telbots/

    }
    teslbot_fetch &>/dev/null
    sudo cp tokenz.txt plugins/telbots/
    #creste file command
    wget -O /usr/bin/bot 'https://raw.githubusercontent.com/Lordsniffer22/nkechi_ofombo/main/bot_runner.sh' &>/dev/null
    chmod +x /usr/bin/bot
    
    #get teslbot service from git
    wget -O teslbot.service https://raw.githubusercontent.com/TeslaSSH/Redq/main/config/teslbot.service &>/dev/null
    sudo mv teslbot.service /etc/systemd/system/
    clear
    print_center -ama "BOT TOKEN REQUIRED"
    sleep 2
    msg -bar3
    echo ""
    read -p "Enter Token: " btoken
    sleep 2
    print_center -ama "Thanks for entering your Telegram Bot Token"

    # save the Bot Token
    echo "$btoken" > plugins/telbots/tokenz.txt


    # Function to generate a random 12-character key
    generate_key() {
      tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 12
    }

   # generate the key
    secretk=$(generate_key)

   # Store the new key in seckey.txt
    echo "$secretk" > seckey.txt
    sudo cp -f seckey.txt plugins/telbots/
   # Display a message
    while read -r line; do
      echo -e "Your Bot secret (Verification) key is: \e[1;95m$line\e[0m"
      echo ""
      print_center -ama "You can use it to verify your bot ownership on Telegram!"
      print_center -ama " This project is brought to you By TeslaSSH, t.me/teslassh"
      sleep 10
    done < seckey.txt
    run_bot
}

ban_me() {
  clear
  print_pink " _____ _____ ____  _        _      ____ ____  _   _ "
  print_pink "|_   _| ____/ ___|| |      / \    / ___/ ___|| | | |"
  print_blue "  | | |  _| \___ \| |     / _ \   \___ \___ \| |_| |"
  print_yellow "  | | | |___ ___) | |___ / ___ \   ___) |__) |  _  |"
  print_yellow "  |_| |_____|____/|_____/_/   \_\ |____/____/|_| |_|" 
  echo ""
}

bot_menu() {
  source <(curl -sSL 'https://raw.githubusercontent.com/TeslaSSH/Tesla_UDP_custom-/main/module/module')
  ban_me
  msg -bar
  print_center -ama "BOT MANAGER By TeslaSSH"
  msg -bar0
  echo ""
  # print options menu
  print_center -ama "${a12:-CHOOSE AN OPTION}"
  msg -bar3
  echo " $(msg -verd "[1]") $(msg -verm2 '>') $(msg -ama "${a6:-RESTART BOT ♞}")"
  echo " $(msg -verd "[2]") $(msg -verm2 '>') $(msg -ama "${a8:-INSTALL BOT ✳️}")"
  echo " $(msg -verd "[3]") $(msg -verm2 '>') $(msg -teal "${a11:-SECRET KEY 🔑}")"
  exit2home

  # prompt user for option selection
  read -p " ⇢  Enter your selection: " option

  # handle option selection
  case $option in
  1)
    run_bot
    ;;
  2)
    bot_install
    ;;
  3)
    see_key
    ;;
  0)
    exit
    ;;
  esac
}

bot_menu


