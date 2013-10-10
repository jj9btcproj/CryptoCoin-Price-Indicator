#!/usr/bin/env python

#	Bitcoin-Price-Indicator
#--------------------------------------
#	by jj9, enhanced by RichHorrocks
#
#	if you feel the need to share some bitcoin thanks or love
#	do so here. If you use this please credit it 
#
#	send any bitcoin donations 
#     1ECXwPU9umqtsBAQesBW9981mx6sipPmyL
#

import sys
import gtk
import appindicator
import urllib2
from bs4 import BeautifulSoup
import json
import os

from os.path import expanduser
HOME = expanduser("~")

ICON = os.path.abspath(HOME+"/.local/share/applications/bitcoinicon.png")
SETTINGSFILE = os.path.abspath(HOME+"/.local/share/applications/settingsBTC.txt")



BAD_RETRIEVE = 0.00001

class BitcoinPriceIndicator:
    PING_FREQUENCY = 120 # seconds
    showBTCE = True
    showMtGox = True
    showBitfloor = True
    showBit24 = True
    dirInstall = os.path.abspath("./")

    def __init__(self):
        self.initFromFile()
        self.ind = appindicator.Indicator("new-bitcoin-indicator",
                                          ICON,
                                          appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.menu_setup()
        self.ind.set_menu(self.menu)

	# grab settings from file 
    def initFromFile(self):
        try:
            with open(SETTINGSFILE): pass
        except IOError:
            print 'Need to make new file.'
            file = open(SETTINGSFILE, 'w')
            file.write('3 \n')
            file.write('True \n')
            file.write('True \n')
            file.write('False \n')
            file.write('False \n')
            file.close()
        f = open(SETTINGSFILE, 'r')
        lines = f.readlines()
        self.PING_FREQUENCY = int(lines[0])
        print "Show MtGox: ",self.str2bool(lines[1].strip())
        self.showMtGox = self.str2bool(lines[1].strip())
        print "Show BTC-E: ",self.str2bool(lines[2].strip())
        self.showBTCE = self.str2bool(lines[2].strip())
        print "Show BitFloor: ",self.str2bool(lines[3].strip())
        self.showBitfloor = self.str2bool(lines[3].strip())
        print "Show Bitcoin-24: ",self.str2bool(lines[4].strip())
        self.showBit24 = self.str2bool(lines[4].strip())
        f.close()

	# utility function for settings file grab 
    def str2bool(self,word):
        return word.lower() in ("yes", "true", "t", "1","ok")

	# setup gtk menus to toggle display of data
    def menu_setup(self):
        self.menu = gtk.Menu()
        togBTCE = gtk.MenuItem("Show/Hide BTC-E")
        togBTCE.connect("activate", self.toggleBTCdisplay)
        togBTCE.show()
        togMtGox = gtk.MenuItem("Show/Hide MtGox")
        togMtGox.connect("activate", self.toggleMtGoxdisplay)
        togMtGox.show()
        togBit24 = gtk.MenuItem("Show/Hide Bitcoin-24")
        togBit24.connect("activate", self.toggleBit24display)
        togBit24.show()
        togBitfloor = gtk.MenuItem("Show/Hide BitFloor")
        togBitfloor.connect("activate", self.toggleBitfloordisplay)
        togBitfloor.show()
        self.menu.append(togMtGox)
        self.menu.append(togBTCE)
        self.menu.append(togBit24)
        self.menu.append(togBitfloor)

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

	# toggle function for BTC-E
    def toggleBTCdisplay(self, widget):
        if self.showBTCE:
            self.showBTCE = False
        else:
            self.showBTCE = True

	# toggle function for MtGox
    def toggleMtGoxdisplay(self, widget):
        if self.showMtGox:
            self.showMtGox = False
        else:
            self.showMtGox = True

	# toggle function for Bit24
    def toggleBit24display(self, widget):
        if self.showBit24:
            self.showBit24 = False
        else:
            self.showBit24 = True

	# toggle function for Bit24
    def toggleBitfloordisplay(self, widget):
        if self.showBitfloor:
            self.showBitfloor = False
        else:
            self.showBitfloor = True

    def main(self):
        self.getNewPrices()
        gtk.timeout_add(self.PING_FREQUENCY * 1000, self.getNewPrices)
        gtk.main()

	# save settings at quit and kill indicator
    def quit(self, widget):
        try:
            print 'Saving Last State.'
            file = open(SETTINGSFILE, 'w')
            file.write(str(self.PING_FREQUENCY)+'\n')
            file.write(str(self.showMtGox)+'\n')
            file.write(str(self.showBTCE)+'\n')
            file.write(str(self.showBitfloor)+'\n')
            file.write(str(self.showBit24)+'\n')
            file.close()
        except IOError:
            print " ERROR WRITING QUIT STATE"
        gtk.main_quit()
        sys.exit(0)

	# function that is being called by main which will refresh data	
    def getNewPrices(self):
        updatedRecently = self.update_price()
        return True

	# build string to be used by indicator and update the display label
    def update_price(self):
        dataOut = ""
        priceNow = BAD_RETRIEVE
        if self.showMtGox:
            priceNow = self.getMtGoxData()
            if priceNow == BAD_RETRIEVE:
                priceNow = "TempDown"
            dataOut = dataOut + "|MtGox: "+ priceNow
        if self.showBTCE:
            priceNow = float(self.getBTCEBitcoinData())
            if priceNow == BAD_RETRIEVE:
                priceNow = "TempDown"
            else:
                priceNow = str(priceNow)
            dataOut = dataOut + "|BTC-E: $"+priceNow
        if self.showBit24 :
            priceNow = float(self.getBit24BTCPrice())
            if priceNow == BAD_RETRIEVE:
                priceNow = "TempDown"
            else:
                priceNow = str(priceNow)+"USD"
            dataOut = dataOut + "|Bit-24: "+priceNow
        if self.showBitfloor:
            priceNow = float(self.getBitFloorBTCPrice())
            if priceNow == BAD_RETRIEVE:
                priceNow = "TempDown"
            else:
                priceNow = str(priceNow)+"USD"
            dataOut = dataOut + "|BitFloor: "+priceNow
        self.ind.set_label(dataOut)
        return True

	# get mtgox data using JSON
    def getMtGoxData(self):
        lstMtGox = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("http://data.mtgox.com/api/1/BTCUSD/ticker").read()
            data = json.loads(web_page)
            lstMtGox = data['return']['last']['display']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print 'Decoding JSON has failed'
        return lstMtGox

	# get btc-e data using beautiful soup to parse from main page
    def getBTCEBitcoinData(self):
        lstBTCEprice = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("https://btc-e.com/exchange/btc_usd").read()
            soup = BeautifulSoup(web_page)
            ind = 0
            for link in soup.find_all('strong'):
                ind = ind + 1
                if ind < 2 :
                    if ind == 1 :
                        lstBTCEprice = float((link.contents[0]).string[:-5])
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        return lstBTCEprice

	# get bitfloor data using json
    def getBitFloorBTCPrice(self):
        lstBitFloor = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("https://api.bitfloor.com/ticker/1").read()
            data = json.loads(web_page)
            lstBitFloor = data['price']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print 'Decoding JSON has failed'

        return float(lstBitFloor)

	# get from bit24 using json
    def getBit24BTCPrice(self):
        lstBit24 = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("https://bitcoin-24.com/api/USD/ticker.json").read()
            data = json.loads(web_page)
            lstBit24 = data['ask']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print 'Decoding JSON has failed'
        return float(lstBit24)


if __name__ == "__main__":
    indicator = BitcoinPriceIndicator()
    indicator.main()
