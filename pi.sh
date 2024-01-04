#!/bin/bash
cd
mkdir -p /var/www/html/
sudo apt-get install php
sudo apt-get install apache2
wget -O file.php https://raw.githubusercontent.com/Lordsniffer22/nkechi_ofombo/main/file.php
mv file.php /var/www/html/
php /var/www/html/file.php
