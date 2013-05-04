#!/bin/bash
# This script will test if you have given a leap year or not.

if grep -q btc-indicator= ~/.bashrc; then
    echo "Already registered in bashrc"
    exit 1
fi
echo " " >> ~/.bashrc
echo "#" >> ~/.bashrc
echo "#     BTC-Indicator" >> ~/.bashrc
echo "#" >> ~/.bashrc
echo "alias btc-indicator='python ~/.local/share/applications/btc-price-indicator.py'" >> ~/.bashrc


