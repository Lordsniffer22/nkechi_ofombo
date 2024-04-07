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
progres() {
comando[0]="$1"
comando[1]="$2"
 (
[[ -e $HOME/fim ]] && rm $HOME/fim
${comando[0]} -y > /dev/null 2>&1
${comando[1]} -y > /dev/null 2>&1
touch $HOME/fim
 ) > /dev/null 2>&1 &
 tput civis
echo -ne "  \033[1;33mWAIT \033[1;37m- \033[1;33m["
while true; do
   for((i=0; i<18; i++)); do
   echo -ne "\033[1;31m#"
   sleep 0.1s
   done
   [[ -e $HOME/fim ]] && rm $HOME/fim && break
   echo -e "\033[1;33m]"
   sleep 1s
   tput cuu1
   tput dl1
   echo -ne "  \033[1;33mWAIT \033[1;37m- \033[1;33m["
done
echo -e "\033[1;33m]\033[1;37m -\033[1;32m OK !\033[1;37m"
tput cnorm
}

#NEGLECTED FUNCTION.
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

restart_bot1() {
    systemctl daemon-reload 
    systemctl restart sshbt
    sleep 3 
}
restart_bot() {
      #Run the bot
    ban_me
    sleep 1
    print_center -ama "Restarting the Bot."
    progres 'restart_bot1'
    echo ""
    print_pink "Bot has been restarted successfully"
    sleep 4
    bot_menu

}

run_bot() {
    #Run the bot
    chmod 640 /etc/systemd/system/sshbt.service
    systemctl daemon-reload 
    systemctl enable sshbt 
    systemctl start sshbt
    echo ""
    sleep 4

}

cease_bot() {
    systemctl stop sshbt
    sleep 4
}
stop_bot() {
  print_center -ama "STOPPING THE BOT..."
  echo ""
  progres 'cease_bot'
  echo ""
  print_pink "Your Bot has been stopped"
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
    systemctl restart sshbt
    bot_menu
}

bot_removo() {
  sudo rm -f /etc/hsm/toxic/olwa.py 
  sudo rm -f /usr/bin/bot
  sleep 3
}
bot_remove() {
    clear
    ban_me
    echo ""
    print_center -ama "Removing. Please wait...."
    progres 'bot_removo'
    msg -bar3
    echo ""
    print_pink "Your bot has been Uninstalled Successfully"
    sudo udp
}
bot_install() {
    cd
    clear
    ban_me
    #sudo apt update && apt upgrade -y
    # sudo apt-get install screen
    prepare_env() {
       sudo apt install python3-pip && sudo pip install telepot && sudo pip install telepot --upgrade &>/dev/null
       sleep 4
    }
    echo ""
    print_center -ama "Preparing Dependancies"
    msg -bar3
    progres 'prepare_env'
    echo ""

   # Download teslbot from git
    teslbot_fetch() {
      sudo mkdir -p /etc/hsm/toxic/
      sudo rm -f /etc/hsm/toxic/olwa.py
      sudo touch /etc/hsm/toxic/tokenz.txt
      sudo touch /etc/hsm/toxic/seckey.txt
      wget -O /etc/hsm/toxic/olwa.py https://raw.githubusercontent.com/Lordsniffer22/nkechi_ofombo/main/teslbot.py
      sleep 4
   }
    print_center -ama "Setting up D-Base"
    msg -bar3
    progres 'teslbot_fetch'
    echo ""

    #creste file command
    sudo rm -f /usr/bin/bot
    wget -O /usr/bin/bot 'https://raw.githubusercontent.com/Lordsniffer22/nkechi_ofombo/main/bot_runner.sh' &>/dev/null
    chmod +x /usr/bin/bot

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    clear 
    ban_me
    print_center -ama "BOT TOKEN REQUIRED"
    sleep 1
    msg -bar3
    echo ""
    read -p "Enter Token: " btoken
    sleep 2
    # save the Bot Token
    echo "$btoken" > /etc/hsm/toxic/tokenz.txt

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # make Ram checker

    make_Ram_cmd() {
      echo '#!/bin/bash
memory=$(neofetch | grep "Memory" | cut -d: -f2 | sed "s/ //g")
echo "$memory"
' > /etc/hsm/toxic/ham.sh

      chmod 777 /etc/hsm/toxic/ham.sh
    }
    make_shell_cmd() {
      echo '#!/bin/bash
      github_file_url="https://raw.githubusercontent.com/Lordsniffer22/nkechi_ofombo/main/teslbot.py"
      local_file_path="/etc/hsm/toxic/olwa.py"

       # Download latest file from github without saving it.
      latest_content=$(wget -O - "$github_file_url" 2>/dev/null)
      #current loko content
      current_content=$(cat "$local_file_path")
       # Compare the two
      if [ "$current_content" != "$latest_content" ]; then
         echo "has been Updated successfully!"\
         rm -f "$local_file_path"
         wget -O "$local_file_path" "$github_file_url" 2>/dev/null
         systemctl restart sshbt
      else
         echo "is already up-to-date."
      fi
      exit' > /etc/hsm/toxic/shell.sh
      chmod 777 /etc/hsm/toxic/shell.sh
    }

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
    make_Ram_cmd
    make_shell_cmd
    clear
    ban_me
    echo ""
    print_center -ama "BOT IS BEING INITIALISED....."
    msg -bar3
    progres 'run_bot'
    echo ""
    print_pink "Cheers! Your bot is now running."
    # Search and remove raw files
    find / -type f -name "ShellBot.sh" 2>/dev/null | while read -r file;
      do
        rm -f "$file"
      done
    sudo bot
}

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
          print_pink "THE BOT IS MEANT TO RUN ON UBUNTU 22.04 AND 23.10 or latest"
          exit 1
      fi
  fi 
} 
install_udp_first() {
    print_center 'Bot installation will begin after this installation process'
    sleep 4
    rm -f install.sh
    wget --no-cache  "https://raw.githubusercontent.com/TeslaSSH/Tesla_UDP_custom-/main/install.sh" -O install.sh
    chmod +x install.sh 
    ./install.sh
    bot_install
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
      echo " $(msg -verd "[2]") $(msg -verm2 '>') $(msg -ama "${a8:-Continue Anyway}")"
      echo " $(msg -verd "[0]") $(msg -verm2 '>') $(msg -ama "${a8:-Exit installer}")"
      echo ""
      read -p " ⇢  Enter your selection: " ansa
      case $ansa in
      1)
        install_udp_first
        ;;
      2)
        bot_install
        ;;
      0)
        exit
        ;;
      esac
   fi   
}

bot_menu



