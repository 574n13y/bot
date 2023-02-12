#!/bin/sh
cd /
sleep 10
cd /home/pi/UdPject/
sudo python3 run.py
sudo python3 Telegram_bot.py
cd /
