#!/bin/bash
# Adds btc-indicator command to run the indicator
if grep -q cryptocoin-indicator= ~/.bashrc; then
	exit 1
fi
echo " " >> ~/.bashrc
echo "#" >> ~/.bashrc
echo "#     CryptoCoin-Indicator" >> ~/.bashrc
echo "#" >> ~/.bashrc
echo "alias cryptocoin-indicator='python ~/.local/share/applications/cryptocoin-price-indicator.py'" >> ~/.bashrc
