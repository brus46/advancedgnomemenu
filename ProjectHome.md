# Advanced Gnome Menu #

This is an eye-candy menu applet for GNOME. (soon even compatibility with KDE and XFCE)

Good looks and usability are the key aims of this project.

Just see it at work and you'll love it ;)
## Project members ##

  * chief developer: Marco Mosconi, brus46@gmail.com
  * developer: Fanen Ahua
  * image designer: Sentinella86

## Source install: ##

  * Download the source
  * Untar it on your pc
  * give the command ./install.sh

## Deb install: ##

  * Download the deb package
  * Double click on the .deb file

## Svn install ##

  * Install subversion (on debian-ubuntu: sudo apt-get install subversion)
  * Create a directory where put the program.
  * Open a terminal and move to that directory
  * Run this command: svn checkout http://advancedgnomemenu.googlecode.com/svn/trunk/ advancedgnomemenu-read-only
  * Enter into the new folder and execute ./install.sh
  * This script will install the latest svn version of agm (please, note that if you use the agm-panel you must remove it and re-add if you want to see changes, if you reboot you obtain the same..).

## Add to panel ##

Once you've installed the program right-click on a gnome panel and select "Add to the panel".

Then select from the gnome applets list "AGM"


## Add to a dock ##

Actually there's no plugin for any dock.

You can use an "experimental-way"

Add a launcher on your bar and set as command "advancedgnomemenu --no-tray-icon"

This should work but sometimes may crashes...
