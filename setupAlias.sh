#!/bin/bash
# Adds cryptocoin-indicator command to run the indicator
# use current directory as directory with python file if no directory given
if [ -z "$1" ]
  then
    currDir=$(pwd)
	currFile=""$currFile"/cryptocoin-price-indicator.py"
else
  currFile=$1
fi

if grep -q cryptocoin-indicator= ~/.bashrc; then
	exit 1
fi
echo " " >> ~/.bashrc
echo "#" >> ~/.bashrc
echo "#     CryptoCoin-Indicator" >> ~/.bashrc
echo "#" >> ~/.bashrc
echo "alias cryptocoin-indicator='python "$currFile"'" >> ~/.bashrc
