#!/bin/bash

#Creating install folders
#Data and executables folder
sudo mkdir /usr/share/AGM/
#Lib folder
sudo mkdir /usr/local/lib/python/

#Installing the main code
sudo cp ./src/AGM.py /usr/share/AGM/
sudo cp ./src/AGM_configurator.glade /usr/share/AGM/
sudo cp -R ./src/pictures/ /usr/share/AGM/
sudo cp -R ./src/AGM/ /usr/local/lib/python/
sudo cp -R ./src/AGMplugins/ /usr/local/lib/python/
sudo cp -R ./src/AGM_Fav_apps_models/ /usr/local/lib/python/

#Installing translation pack
sudo cp -R ./src/locale/ /usr/share/AGM/

#make config dir
mkdir ~/.config/agm/
#make theme dir
mkdir ~/.config/agm/themes/

#move old config if exist
CFILE=~/.AGM_config
if [ -f $CFILE ];
then mv ~/.AGM_config ~/.config/agm/AGM_config
fi

#install default config if necessary
CFILE=~/.config/agm/AGM_config
if [ -f $CFILE ];
then echo "config file already exists, skipping"
else cp ./src/AGM_default_config ~/.config/agm/AGM_config
fi

#move old fav apps if exist
CFILE=~/.AGM_fav_app
if [ -f $CFILE ];
then mv ~/.AGM_fav_app ~/.config/agm/AGM_fav_app
fi

#install default fav apps if necessary
CFILE=~/.config/agm/AGM_fav_app
if [ -f $CFILE ]; 
then echo "favourite apps already configured, skipping"
else cp ./src/AGM_default_fav_app ~/.config/agm/AGM_fav_app
fi

#move old themes if exist
mv ~/.AGM/themes/* ~/.config/agm/themes/
rm -R ~/.AGM/

#Installing runnable files
sudo cp ./install_files/advancedgnomemenu /usr/bin/
sudo chmod +x /usr/bin/advancedgnomemenu

#Installing desktop shortcuts
sudo cp -R ./install_files/AGM.png /usr/share/pixmaps/
sudo cp ./install_files/agm-config.desktop /usr/share/applications/
sudo cp ./install_files/agm.desktop /usr/share/applications/

#Installing Gnome_applet
sudo cp -R ./src/gnomeAgmApplet.py /usr/share/AGM/
sudo chmod +x /usr/share/AGM/gnomeAgmApplet.py
sudo chmod +r /usr/share/AGM/gnomeAgmApplet.py
sudo cp -R ./src/gnomeAgmApplet.server /usr/lib/bonobo/servers/
sudo chmod +x /usr/lib/bonobo/servers/gnomeAgmApplet.server
sudo chmod +r /usr/lib/bonobo/servers/gnomeAgmApplet.server

