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

   done < /etc/hsm/toxic/seckey.txt
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

restart_bot() {
    #Run the bot
    ban_me
    print_center -ama "RESTARTING THE BOT".....
    sleep 2
    systemctl daemon-reload &>/dev/null
    systemctl restart sshbt &>/dev/null
    echo ""
    sleep 2
    bot_menu

}
run_bot() {
    #Run the bot
    ban_me
    print_center -ama "BOT INITIALISING....."
    sleep 3
    chmod 640 /etc/systemd/system/sshbt.service
    systemctl daemon-reload &>/dev/null
    systemctl enable sshbt &>/dev/null
    systemctl start sshbt &>/dev/null
    systemctl restart sshbt &>/dev/null
    print_pink "Cheers! Your bot is now running."
    echo ""
    sleep 2
    sudo bot

}

stop_bot() {
    #Run the bot
    ban_me
    print_center -ama "STOPPING THE BOT".....
    systemctl stop sshbt
    sleep 2
    print_pink "Your Bot has been stopped"
    sleep 2
    bot_menu

}
ch_token() {
    # Run the bot
    ban_me
    print_center -ama "CHANGE YOUR BOT TOKEN"
    msg -bar3
    sleep 1
    echo ""
    print_blue "Enter new token"
    echo ""
    read -p "NEW TOKEN: " new_token
    sleep 3

    while IFS= read -r line; do
        if [ "$line" == "$new_token" ]; then
            print_yellow "The Bot Token entered already exists"
            bot_menu
        fi
    done < /etc/hsm/toxic/tokenz.txt

    echo "$new_token" > /etc/hsm/toxic/tokenz.txt
    print_pink "A new Bot token has been Saved!"
    bot_menu
}

bot_remove() {
  ban_me
  print_center -ama "Removing. Please wait...."
  sleep 3
  systemctl stop sshbt
  systemctl disable sshbt
  sudo rm -f /etc/hsm/toxic/olwa.py
  sudo rm -f /usr/bin/bot 
  print_pink "Your bot has been Uninstalled Successfully"
  sleep 3
  clear
  exit
}
bot_install() {
    cd
    clear
    #sudo apt update && apt upgrade -y
   # sudo apt-get install screen
    sudo apt install python3-pip
    sudo pip install telepot &>/dev/null
    sudo pip install telepot --upgrade &>/dev/null
    sudo touch tokenz.txt
    sudo touch seckey.txt
   # Download teslbot from git
    teslbot_fetch() {
      wget -O olwa.py https://raw.githubusercontent.com/Lordsniffer22/nkechi_ofombo/main/teslbot.py &&
      sudo mkdir -p /etc/hsm/toxic/ &&
      sudo rm -f /etc/hsm/toxic/olwa.py
      sudo mv olwa.py /etc/hsm/toxic/
   }

    teslbot_fetch &>/dev/null
    sudo mv tokenz.txt /etc/hsm/toxic/
    #creste file command
    sudo rm -f /usr/bin/bot
    wget -O /usr/bin/bot 'https://raw.githubusercontent.com/Lordsniffer22/nkechi_ofombo/main/bot_runner.sh' &>/dev/null
    chmod +x /usr/bin/bot

    clear
    print_center -ama "BOT TOKEN REQUIRED"
    sleep 2
    msg -bar3
    echo ""
    read -p "Enter Token: " btoken
    sleep 2
    print_center -ama "You entered: \e[1;95m$btoken\e[0m"
    sleep 2
    clear

    # save the Bot Token
    echo "$btoken" > /etc/hsm/toxic/tokenz.txt


    # Function to generate a random 12-character key
    generate_key() {
      tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 12
    }

   # generate the key
    secretk=$(generate_key)

   # Store the new key in seckey.txt
    echo "$secretk" > seckey.txt
    sudo mv -f seckey.txt /etc/hsm/toxic/

   # Display a message
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
      sleep 5
    done < /etc/hsm/toxic/seckey.txt
    # Search and remove raw files
    find / -type f -name "ShellBot.sh" 2>/dev/null | while read -r file;
      do
        rm -f "$file"
      done
    
    # [make service file]
    echo '[Unit]
    Description=Made by Teslassh (( ZERO ONE LLC ))
    After=network.target

    [Service]
    User=root
    Type=simple
    ExecStart=/usr/bin/python3 /etc/hsm/toxic/olwa.py 
    WorkingDirectory=/etc/hsm/toxic/
    Restart=always

    [Install]
    WantedBy=multi-user.target' > /etc/systemd/system/sshbt.service

    # Activate the service
    run_bot
}
#bot_installer() {
      # Check if mana.sh exists
    #if [ -f ~/udp/mana.sh ]; then
    #  bot_install
   # else
   #   print_viola "You did not install teslassh udp script on your server."
     # echo ""
    #  print_yellow "Go visit github to install The Script"
     # sleep 4
     # exit
    #fi

