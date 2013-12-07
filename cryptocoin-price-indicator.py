#!/usr/bin/env python

#	CryptoCoin-Price-Indicator
#--------------------------------------
#	by jj9,
#
# 	generalizes and combines old btc version enhanced by RichHorrocks and Zapsoda (btcapicalls/setupfile maintainance for old btc version)  and ltc version
#
#	if you feel the need to share some bitcoin thanks or love
#	do so here. If you use this please credit it 
#
#	send any  donations
#   BTC : 1ECXwPU9umqtsBAQesBW9981mx6sipPmyL
#   LTC : LUJz8yaS4uL1zrzwARbA4CiMpAwbpUwWY6
#   NMC : N1SKXkrcyhxVYwQGsbLTFMbGAgeqL2g9tZ

import sys
import gtk
import appindicator
import urllib2
import json
import os

from os.path import expanduser
HOME = expanduser("~")


SETTINGSFILE = os.path.abspath(HOME+"/.local/share/applications/settingsCryptoIndicator.dat")
BAD_RETRIEVE = 0.00001

class CryptoCoinPriceIndicator:
    PING_FREQUENCY = 1 # seconds
    BTCICON = os.path.abspath(HOME+"/.local/share/applications/bitcoinicon.png")
    LTCICON = os.path.abspath(HOME+"/.local/share/applications/litecoinicon.png")
    NMCICON = os.path.abspath(HOME+"/.local/share/applications/nmcicon.png")
    APPDIR = HOME+"/.local/share/applications/"
    APPNAME = 'CryptoCoin Indicator';VERSION = '0.5'
    BTCMODE = True; BTCInit = False;
    LTCMODE = True; LTCInit = False;
    NMCMODE = True; NMCInit = False;

    def __init__(self):
        self.initFromFile()
        self.ind = appindicator.Indicator("new-bitcoin-indicator", self.BTCICON,appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.menu_setup()
        self.ind.set_menu(self.menu)

    def main(self):
        self.updateIndicators()
        if self.BTCMODE:
            gtk.timeout_add(self.PING_FREQUENCY * 1000, self.getNewPricesBTC)
        if self.LTCMODE:
            gtk.timeout_add(self.PING_FREQUENCY * 1000, self.getNewPricesLTC)
        if self.NMCMODE:
            gtk.timeout_add(self.PING_FREQUENCY * 1000, self.getNewPricesNMC)
        gtk.main()

    def updateIndicators(self):
        if self.BTCMODE:
            self.updateBTCIndicator()
        if self.LTCMODE:
            self.updateLTCIndicator()
        if self.NMCMODE:
            self.updateNMCIndicator()

    def updateBTCIndicator(self):
        self.getNewPricesBTC()
    def updateLTCIndicator(self):
        self.getNewPricesLTC()
    def updateNMCIndicator(self):
        self.getNewPricesNMC()

    def initLTCAddOn(self,widget):
        if (not self.LTCInit) or (widget is None):
            self.indLTC = appindicator.Indicator("new-litecoin-indicator", self.LTCICON, appindicator.CATEGORY_APPLICATION_STATUS)
            self.indLTC.set_status(appindicator.STATUS_ACTIVE)
            self.menu_setupLTC()
            self.indLTC.set_menu(self.menuLTC)
            if (not self.LTCMODE) and (widget is not None):
                self.LTCMODE = True
                gtk.timeout_add(self.PING_FREQUENCY * 1000, self.getNewPricesLTC)
            print "LTC Mode now On"
        else:
            self.noLTC(widget)
        self.getNewPricesLTC()
    def initNMCAddOn(self,widget):
        if (not self.NMCInit) or (widget is None):
            self.indNMC = appindicator.Indicator("new-nmccoin-indicator", self.NMCICON, appindicator.CATEGORY_APPLICATION_STATUS)
            self.indNMC.set_status(appindicator.STATUS_ACTIVE)
            self.menu_setupNMC()
            self.indNMC.set_menu(self.menuNMC)
            if (not self.NMCMODE) and (widget is not None):
                self.NMCMODE = True
                gtk.timeout_add(self.PING_FREQUENCY * 1000, self.getNewPricesNMC)
            print "NMC Mode now On"
        else:
            self.noNMC(widget)
        self.getNewPricesNMC()
	# setup gtk menus to toggle display of data
    def menu_setup(self):
        self.menu = gtk.Menu()
        self.BTCtickers = None
        self.btceBTC = gtk.RadioMenuItem(self.BTCtickers,"BTC-E"); self.btceBTC.connect("activate", lambda x: self.toggleBTCdisplay("btce")); self.btceBTC.show()
        self.BTCtickers = self.btceBTC
        self.mtgoxBTC = gtk.RadioMenuItem(self.BTCtickers,"MtGox"); self.mtgoxBTC.connect("activate", lambda x: self.toggleBTCdisplay("mtgox")); self.mtgoxBTC.show()
        self.BTCtickers = self.mtgoxBTC
        self.bitstampBTC = gtk.RadioMenuItem(self.BTCtickers,"BitStamp"); self.bitstampBTC.connect("activate", lambda x: self.toggleBTCdisplay("bitstamp")); self.bitstampBTC.show()
        self.BTCtickers = self.bitstampBTC
        self.blockchainBTC = gtk.RadioMenuItem(self.BTCtickers,"BlockChain"); self.blockchainBTC.connect("activate", lambda x: self.toggleBTCdisplay("blockchain")); self.blockchainBTC.show()
        self.BTCtickers = self.blockchainBTC

        self.defSet = gtk.MenuItem("Choose exchange : "); self.defSet.show()
        self.menu.append(self.defSet)
        self.menu.append(self.mtgoxBTC); self.menu.append(self.btceBTC)
        self.menu.append(self.bitstampBTC); self.menu.append(self.blockchainBTC)

        self.setRefreshMenu(self.menu)

        self.ltcAdd = gtk.CheckMenuItem("LTC Price"); self.ltcAdd.connect("activate", self.initLTCAddOn);
        if self.LTCMODE:
            self.ltcAdd.activate();
        self.ltcAdd.show();self.menu.append(self.ltcAdd)

        self.nmcAdd = gtk.CheckMenuItem("NMC Price"); self.nmcAdd.connect("activate", self.initNMCAddOn);
        if self.NMCMODE:
            self.nmcAdd.activate();
        self.nmcAdd.show();self.menu.append(self.nmcAdd)

        self.about = gtk.MenuItem("About"); self.about.connect("activate",self.menu_about_response);self.about.show()
        self.menu.append(self.about)
        self.quit_item = gtk.MenuItem("Quit Indicator"); self.quit_item.connect("activate", self.quit); self.quit_item.show()
        self.menu.append(self.quit_item)
        self.getNewPricesBTC()

    def menu_setupLTC(self):
        self.menuLTC = gtk.Menu()
        self.LTCtickers = None
        self.btceLTC = gtk.RadioMenuItem(self.LTCtickers,"BTC-E"); self.btceLTC.connect("activate", lambda x: self.toggleLTCdisplay("btce")); self.btceLTC.show()
        self.LTCtickers = self.btceLTC
        #self.mtgoxLTC = gtk.RadioMenuItem(self.LTCtickers,"MtGox"); self.mtgoxLTC.connect("activate", lambda x: self.toggleLTCdisplay("mtgox")); self.mtgoxLTC.show()
        #self.BTCtickers = self.mtgoxBTC

        defSetLTC = gtk.MenuItem("Choose exchange : "); defSetLTC.show()
        self.menuLTC.append(defSetLTC)
        self.menuLTC.append(self.btceLTC);#self.menuLTC.append(self.mtgoxLTC);
        self.setRefreshMenu(self.menuLTC)

        self.kill_LTC = gtk.MenuItem("LTC Off"); self.kill_LTC.connect("activate", self.noLTC); self.kill_LTC.show(); self.menuLTC.append(self.kill_LTC)
        self.quit_item = gtk.MenuItem("Quit Indicator"); self.quit_item.connect("activate", self.quit); self.quit_item.show()
        self.menuLTC.append(self.quit_item)
        self.LTCInit = True

    def menu_setupNMC(self):
        self.menuNMC = gtk.Menu()
        self.NMCtickers = None
        self.btceNMC = gtk.RadioMenuItem(self.NMCtickers,"BTC-E"); self.btceNMC.connect("activate", lambda x: self.toggleNMCdisplay("btce")); self.btceNMC.show()
        self.NMCtickers = self.btceNMC
        #self.mtgoxLTC = gtk.RadioMenuItem(self.LTCtickers,"MtGox"); self.mtgoxLTC.connect("activate", lambda x: self.toggleLTCdisplay("mtgox")); self.mtgoxLTC.show()
        #self.BTCtickers = self.mtgoxBTC

        defSetNMC = gtk.MenuItem("Choose exchange : "); defSetNMC.show()
        self.menuNMC.append(defSetNMC)
        self.menuNMC.append(self.btceNMC);#self.menuLTC.append(self.mtgoxLTC);
        self.setRefreshMenu(self.menuNMC)

        self.kill_NMC = gtk.MenuItem("NMC Off"); self.kill_NMC.connect("activate", self.noNMC); self.kill_NMC.show();self.menuNMC.append(self.kill_NMC)
        self.quit_item = gtk.MenuItem("Quit Indicator"); self.quit_item.connect("activate", self.quit); self.quit_item.show()
        self.menuNMC.append(self.quit_item)
        self.NMCInit = True

    def noLTC(self,widget):
        self.indLTC.set_label("")
        self.indLTC.set_icon("")
        self.LTCMODE = False
        self.LTCInit = False

    def noNMC(self,widget):
        self.indNMC.set_label("")
        self.indNMC.set_icon("")
        self.NMCMODE = False
        self.NMCInit = False


    def setRefreshMenu(self,menuIn):
        refreshmenu = gtk.Menu()
        refMenu =gtk.MenuItem("Set refresh rate :")
        refMenu.set_submenu(refreshmenu)

        self.refreshRates = None
        menuRefresh1 = gtk.RadioMenuItem(self.refreshRates,"3s"); menuRefresh1.connect("activate",lambda x: self.setPing(3)); menuRefresh1.show()
        self.refreshRates = menuRefresh1
        menuRefresh2 = gtk.RadioMenuItem(self.refreshRates,"10s"); menuRefresh2.connect("activate",lambda x: self.setPing(10)); menuRefresh2.show()
        self.refreshRates = menuRefresh2
        menuRefresh3 = gtk.RadioMenuItem(self.refreshRates,"30s"); menuRefresh3.connect("activate",lambda x: self.setPing(30)); menuRefresh3.show()
        self.refreshRates = menuRefresh3
        menuRefresh4 = gtk.RadioMenuItem(self.refreshRates,"1m"); menuRefresh4.connect("activate",lambda x: self.setPing(60)); menuRefresh4.show()
        self.refreshRates = menuRefresh4
        menuRefresh5 = gtk.RadioMenuItem(self.refreshRates,"5m"); menuRefresh5.connect("activate",lambda x: self.setPing(300)); menuRefresh5.show()
        self.refreshRates = menuRefresh5
        menuRefresh6 = gtk.RadioMenuItem(self.refreshRates,"10m"); menuRefresh6.connect("activate",lambda x: self.setPing(600)); menuRefresh6.show()
        self.refreshRates = menuRefresh6;

        refreshmenu.append(menuRefresh1);refreshmenu.append(menuRefresh2);refreshmenu.append(menuRefresh3);
        refreshmenu.append(menuRefresh4);refreshmenu.append(menuRefresh5);refreshmenu.append(menuRefresh6);
        refMenu.show(); refreshmenu.show()
        menuIn.append(refMenu)

    def setPing(self,newTime):
        self.PING_FREQUENCY = newTime

	# toggle function for exchanges
    def toggleBTCdisplay(self, exch):
        self.exchange = exch

	# toggle function for exchanges
    def toggleLTCdisplay(self, exch):
        self.exchangeLTC = exch

	# toggle function for exchanges
    def toggleNMCdisplay(self, exch):
        self.exchangeNMC = exch

	# function that is being called by main which will refresh data	
    def getNewPricesBTC(self):
        updatedRecently = self.update_priceBTC()
        return True
    def getNewPricesLTC(self):
        updatedRecentlyLTC = self.update_priceLTC()
        return True
    def getNewPricesNMC(self):
        updatedRecentlyNMC = self.update_priceNMC()
        return True

	# build string to be used by indicator and update the display label
    def update_priceBTC(self):
        dataOut = ""
        priceNow = BAD_RETRIEVE

        priceNow = self.getMtGoxData("")
        if priceNow == BAD_RETRIEVE:
            priceNow = "TempDown"
        else:
            priceNow = str(priceNow)+" USD"
        if "mtgox" in self.exchange:
            dataOut = dataOut + ' | ' if dataOut != "" else dataOut
            dataOut = dataOut + "MtGox: "+priceNow
        self.mtgoxBTC.set_label("MtGox| "+str(priceNow))

        priceNow = self.getBTCEDataUSD("")
        if priceNow == BAD_RETRIEVE:
            priceNow = "TempDown"
        else:
            priceNow = str(priceNow)+" USD"
        if "btce" in self.exchange:
            dataOut = dataOut + ' | ' if dataOut != "" else dataOut
            dataOut = dataOut + "BTC-E: "+priceNow
        self.btceBTC.set_label("BTC-E | "+str(priceNow))

        priceNow = self.getBitStampBTCPrice()
        if priceNow == BAD_RETRIEVE:
            priceNow = "TempDown"
        else:
            priceNow = str(priceNow)+" USD"
        if "bitstamp" in self.exchange:
            dataOut = dataOut + ' | ' if dataOut != "" else dataOut
            dataOut = dataOut + "Bitstamp: "+priceNow
        self.bitstampBTC.set_label("Bitstamp | "+str(priceNow))

        priceNow = self.getBlockChainBTCPrice()
        if priceNow == BAD_RETRIEVE:
            priceNow = "TempDown"
        else:
            priceNow = str(priceNow)+" USD"
        if "blockchain" in self.exchange:
            dataOut = dataOut + ' | ' if dataOut != "" else dataOut
            dataOut = dataOut + "Blockchain: "+priceNow
        self.blockchainBTC.set_label("Blockchain | "+str(priceNow))

        self.ind.set_label(dataOut)
        return True

    # build string to be used by indicator and update the display label
    def update_priceLTC(self):
        dataOut = ""
        priceNow = BAD_RETRIEVE
        #priceNow = self.getMtGoxData("ltc")
        #if priceNow == BAD_RETRIEVE:
        #    priceNow = "TempDown"
        #else:
        #    priceNow = str(priceNow)+" USD"
        #if self.exchangeLTC is "mtgox":
        #    dataOut = dataOut + ' | ' if dataOut != "" else dataOut
        #    dataOut = dataOut + "MtGox: "+priceNow
        #self.mtgoxLTC.set_label("MtGox| "+str(priceNow))
        priceNow = self.getBTCEDataUSD("ltc")
        if priceNow == BAD_RETRIEVE:
            priceNow = "TempDown"
        else:
            priceNow = str(priceNow)+" USD"
        if "btce" in self.exchangeLTC:
            dataOut = dataOut + ' | ' if dataOut != "" else dataOut
            dataOut = dataOut + "BTC-E: "+priceNow
        self.btceLTC.set_label("BTC-E | "+str(priceNow))
        if self.LTCMODE:
            self.indLTC.set_label(dataOut)
        return True

    # build string to be used by indicator and update the display label
    def update_priceNMC(self):
        dataOut = ""
        priceNow = BAD_RETRIEVE

        priceNow = self.getBTCEDataUSD("nmc")
        if priceNow == BAD_RETRIEVE:
            priceNow = "TempDown"
        else:
            priceNow = str(priceNow)+" USD"
        if "btce" in self.exchangeNMC:
            dataOut = dataOut + ' | ' if dataOut != "" else dataOut
            dataOut = dataOut + "BTC-E: "+priceNow
        self.btceNMC.set_label("BTC-E | "+str(priceNow))

        if self.NMCMODE:
            self.indNMC.set_label(dataOut)
        return True


	# get mtgox data using JSON
    def getMtGoxData(self,coin):
        lstMtGox = BAD_RETRIEVE
        try :
            if coin is "ltc":
                web_page = urllib2.urlopen("http://data.mtgox.com/api/1/LTCUSD/ticker").read()
            elif coin is "nmc":
                web_page = urllib2.urlopen("http://data.mtgox.com/api/1/NMCUSD/ticker").read()
            else:
                web_page = urllib2.urlopen("http://data.mtgox.com/api/1/BTCUSD/ticker").read()
            data = json.loads(web_page)
            lstMtGox = data['return']['last']['value']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print 'Decoding JSON has failed'
        return "{0:,.2f}".format(float(lstMtGox))
	
	# get btc-e data using json
    def getBTCEDataUSD(self,coin):
        lstBTCEprice = BAD_RETRIEVE
        try :
            if coin is "ltc":
                web_page = urllib2.urlopen("https://btc-e.com/api/2/ltc_usd/ticker").read()
            elif coin is "nmc":
                web_page = urllib2.urlopen("https://btc-e.com/api/2/nmc_usd/ticker").read()
            else:
                web_page = urllib2.urlopen("https://btc-e.com/api/2/btc_usd/ticker").read()
            data = json.loads(web_page)
            lstBTCEprice = data['ticker']['last']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        return "{0:,.2f}".format(float(lstBTCEprice))

    # get btc-e data using json
    def getBTCEDataBTC(self,coin):
        lstBTCEprice = BAD_RETRIEVE
        try :
            if coin is "nmc":
                web_page = urllib2.urlopen("https://btc-e.com/api/2/nmc_btc/ticker").read()
            elif coin is "nvc":
                web_page = urllib2.urlopen("https://btc-e.com/api/2/nvc_btc/ticker").read()
            elif coin is "xpm":
                web_page = urllib2.urlopen("https://btc-e.com/api/2/xom_btc/ticker").read()
            elif coin is "ftc":
                web_page = urllib2.urlopen("https://btc-e.com/api/2/ftc_btc/ticker").read()
            elif coin is "ppc":
                web_page = urllib2.urlopen("https://btc-e.com/api/2/ppc_btc/ticker").read()
            else:
                web_page = urllib2.urlopen("https://btc-e.com/api/2/ltc_btc/ticker").read()
            data = json.loads(web_page)
            lstBTCEprice = data['ticker']['last']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        return "{0:,.2f}".format(float(lstBTCEprice))

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

        return "{0:,.2f}".format(float(lstBlockChain))

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
        return "{0:,.2f}".format(float(lstBitStamp))


    #############################################
    ##########Settings###File####################
    #############################################
	# grab settings from file
    def initFromFile(self):
        try:
            with open(SETTINGSFILE): pass
        except IOError:
            print 'Need to make new file.'
            file = open(SETTINGSFILE, 'w')
            file.write(os.getcwd()+'\n')
            file.write('10 \n')
            file.write('mtgox \n')
            file.write('True \n')
            file.write('btce \n')
            file.write('True \n')
            file.write('btce \n')
            file.write('True \n')
            file.close()
        f = open(SETTINGSFILE, 'r')
        lines = f.readlines()
        currDir = (lines[0].strip())
        if ".local/share/applicatins" not in currDir:
            self.setAppDir(currDir)
        print "App Directory : "+self.APPDIR
        print "Refresh rate:",int(lines[1]),"seconds"
        self.PING_FREQUENCY = int(lines[1])
        print "BTC Exchange :",(lines[2].strip()),"   Display :",self.str2bool(lines[3].strip())
        self.exchange = (lines[2].strip())
        self.BTCMODE = self.str2bool(lines[3].strip())
        print "LTC Exchange :",(lines[4].strip()),"   Display :",self.str2bool(lines[5].strip())
        self.exchangeLTC = (lines[4].strip())
        self.LTCMODE = self.str2bool(lines[5].strip())
        print "NMC Exchange : ",(lines[6].strip()),"   Display :",self.str2bool(lines[7].strip())
        self.exchangeNMC = (lines[6].strip())
        self.NMCMODE = self.str2bool(lines[7].strip())
        f.close()

    def setAppDir(self,currDir):
        self.BTCICON = os.path.abspath(currDir+"/res/bitcoinicon.png")
        self.LTCICON = os.path.abspath(currDir+"/res/litecoinicon.png")
        self.NMCICON = os.path.abspath(currDir+"/res/nmcicon.png")
        self.APPDIR = currDir

	# utility function for settings file grab
    def str2bool(self,word):
        return word.lower() in ("yes", "true", "t", "1","ok")

    def quit(self, widget, data=None):
        gtk.main_quit()
	# save settings at quit and kill indicator
    def quit(self, widget):
        try:
            print 'Saving Last State.'
            file = open(SETTINGSFILE, 'w')
            file.write(str(self.APPDIR)+'\n')
            file.write(str(self.PING_FREQUENCY)+'\n')
            file.write(str(self.exchange)+'\n')
            file.write(str(self.BTCMODE)+'\n')
            file.write(str(self.exchangeLTC)+'\n')
            file.write(str(self.LTCMODE)+'\n')
            file.write(str(self.exchangeNMC)+'\n')
            file.write(str(self.NMCMODE)+'\n')
            file.close()
        except IOError:
            print " ERROR WRITING QUIT STATE"
        gtk.main_quit()
        sys.exit(0)

    def menu_about_response(self,widget):
        self.menu.set_sensitive(False)
        widget.set_sensitive(False)
        ad=gtk.AboutDialog()
        ad.set_name(self.APPNAME)
        ad.set_version(self.VERSION)
        ad.set_comments("A bitcoin ticker indicator")
        ad.set_license(''+
        'This program is free software: you can redistribute it and/or modify it\n'+
        'under the terms of the GNU General Public License as published by the\n'+
        'Free Software Foundation, either version 3 of the License, or (at your option)\n'+
        'any later version.\n\n'+
        'This program is distributed in the hope that it will be useful, but\n'+
        'WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY\n'+
        'or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for\n'+
        'more details.\n\n'+
        'You should have received a copy of the GNU General Public License along with\n'+
        'this program.  If not, see <http://www.gnu.org/licenses/>.')
        ad.set_website('https://github.com/jj9btcproj/Bitcoin-Price-Indicator')
        ad.set_authors(['Written by jj9: \n If you want to tip the following are jj9 addressess \n'+
                        'BTC: 1ECXwPU9umqtsBAQesBW9981mx6sipPmyL \n '+
                        'LTC : LUJz8yaS4uL1zrzwARbA4CiMpAwbpUwWY6 \n '+
                        ' NMC: N1SKXkrcyhxVYwQGsbLTFMbGAgeqL2g9tZ \n \n'+
                        'special thanks to RichHorrocks and Zapsoda for updating setup file and some btce api calls\n\n'+
                        '---jj9'])
        ad.run()
        ad.destroy()
        self.menu.set_sensitive(True)
        widget.set_sensitive(True)

if __name__ == "__main__":
    indicator = CryptoCoinPriceIndicator()
    indicator.main()
