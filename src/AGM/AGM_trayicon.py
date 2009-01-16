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
import AGM.AGM_default_config

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
        self.X=0
        self.Y=0
        self.popup=AGM.AGM_default_config.popup_style()
        self.top_icon=AGM.AGM_default_config.top_position()
        self.gravity=gtk.gdk.GRAVITY_NORTH_WEST

        #for widget in self.get_icon():
        #    print widget
        #    widget.add_events(gtk.gdk.MOTION_NOTIFY | gtk.gdk.BUTTON_PRESS)
        #    widget.connect("motion_notify_event", self.motion_notify)

        #rootwin = self.get_screen().get_root_window()
        #rootwin.add_events(gtk.gdk.MOTION_NOTIFY | gtk.gdk.BUTTON_PRESS)

        #rootwin.connect("motion_notify_event", self.motion_notify)

        self.menu = TrayMenu()
        pass
    def tray_icon_on_click(self, user_data):
        if (self.win.get_hidden()):
            
            self.motion_notify(None, None)
            self.define_menu()
            self.win.show(self.X, self.Y, self.popup, self.top_icon, self.gravity)
        else:
            self.win.hide()
        
    def tray_icon_on_menu(self, button, activation_time, user_data):
        self.menu.show(self)

    def motion_notify(self, widget, event):
        if event!=None:
            xw, yw=event.x, event.y
        else: xw, yw=(32,32)
        rootwin = self.get_screen().get_root_window()
        x, y, mods = rootwin.get_pointer()
        #w, h=self.get_size_request()
        w, h=(32, 32)
        
        if y<200:
            self.X=x-xw
            self.Y=y-yw+h
            self.popup.set_width(w)
        else:
            self.X=x-xw
            self.Y=y-yw
            self.popup.set_width(w)
    def define_menu(self):
        screen_w, screen_h=(gtk.gdk.screen_width(), gtk.gdk.screen_height())
        width, height = (conf.window_width, conf.window_height)
        
        self.top_icon=AGM.AGM_default_config.top_position()
        self.popup=AGM.AGM_default_config.popup_style()
        
        if (self.Y<=screen_h/2):
            #Top icon sud
            if (self.X<=screen_w/2):
                #Top icon east
                self.top_icon.set_pos(self.top_icon.DW_RIGHT)
                self.gravity=gtk.gdk.GRAVITY_NORTH_WEST
            else:
                #top icon west
                self.top_icon.set_pos(self.top_icon.DW_LEFT)
                self.gravity=gtk.gdk.GRAVITY_NORTH_EAST
        else:
            #Top icon nord
            if (self.X<=screen_w/2):
                #Top icon east
                self.top_icon.set_pos(self.top_icon.TOP_RIGHT)
                self.gravity=gtk.gdk.GRAVITY_SOUTH_WEST
            else:
                #top icon west
                self.top_icon.set_pos(self.top_icon.TOP_LEFT)
                self.gravity=gtk.gdk.GRAVITY_SOUTH_EAST
        
        if (self.X<=screen_w/2):
            self.popup.set(self.popup.LEFT)
        else:
            self.popup.set(self.popup.RIGHT)
        
        

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
        
        configGM=gtk.MenuItem()
        configGMBox=gtk.HBox(spacing=5)
        configGMImage=gtk.Image()
        configGMImage.set_from_stock(gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_MENU)
        configGMBox.pack_start(configGMImage, False, False)
        configGMBox.pack_start(gtk.Label("Edit gnome menu"), False, False)
        configGMBox.show_all()
        configGM.add(configGMBox)
        
        configFA=gtk.MenuItem()
        configFABox=gtk.HBox(spacing=5)
        configFAImage=gtk.Image()
        configFAImage.set_from_stock(gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_MENU)
        configFABox.pack_start(configFAImage, False, False)
        configFABox.pack_start(gtk.Label("Config Fav apps"), False, False)
        configFABox.show_all()
        configFA.add(configFABox)
        
        
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
        
        self.append(info)
        self.append(exit)
        self.append(config)
        self.append(configFA)
        self.append(configGM)
    
        config.connect("button-press-event", self.config)
        configGM.connect("button-press-event", self.configGM)
        configFA.connect("button-press-event", self.configFA)
        info.connect("button-press-event", self.info)        
        exit.connect("button-press-event", self.close)
        
        config.show()
        configFA.show()
        configGM.show()
        info.show()
        exit.show()
        pass

    def config(self, obj=None, event=None):
        Config()

    def configFA(self, obj=None, event=None):
        from AGM.AGM_config_fav_apps import ConfigFavApps
        ConfigFavApps()
        
    def configGM(self, obj=None, event=None):
        if os.fork()==0:
            try:
                os.execvp("alacarte", ["alacarte"])
            except: print "Launching Alacarte."
            sys.exit(-1)
    
    def info(self, obj=None, event=None):
        Info()

    def close(self, obj=None, event=None):
        gtk.main_quit()
    
    def show(self, button_clicked):
        self.popup(None, None, None, 0, 0)