#!/bin/bash
#Prepare the environment
print_blue() {
    echo -e "\e[1;34m$1\e[0m"
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
    while read -r line; do
      echo -e "Your Bot secret (Verification) key is: \e[1;95m$line\e[0m"
      echo ""
      print_blue "You can use it to verify your bot ownership on Telegram!"
      print_center -ama " This project is brought to you By TeslaSSH, t.me/teslassh"
      sleep 10
   done < plugins/telbots/seckey.txt
}
run_bot() {
    #Run the bot
    sudo pip install telepot --upgrade &>/dev/null
    cd plugins/telbots/
    screen -dmS Tesla_SSH_BOT /usr/bin/python3 teslbot.py
    sleep 3
    echo "Cheers! Your bot is now running."
    sleep 10

}
bot_install() {
    sudo apt update && apt upgrade -y
    sudo apt-get install screen
    clear
    sudo apt install python3-pip
    sudo pip install telepot &>/dev/null
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

bot_menu() {
  source <(curl -sSL 'https://raw.githubusercontent.com/TeslaSSH/Tesla_UDP_custom-/main/module/module')
  clear
  echo ""
  msg -bar
  print_center -ama "BOT MANAGER By TeslaSSH"
  msg -bar0
  echo ""
  # print options menu
  print_center -ama "${a12:-CHOOSE AN OPTION}"
  msg -bar3
  echo " $(msg -verd "[1]") $(msg -verm2 '>') $(msg -teal "${a6:-RESTART BOT♞}")"
  echo " $(msg -verd "[2]") $(msg -verm2 '>') $(msg -ama "${a8:-INSTALL BOT}")"
  echo " $(msg -verd "[3]") $(msg -verm2 '>') $(msg -teal "${a11:-SECRET KEY⚡}")"
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


