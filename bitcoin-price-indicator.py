#!/usr/bin/env python

#	Bitcoin-Price-Indicator
#--------------------------------------
#	by jj9 
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
    PING_FREQUENCY = 2 # seconds
    showBTCE = True
    showMtGox = True
    showBlockChain = True
    showBitStamp = True
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
            file.write('True \n')
            file.write('True \n')
            file.close()
        f = open(SETTINGSFILE, 'r')
        lines = f.readlines()
        print "Refresh rate:",int(lines[0]),"seconds"
        self.PING_FREQUENCY = int(lines[0])
        print "Show MtGox:",self.str2bool(lines[1].strip())
        self.showMtGox = self.str2bool(lines[1].strip())
        print "Show BTC-E:",self.str2bool(lines[2].strip())
        self.showBTCE = self.str2bool(lines[2].strip())
        print "Show BlockChain:",self.str2bool(lines[3].strip())
        self.showBlockChain = self.str2bool(lines[3].strip())
        print "Show BitStamp:",self.str2bool(lines[4].strip())
        self.showBitStamp = self.str2bool(lines[4].strip())
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
        togBitStamp = gtk.MenuItem("Show/Hide BitStamp")
        togBitStamp.connect("activate", self.toggleBitStampdisplay)
        togBitStamp.show()
        togBlockChain = gtk.MenuItem("Show/Hide BlockChain")
        togBlockChain.connect("activate", self.toggleBlockChaindisplay)
        togBlockChain.show()
        self.menu.append(togMtGox)
        self.menu.append(togBTCE)
        self.menu.append(togBitStamp)
        self.menu.append(togBlockChain)

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

	# toggle function for BitStamp
    def toggleBitStampdisplay(self, widget):
        if self.showBitStamp:
            self.showBitStamp = False
        else:
            self.showBitStamp = True

	# toggle function for BitStamp
    def toggleBlockChaindisplay(self, widget):
        if self.showBlockChain:
            self.showBlockChain = False
        else:
            self.showBlockChain = True

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
            file.write(str(self.showBlockChain)+'\n')
            file.write(str(self.showBitStamp)+'\n')
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
            priceNow = float(self.getMtGoxData())
            if priceNow == BAD_RETRIEVE:
                priceNow = "TempDown"
            else:
                priceNow = str(priceNow)+"USD"
            dataOut = dataOut + "|MtGox: "+ priceNow
        if self.showBTCE:
            priceNow = float(self.getBTCEBitcoinData())
            if priceNow == BAD_RETRIEVE:
                priceNow = "TempDown"
            else:
                priceNow = str(priceNow)+"USD"
            dataOut = dataOut + "|BTC-E: "+priceNow
        if self.showBitStamp :
            priceNow = float(self.getBitStampBTCPrice())
            if priceNow == BAD_RETRIEVE:
                priceNow = "TempDown"
            else:
                priceNow = str(priceNow)+"USD"
            dataOut = dataOut + "|BitStamp: "+priceNow
        if self.showBlockChain:
            priceNow = float(self.getBlockChainBTCPrice())
            if priceNow == BAD_RETRIEVE:
                priceNow = "TempDown"
            else:
                priceNow = str(priceNow)+"USD"
            dataOut = dataOut + "|BlockChain: "+priceNow
        self.ind.set_label(dataOut)
        return True

	# get mtgox data using JSON
    def getMtGoxData(self):
        lstMtGox = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("http://data.mtgox.com/api/1/BTCUSD/ticker").read()
            data = json.loads(web_page)
            lstMtGox = data['return']['last']['value']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print 'Decoding JSON has failed'
        return lstMtGox

	# get btc-e data using json
    def getBTCEBitcoinData(self):
        lstBTCEprice = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("https://btc-e.com/api/2/btc_usd/ticker").read()
            data = json.loads(web_page)
            lstBTCEprice = data['ticker']['last']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        return lstBTCEprice

	# get BlockChain data using json
    def getBlockChainBTCPrice(self):
        lstBlockChain = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("https://blockchain.info/ticker").read()
            data = json.loads(web_page)
            lstBlockChain = data['USD']['last']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print 'Decoding JSON has failed'

        return float(lstBlockChain)

	# get BitStamp data using json
    def getBitStampBTCPrice(self):
        lstBitStamp = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("https://www.bitstamp.net/api/ticker").read()
            data = json.loads(web_page)
            lstBitStamp = data['last']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print 'Decoding JSON has failed'
        return float(lstBitStamp)

if __name__ == "__main__":
    indicator = BitcoinPriceIndicator()
    indicator.main()
