rm bitcoin-price-indicator.desktop
echo "[Desktop Entry]" >> bitcoin-price-indicator.desktop
echo "Encoding=UTF-8 " >> bitcoin-price-indicator.desktop
echo "Version=1.0" >> bitcoin-price-indicator.desktop
echo "Name=Bitcoin Market Price Indicator" >> bitcoin-price-indicator.desktop
echo "Comment=Market price Indicator for Bitcoin" >> bitcoin-price-indicator.desktop
echo "Exec=python /home/$(logname)/.local/share/applications/btc-price-indicator.py" >> bitcoin-price-indicator.desktop
echo "Icon=/home/$(logname)/.local/share/applications/bitcoinicon.png" >> bitcoin-price-indicator.desktop
echo "Categories=GNOME;Application;Network;" >> bitcoin-price-indicator.desktop
echo "Type=Application" >> bitcoin-price-indicator.desktop
echo "Terminal=false" >> bitcoin-price-indicator.desktop
echo "X-Ayatana-Desktop-Shortcuts=Regular;" >> bitcoin-price-indicator.desktop
echo "Name[en_US]=Bitcoin Market Price Indicator" >> bitcoin-price-indicator.desktop
