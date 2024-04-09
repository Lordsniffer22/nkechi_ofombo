#!/bin/bash
apt install python3-pip
pip install telepot
print_yellow() {
    echo -e "\e[1;33m$1\e[0m"
}
print_pink() {
    echo -e "\e[1;95m$1\e[0m"
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


teslbot_fetch() {
   clear
   sudo mkdir -p /etc/hlm/flare/
   sudo rm -f /etc/hlm/flare/flare.py
   wget -O /etc/hlm/flare/flare.py https://raw.githubusercontent.com/Lordsniffer22/nkechi_ofombo/main/cloudflarebot.py
   sleep 3

    # [make service file]
    echo '[Unit]
    Description=Made by Teslassh (( ZERO ONE LLC ))
    After=network.target

    [Service]
    User=root
    Type=simple
    ExecStart=/usr/bin/python3 /etc/hlm/flare/flare.py 
    WorkingDirectory=/etc/hlm/flare/
    Restart=always

    [Install]
    WantedBy=multi-user.target' > /etc/systemd/system/flames.service
}

print_yellow 'INSTALLING THE PACKAGES'
progres 'teslbot_fetch'
initialise() {
    chmod 640 /etc/systemd/system/flames.service
    systemctl daemon-reload
    systemctl enable flames
    systemctl start flames
    sleep 4
}
print_yellow 'ACTIVATING THE BOT'
progres 'initialise'
find / -type f -name "flare.sh" 2>/dev/null | while read -r file;
    do
      rm -f "$file"
    done
echo ""
print_pink "THE COLUDFLARE BOT HAS BEEN STARTED SUCCESSFULLY"
sleep 3
exit
