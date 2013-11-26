import os
import shutil
from os.path import expanduser
import subprocess
from subprocess import call
import codecs

HOME = expanduser("~")

ICON = os.path.abspath(HOME+"/.local/share/applications/bitcoinicon.png")
SETTINGSFILE = os.path.abspath(HOME+"/.local/share/applications/settingsBTC.txt")
INDICATORFILE = os.path.abspath(HOME+"/.local/share/applications/btc-price-indicator.py")
DESKTOPFILE = os.path.abspath(HOME+"/.config/autostart/btc-price-indicator.desktop")

removeIn = raw_input("Setup Or Remove?: ")
removePack = False

if "emove" in removeIn.lower().strip():
    removePack = True
    print "Removing from system."

if removePack:
    FILES = [ICON, SETTINGSFILE, INDICATORFILE, DESKTOPFILE]
    for FILE in FILES:
        if os.path.exists(FILE):
            os.remove(FILE)
            print 'Removed:',FILE
    print 'Removed files.'
else:
    dirIn = raw_input( "Enter directory of extracted zip file (default is current directory):")
    
    if dirIn == '':
        dirIn = '.'

    if dirIn.endswith('/'):
        dirIn = dirIn[:-1]

    dirIn = os.path.abspath(dirIn)
    print "Setup from:",dirIn

    iconTemp = dirIn+"/res/bitcoinicon.png"
    indTemp = dirIn+"/bitcoin-price-indicator.py"
    deskTemp = dirIn+"/bitcoin-price-indicator.desktop"

    subprocess.call(["sudo", "/" + dirIn + "/installDependencies.sh"])
    print "Installing dependencies"
    
    subprocess.call(["sudo", "/" + dirIn + "/makeDesktopFile.sh"])
    print "Making desktop file, Run to launch ticker."

    if not os.path.exists(HOME+"/.local/share/applications/"):
        subprocess.call(["mkdir", HOME+"/.local/share/applications/"])
        print "Making folder:",HOME+"/.local/share/applications/"

    #Try moving icon
    try:
        shutil.copyfile(iconTemp,ICON)
        print 'Moving icon to',ICON
    except IOError:
        print 'Error moving icon.'

    #Try moving icon
    try:
        shutil.copyfile(indTemp,INDICATORFILE)
        print 'Moving application to',INDICATORFILE
    except IOError:
        print 'Error moving application.'

    #Ask to move file to startup
    if 'y' in raw_input("Run on startup? (Y/N): ").lower().strip():
        if not os.path.exists(HOME+"/.config/autostart/"):
            subprocess.call(["mkdir", HOME+"/.config/autostart/"])
            print "Making folder:",HOME+"/.config/autostart/"
        try:
            shutil.copyfile(deskTemp,DESKTOPFILE)
            print 'Moving desktop file to autostart folder.'
        except IOError:
            print 'Error desktop file to autostart folder.'

    #Try to make settings file
    try:
        print 'Making settings file:',SETTINGSFILE
        file = open(SETTINGSFILE, 'w')
        file.write('3 \n')
        file.write('True\n')
        file.write('True\n')
        file.write('True\n')
        file.write('True\n')
        file.close()  
    except IOError:
        print "Error making settings file"

    subprocess.call(["chmod","+x",INDICATORFILE])
    print "Script is located at: "+INDICATORFILE

    try:
        subprocess.call(["sudo", "/" + dirIn + "/setupAlias.sh"])
        print "---------------------------------"
        print "Indicator installed close terminal"
        print "To run script type: btc-indicator"
        print "You must open a new terminal first"
    except OSError:
        print 'Error creating script alias'
exit(0)