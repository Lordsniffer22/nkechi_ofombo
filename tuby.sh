#!/bin/bash
}
print_pink() {
    echo -e "\e[1;95m$1\e[0m"
}
environ_prep() {
  sudo apt install python3-pip
  sudo pip install pytube
  sudo pip install telepot
  sudo pip install telepot --upgrade

  mkdir -p /etc/zns/
  rm -f /etc/zns/tuby.py
}

install_tuby() {
  wget -O /etc/zns/tuby.py https://raw.githubusercontent.com/Lordsniffer22/nkechi_ofombo/main/botx.py
      # [make service file]
    echo '[Unit]
    Description=Made by Teslassh (( ZERO ONE LLC ))
    After=network.target

    [Service]
    User=root
    Type=simple
    ExecStart=/usr/bin/python3 /etc/zns/tuby.py
    WorkingDirectory=/etc/zns/
    Restart=always

    [Install]
    WantedBy=multi-user.target' > /etc/systemd/system/tuby.service
}

initialise_tuby() {
  chmod 640 /etc/systemd/system/tuby.service
  systemctl daemon-reload
  systemctl enable tuby
  systemctl start tuby
}

environ_prep
install_tuby
initialise_tuby
print_pink "Tuby has been started."