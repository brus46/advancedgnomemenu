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


import gtk
import os
from AGM.AGM_info import Info
from AGM.AGM_config import Config
from AGM.AGM_default_config import conf as config

conf=config()

class TrayIcon(gtk.StatusIcon):
    
    def __init__(self, window):
        self.win=window
        gtk.StatusIcon.__init__(self)
        self.connect("activate", self.tray_icon_on_click);
        self.connect("popup-menu",self.tray_icon_on_menu);
        self.set_from_file(conf.default_logo_path);
        self.set_tooltip("AdvancedGnomeMenu");
        self.set_visible(True)
        self.menu = TrayMenu()
        pass
    def tray_icon_on_click(self, user_data):
        self.win.setOnFocus()
        
    def tray_icon_on_menu(self, button, activation_time, user_data):
        self.menu.show(self)


class TrayMenu(gtk.Menu):
    def __init__(self):
        gtk.Menu.__init__(self)
        
        config=gtk.MenuItem()
        configBox=gtk.HBox(spacing=5)
        configImage=gtk.Image()
        configImage.set_from_stock(gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_MENU)
        configBox.pack_start(configImage, False, False)
        configBox.pack_start(gtk.Label("Config AGM"), False, False)
        configBox.show_all()
        config.add(configBox)
        
        
        info=gtk.MenuItem()
        infoBox=gtk.HBox(spacing=5)
        infoImage=gtk.Image()
        infoImage.set_from_stock(gtk.STOCK_INFO, gtk.ICON_SIZE_MENU)
        infoBox.pack_start(infoImage, False, False)
        infoBox.pack_start(gtk.Label("Info about AGM"), False, False)
        infoBox.show_all()
        info.add(infoBox)
        
        exit=gtk.MenuItem()
        exitBox=gtk.HBox(spacing=5)
        exitImage=gtk.Image()
        exitImage.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        exitBox.pack_start(exitImage, False, False)
        exitBox.pack_start(gtk.Label("Exit"), False, False)
        exitBox.show_all()
        exit.add(exitBox)
        
        
        self.append(config)
        self.append(info)
        self.append(exit)

        config.connect("activate", self.config)
        info.connect("activate", self.info)        
        exit.connect("activate", self.close)
        
        config.show()
        info.show()
        exit.show()
        pass

    def config(self, obj=None):
        Config()
    
    def info(self, obj=None):
        Info()

    def close(self, obj=None):
        gtk.main_quit()
    
    def show(self, button_clicked):
        self.popup(None, None, None, 0, 0)
        #Exit, Info, Config, Edit menu
        pass