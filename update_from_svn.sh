#!/bin/bash
# This script will update agm to the latest svn version.

echo "gksu apt-get install subversion"
gksu 'apt-get install subversion'

echo "svn checkout http://advancedgnomemenu.googlecode.com/svn/trunk/ advancedgnomemenu-read-only"
svn checkout http://advancedgnomemenu.googlecode.com/svn/trunk/ advancedgnomemenu-read-only

echo "cd ./advancedgnomemenu-read-only"
cd ./advancedgnomemenu-read-only

echo "./install.sh"
gksu './install.sh'

echo "cd .."
cd ..

echo "sudo rm -R ./advancedgnomemenu-read-only"
sudo rm -R ./advancedgnomemenu-read-only

echo "AGM Updated"