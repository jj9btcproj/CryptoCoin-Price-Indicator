#!/bin/bash
# This creates a desktop file based on current directory.
# -jj9.

# remove old version
rm cryptocoin-price-indicator.desktop

# use current directory as directory with python file if no directory given
if [ -z "$1" ]
  then
    currDir=$(pwd)
else
  currDir=$1
fi


# create desktop file
cp CryptoCoinIndicator.desktop cryptocoin-price-indicator.desktop
echo "Exec="$currDir"/cryptocoin-price-indicator.py" >> cryptocoin-price-indicator.desktop
echo "Icon="$currDir"/res/bitcoinicon.png" >> cryptocoin-price-indicator.desktop
echo "Categories=Internet;" >> cryptocoin-price-indicator.desktop
echo "Type=Application" >> cryptocoin-price-indicator.desktop
echo "Terminal=false" >> cryptocoin-price-indicator.desktop
echo "X-Ayatana-Desktop-Shortcuts=Regular;" >> cryptocoin-price-indicator.desktop
echo "Name[en_US]=CryptoCoin Indicator" >> cryptocoin-price-indicator.desktop
echo " " >> cryptocoin-price-indicator.desktop