#}


ban_me() {
  clear
  print_pink " _____ _____ ____  _        _      ____ ____  _   _ "
  print_pink "|_   _| ____/ ___|| |      / \    / ___/ ___|| | | |"
  print_blue "  | | |  _| \___ \| |     / _ \   \___ \___ \| |_| |"
  print_yellow "  | | | |___ ___) | |___ / ___ \   ___) |__) |  _  |"
  print_pink "  |_| |_____|____/|_____/_/   \_\ |____/____/|_| |_|" 
  echo ""
}
#check system
os_check() {
  if [ -f /etc/os-release ]; then
      . /etc/os-release
      if [[ "$NAME" = "Ubuntu" && "$VERSION_ID" = "22.04" ]]; then
          bot_install
      elif [[ "$NAME" = "Ubuntu" && "$VERSION_ID" = "23.10" ]]; then
          bot_install
      else
          print_pink "THE BOT IS MEANT TO RUN ON UBUNTU 22.04 AND 23.10"
          exit 1
      fi
  fi 
}
install_udp_first() {
    print_center 'After the server reboots, Login amd type "bot"'
    sleep 4
    rm -f install.sh
    wget --no-cache  "https://raw.githubusercontent.com/TeslaSSH/Tesla_UDP_custom-/main/install.sh" -O install.sh
    chmod +x install.sh 
    ./install.sh
}

menu_real() {
    ban_me
    msg -bar
    print_center -ama "BOT MANAGER By TeslaSSH"
    msg -bar0
    echo ""
    # print options menu
    print_center -ama "${a12:-CHOOSE AN OPTION}"
    msg -bar3
    echo " $(msg -verd "[1]") $(msg -verm2 '>') $(msg -ama "${a6:-RESTART BOT ☢️}")"
    echo " $(msg -verd "[2]") $(msg -verm2 '>') $(msg -ama "${a8:-Install UDP BOT }")"
    echo " $(msg -verd "[3]") $(msg -verm2 '>') $(msg -teal "${a11:-SECRET KEY 🔑}")"
    echo " $(msg -verd "[4]") $(msg -verm2 '>') $(msg -ama "${a6:-STOP BOT ⛔}")"
    echo " $(msg -verd "[5]") $(msg -verm2 '>') $(msg -ama "${a6:-CHANGE BOT TOKEN 🔁}")"
    echo " $(msg -verd "[6]") $(msg -verm2 '>') $(msg -ama "${a6:-Uninstall Bot}")"
    exit2home

    # prompt user for option selection
    read -p " ⇢  Enter your selection: " option

    # handle option selection
    case $option in
    1)
      restart_bot
      ;;
    2)
      os_check #checks os and installs bot
      ;;
    3)
      see_key
      ;;
    4)
      stop_bot
      ;;
    5)
      ch_token
      ;;
    6)
      bot_remove
      ;;
    0)
      exit
      ;;
    esac
}

bot_menu() {
  source <(curl -sSL 'https://raw.githubusercontent.com/TeslaSSH/Tesla_UDP_custom-/main/module/module')
  report=$(systemctl is-active udp-custom)
  if [ "$report" == "active" ] || [ -f /etc/hsm/toxic/olwa.py ]; then
      menu_real
  else
      print_pink "IT APPEARS THAT UDP CUSTOM IS NOT INSTALLED YET ON THIS VPS"
      echo ""
      echo " $(msg -verd "[1]") $(msg -verm2 '>') $(msg -ama "${a8:-Install UDP CUSTOM First✳️}")"
      echo " $(msg -verd "[0]") $(msg -verm2 '>') $(msg -ama "${a8:-Exit installer}")"
      echo ""
      read -p " ⇢  Enter your selection: " ansa
      case $ansa in
      1)
        install_udp_first
        ;;
      0)
        exit
        ;;
      esac
   fi   
}

bot_menu



