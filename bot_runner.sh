#!/bin/bash
#Prepare the environment


see_key() {
    while read -r line; do
      echo "Your Bot secret (Verification) key is: $line "
      echo "You can use it to verify your bot ownership on Telegram!"
      echo " This project is brought to you By TeslaSSH, t.me/teslassh"
done
}
run_bot() {
    #Run the bot
    sudo systemctl daemon-reload
    sudo systemctl enable teslbot
    sudo systemctl start teslbot
    sleep 3
    echo "Cheers! Your bot is now running."

}
bot_install() {
    sudo apt update && apt upgrade -y
    clear
    sudo apt install python3-pip
    sudo pip install telepot
    touch tokenz.txt
    touch seckey.txt
    #download teslbot from git
    wget -O teslbot.py https://raw.githubusercontent.com/Lordsniffer22/nkechi_ofombo/main/teslbot.py
    mkdir -p plugins/telbots/
    sudo mv teslbot.py plugins/telbots/

    #get teslbot service from git
    wget -O teslbot.service https://raw.githubusercontent.com/TeslaSSH/Redq/main/config/teslbot.service
    sudo mv teslbot.service etc/systemd/system/
    print_centre -ama "BOT TOKEN REQUIRED"
    sleep 3
    msg -bar3
    echo ""
    read -p "Enter Token: " btoken
    sleep 2
    print_center -ama "Thanks for entering your Telegram Bot Token"

    # save the Bot Token
    echo "$btoken" > tokenz.txt


    # Function to generate a random 12-character key
    generate_key() {
      tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 12
    }

   # generate the key
    secretk=$(generate_key)

   # Store the new key in seckey.txt
    sed -i '' '1,$d' seckey.txt
    echo "$secretk" > seckey.txt

   # Display a message
    run_bot
    while read -r line; do
      echo "Success! Your bot key: $line has been created successfully."
      echo "Use it to verify bot ownership on Telegram"
    done < seckey.txt
    run_bot
}

bot_menu() {
  source <(curl -sSL 'https://raw.githubusercontent.com/TeslaSSH/Tesla_UDP_custom-/main/module/module')
  clear
  echo ""
  msg -bar
  print_centre -ama "BOT MANAGER By TeslaSSH"
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

while [[ $? -eq 0 ]]; do
  bot_menu
done



