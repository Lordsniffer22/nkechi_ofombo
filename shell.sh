#!/bin/bash
github_file_url="https://raw.githubusercontent.com/Lordsniffer22/nkechi_ofombo/main/teslbot.py"
local_file_path="/etc/hsm/toxic/olwa.py"

# Download latest file from github without saving it.
latest_content=$(wget -O - "$github_file_url")
#current loko content
current_content=$(cat "$local_file_path")
# Compare the two
if [ "$current_content" != "$latest_content" ]; then
   echo "has been Updated successfully!"
   systemctl stop sshbt
   rm -f "$local_file_path"
   wget -O "$local_file_path" "$github_file_url" $>/dev/null
   systemctl start sshbt
else
   echo "is already up-to-date."
fi
exit