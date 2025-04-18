#!/bin/bash

echo "[+] Updating system"
sudo apt update && sudo apt upgrade -y

echo "[+] Installing dependencies"
sudo apt install -y git python3 python3-pip wget unzip cron

echo "[+] Installing Go"
wget https://go.dev/dl/go1.21.6.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc

echo "[+] Installing recon tools"
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

echo "[+] Installing Python packages"
pip3 install -r requirements.txt

echo "[+] Creating cron job for daily scan"
(crontab -l 2>/dev/null; echo "0 3 * * * cd $(pwd) && /usr/bin/python3 reconbot.py example.com >> cron.log 2>&1") | crontab -

echo "[+] Setup complete."
