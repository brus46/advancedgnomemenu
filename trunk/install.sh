#!/bin/bash

#Creating install folders
sudo mkdir /usr/share/AGM/
sudo mkdir /usr/local/lib/python/

#Installing the main code
sudo cp ./src/AGM.py /usr/share/AGM/
sudo cp -R ./src/pictures/ /usr/share/AGM/
sudo cp -R ./src/AGM/ /usr/local/lib/python/
sudo cp -R ./src/AGMplugins/ /usr/local/lib/python/

#Installing runnable files
sudo cp ./install_files/advancedgnomemenu /usr/bin/
sudo chmod +x /usr/bin/advancedgnomemenu

#Installing desktop shortcuts
sudo cp ./install_files/AGM.png /usr/share/pixmaps/
sudo cp ./install_files/agm-config.desktop /usr/share/applications/
sudo cp ./install_files/agm.desktop /usr/share/applications/

#Installing Gnome_applet
sudo cp -R ./src/gnomeAgmApplet.py /usr/share/AGM/
sudo chmod 777 /usr/share/AGM/gnomeAgmApplet.py
sudo cp -R ./src/gnomeAgmApplet.server /usr/lib/bonobo/servers/
sudo chmod 777 /usr/lib/bonobo/servers/gnomeAgmApplet.server
