
#Creating install folders
#Data and executables folder
sudo mkdir /usr/share/AGTM/
#Lib folder
sudo mkdir /usr/local/lib/python/

#Installing the main code

#Installing the main code
sudo cp ./src/AGTM.py /usr/share/AGTM/
sudo chmod +x /usr/share/AGTM/AGTM.py
sudo cp -R ./src/AGTM/ /usr/local/lib/python/
sudo cp -R ./src/AG_commons/ /usr/local/lib/python/

#Installing runnable files
sudo cp ./install_files/advancedgnometabmenu.sh /usr/bin/advancedgnometabmenu
sudo chmod +x /usr/bin/advancedgnometabmenu

#Installing desktop shortcuts
sudo cp -R ./install_files/logo_agtm.png /usr/share/pixmaps/AGTM.png
sudo cp ./install_files/agtm.desktop /usr/share/applications/

