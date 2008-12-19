#    Author name:    Marco Mosconi
#    Author email:   brus46@gmail.com
#    Author website: http://www.sciallo.net

#    This file is part of AGM.

#    AGM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk, os, sys
import AGM.AGM_utils as utils
from AGM.AGM_info import Info

class InfoMenu(gtk.Menu):
    def __init__(self):
        gtk.Menu.__init__(self)
        
        info=gtk.MenuItem()
        infoBox=gtk.HBox(spacing=5)
        infoImage=gtk.Image()
        infoImage.set_from_stock(gtk.STOCK_INFO, gtk.ICON_SIZE_MENU)
        infoBox.pack_start(infoImage, False, False)
        infoBox.pack_start(gtk.Label("Info about AGM"), False, False)
        infoBox.show_all()
        info.add(infoBox)

        gnome_info=gtk.MenuItem()
        gnome_infoBox=gtk.HBox(spacing=5)
        gnome_infoImage=gtk.Image()
        #gnome-logo-icon-transparent
        gnome_infoImage.set_from_pixbuf(utils.getPixbufFromName("gnome-logo-icon-transparent", 18))
        gnome_infoBox.pack_start(gnome_infoImage, False, False)
        gnome_infoBox.pack_start(gtk.Label("Info about Gnome"), False, False)
        gnome_infoBox.show_all()
        gnome_info.add(gnome_infoBox)
        
        ubuntu_info=gtk.MenuItem()
        ubuntu_infoBox=gtk.HBox(spacing=5)
        ubuntu_infoImage=gtk.Image()
        ubuntu_infoImage.set_from_pixbuf(utils.getPixbufFromName("distributor-logo", 18))
        ubuntu_infoBox.pack_start(ubuntu_infoImage, False, False)
        ubuntu_infoBox.pack_start(gtk.Label("Info about Ubuntu linux"), False, False)
        ubuntu_infoBox.show_all()
        ubuntu_info.add(ubuntu_infoBox)
        
        self.append(info)
        self.append(gnome_info)
        self.append(ubuntu_info)

        info.connect("activate", self.agm_info)        
        gnome_info.connect("activate", self.gnome_info)        
        ubuntu_info.connect("activate", self.ubuntu_info)        
        
        info.show()
        gnome_info.show()
        ubuntu_info.show()

        pass
    
    def gnome_info(self, obj=None):
        if (os.fork()==0):
            os.execvp("gnome-about", ["gnome-about"])
            sys.exit(-1)
    
    def ubuntu_info(self, obj=None):
        if (os.fork()==0):
            os.execvp("yelp", ["yelp", "ghelp:about-ubuntu"])
            sys.exit(-1)
    
    def agm_info(self, obj=None):
        Info()
    
    def show(self, button_clicked):
        self.popup(None, None, None, 0, 0)
        pass