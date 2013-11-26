#!/bin/bash
# Adds btc-indicator command to run the indicator
if grep -q btc-indicator= ~/.bashrc; then
	exit 1
fi
echo " " >> ~/.bashrc
echo "#" >> ~/.bashrc
echo "#     BTC-Indicator" >> ~/.bashrc
echo "#" >> ~/.bashrc
echo "alias btc-indicator='python ~/.local/share/applications/btc-price-indicator.py'" >> ~/.bashrc
eval $(source /home/kieth/.bashrc)