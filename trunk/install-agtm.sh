
#Creating install folders
#Data and executables folder
sudo mkdir /usr/share/AGTM/

#Installing the main code
sudo cp -R ./src/AGTM/ /usr/share/AGTM/

#Installing runnable files
sudo cp ./install_files/advancedgnometabmenu /usr/bin/
sudo chmod +x /usr/bin/advancedgnometabmenu

#Installing desktop shortcuts
sudo cp -R ./install_files/logo_agtm.png /usr/share/pixmaps/AGTM.png
sudo cp ./install_files/agtm.desktop /usr/share/applications/

