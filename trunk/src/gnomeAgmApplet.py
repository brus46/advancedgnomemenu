#!/usr/bin/env python

#    Program name: AGM - Advanced Gnome Menu
#    Project version: 0.8.4
#    Project licence: GPL v3
# 
#    Author name:    Marco Mosconi
#    Author email:   brus46@gmail.com
#    Author website: http://www.sciallo.net

#    This program is free software: you can redistribute it and/or modify
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

import pygtk
import os, sys, gobject
pygtk.require('2.0')

FILEPATH = os.path.abspath(__file__)
pwd, dirname = os.path.split(os.path.dirname(FILEPATH))
if dirname != "src":
    print 'Running installed agm_applet, modifying PYTHONPATH.'
    sys.path.insert(0, "/usr/local/lib/python/")

from AGM.AGM_default_config import conf as config
import AGM.AGM_default_config
import gnomeapplet
import gtk
from AGM.AGM_Main_Window import AGM as agm
import AGM.AGM_utils as utils
#from AGM.AGM_focus_thread import FocusThread as ShowThread

conf=config()

class AGM_applet(gnomeapplet.Applet):
    def __init__(self,applet,iid):
        self.__gobject_init__()
        self.last_size=32
        self.applet = applet
        applet.set_applet_flags(gnomeapplet.EXPAND_MINOR)
        
        self.AGM=agm(False, False, False, applet=True, applet_unpressed=self.set_unpressed_icon)
        self.mybutton=gtk.HBox()
        self.icon=gtk.Image()
        size=self.get_size()
        self.icon_name=conf.applet_icon
        self.icon.set_from_pixbuf(utils.getPixbufFromName(self.icon_name, size))
        self.label=gtk.Label()
        if (conf.applet_show_text): self.label.set_text(conf.applet_text)
        self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.applet_fg_color))
        self.icon.set_size_request(size, size)
        
        #self.mybutton.pack_start(self.icon, False)
        #self.mybutton.add(self.label)
        
        self.X, self.Y=0, 0
        self.popup=AGM.AGM_default_config.popup_style()
        self.top_icon=AGM.AGM_default_config.top_position()
        self.gravity=gtk.gdk.GRAVITY_NORTH_WEST
        
        self.orientation = self.applet.get_orient()
        
        self.applet.add(self.mybutton)
        self.applet.add_events(gtk.gdk.MOTION_NOTIFY | gtk.gdk.BUTTON_PRESS)

        self.applet.connect("motion_notify_event", self.motion_notify)
        self.applet.connect("button-press-event", self.showHelpMenu, applet)
        self.applet.connect("destroy-event",self.cleanup)
        self.applet.connect("delete-event",self.cleanup)
        #self.applet.connect("change-size", self.on_change_size)
        self.applet.connect("change-background", self.change_background)
        self.applet.connect("change-orient",self.change_orientation)
        
        self.mybutton.connect("size-allocate",self.on_change_size)
        
        #self.ShowThread=ShowThread(self.AGM.win.has_toplevel_focus, self.has_focus, self.AGM.get_hidden, self.AGM.set_hidden, self.AGM.setOnFocus)
        self.applet.show_all()
        self.change_orientation(None, None)

        #self.ShowThread.start()
        pass
    
    def change_config(self):   
        size=self.get_size()
        self.icon.set_from_pixbuf(utils.getPixbufFromName(conf.applet_icon, size))
        if (conf.applet_show_text): 
            self.label.set_text(conf.applet_text)
        else:
            self.label.set_text("")
        self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.applet_fg_color))
        
        self.on_change_size()
        self.mybutton.show_all()
    def has_focus(self):
        return self.label.is_focus()
    
    def get_size(self):
        try:
            if self.orientation == gnomeapplet.ORIENT_UP or self.orientation == gnomeapplet.ORIENT_DOWN:
                size=self.mybutton.get_allocation().height
            else: size=self.mybutton.get_allocation().width
        except:
            size=self.last_size

        if size<32:
            size=32
        self.last_size=size
        return size
    
    def on_change_size (self, obj=None, rect=None, force=False):
        last_size=self.last_size
        size=self.get_size()
        #print size
        if size!=last_size or force:
            w, h=self.label.size_request()
            pixbuf=utils.getPixbufFromName(self.icon_name, size=256)
            width=pixbuf.get_width()
            height=pixbuf.get_height()
            if self.orientation != gnomeapplet.ORIENT_UP and self.orientation != gnomeapplet.ORIENT_DOWN:
                if width != size:
                    height=height*size/width
                    width=size
            else:
                if height != size:
                    width=width*size/height
                    height=size
    
            pixbuf = pixbuf.scale_simple(width, height, gtk.gdk.INTERP_HYPER)
            self.icon.set_from_pixbuf(pixbuf)
            self.icon.set_size_request(width, size)
            
            if self.orientation == gnomeapplet.ORIENT_UP or self.orientation == gnomeapplet.ORIENT_DOWN:
                self.label.set_angle(0)
                widthL, heightL=self.label.size_request()
                self.applet.set_size_request( width+widthL+5,size)
                
            else:
                if self.orientation == gnomeapplet.ORIENT_LEFT:
                    self.label.set_angle(270)
                else: self.label.set_angle(90)
                widthL, heightL=self.label.size_request()
                self.applet.set_size_request( size, height+heightL+5)
    
    def change_orientation(self,arg1,data):
        self.orientation = self.applet.get_orient()

        if self.orientation == gnomeapplet.ORIENT_UP or self.orientation == gnomeapplet.ORIENT_DOWN:
            tmpbox = gtk.HBox()
        else:
            tmpbox = gtk.VBox()
        
        # reparent all the hboxes to the new tmpbox
        for i in (self.mybutton.get_children()):
            i.reparent(tmpbox)

        # now remove the link between big_evbox and the box
        self.applet.remove(self.applet.get_children()[0])
        for child in self.mybutton:
            self.mybutton.remove(child)
        self.mybutton.add(tmpbox)
        tmpbox.pack_start(self.icon, False)
        tmpbox.add(self.label)
        self.applet.add(self.mybutton)
        self.on_change_size()
        self.applet.show_all()
    
    def change_background(self, applet, type, color, pixmap):
        applet.set_style(None)
        applet.modify_style(gtk.RcStyle())
        if (type == gnomeapplet.COLOR_BACKGROUND):
            applet.modify_bg(gtk.STATE_NORMAL, color)
        elif (type == gnomeapplet.PIXMAP_BACKGROUND):
            applet.get_style().bg_pixmap[gtk.STATE_NORMAL] = pixmap

    
    def cleanup(self, win):
        self.AGM.exit(None)
        del self.applet
    
    def showHelpMenu(self, widget, event, applet):
        #print event.type, event.button
        if event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 3:
                self.create_menu(applet)
            else: self.showMenu()
    
    def set_pressed_icon(self):
        if conf.use_applet_icon_pressed:
            self.icon_name=conf.applet_icon_pressed
            self.on_change_size(force=True)
    
    def set_unpressed_icon(self):
        if conf.use_applet_icon_pressed: 
            self.icon_name=conf.applet_icon
            self.on_change_size(force=True)

    def showMenu(self):
        if (self.AGM.get_hidden()):
           self.define_menu()
           self.AGM.show(self.X, self.Y, self.popup, self.top_icon, self.gravity)
           self.set_pressed_icon()
        else:
           self.AGM.hide()
           self.set_unpressed_icon()
    
    def create_menu(self, applet):
        propxml="""
                <popup name="button3">
                <menuitem name="About" verb="About" label="_About" pixtype="stock" pixname="gtk-about"/>
                <menuitem name="EditGnomeMenu" verb="EditGnomeMenu" label="Edit Gnome Menu" pixtype="stock" pixname="gtk-preferences"/>
                <menuitem name="Config" verb="Config" label="Config AGM" pixtype="stock" pixname="gtk-preferences"/>
                <menuitem name="Reload" verb="Reload" label="Reload" pixtype="stock" pixname="gtk-refresh"/>
                </popup>
                
                """
        verbs = [("About", self.showAboutDialog), ("Config", self.showConfigDialog), ("ConfigFavApps", self.showFavAppsConfig), ("EditGnomeMenu", self.configMenuAlacarte), ("Reload", self.reload)]
        self.applet.setup_menu(propxml, verbs, None)
    
    def reload(self, *arguments, **keywords):
        sys.exit(-1)
    
    def showFavAppsConfig(self, *arguments, **keywords):
        from AGM.AGM_config_fav_apps import ConfigFavApps
        ConfigFavApps()
    
    def configMenuAlacarte(self, *arguments, **keywords):
        if os.fork()==0:
            try:
                os.execvp("alacarte", ["alacarte"])
            except: print "Launching Alacarte."
            sys.exit(-1)
    
    def showAboutDialog(self, *arguments, **keywords):
        from AGM.AGM_info import Info
        Info()
    
    def showConfigDialog(self, *arguments, **keywords):
        from AGM.AGM_config import Config
        Config()
    
    def motion_notify(self, widget, event):
        xw, yw=event.x, event.y
        rootwin = widget.get_screen().get_root_window()
        x, y, mods = rootwin.get_pointer()
        w, h=self.applet.get_size_request()
        
        if self.orientation == gnomeapplet.ORIENT_UP:
            self.X=x-xw
            self.Y=y-yw+h
            self.popup.set_width(w)
        elif self.orientation == gnomeapplet.ORIENT_DOWN:
            self.X=x-xw
            self.Y=y-yw
            self.popup.set_width(w)
        elif self.orientation == gnomeapplet.ORIENT_LEFT:
            self.X=x-xw
            self.Y=y-yw
            self.popup.set_width(0)
        elif self.orientation == gnomeapplet.ORIENT_RIGHT:
            self.X=x-xw+w
            self.Y=y-yw
            self.popup.set_width(0)
        
        diff, applet_diff=conf.read_conf()
        if applet_diff: self.change_config()
        #print self.X, self.Y
        
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
        
        
gobject.type_register(AGM_applet)    
    
def factory(applet, iid):
    agm_applet=AGM_applet(applet,iid)
    applet.set_background_widget(applet)
    applet.show_all()
    return gtk.TRUE
    
if len(sys.argv)>=2 and (sys.argv[1]=="--test"):
    mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
    print "APPLET_TEST"
    mainWindow.set_title("Test Panel")
    mainWindow.connect("destroy", gtk.main_quit)
    applet = gnomeapplet.Applet()
    factory(applet, None)
    applet.reparent(mainWindow)
    mainWindow.show_all()
    gtk.main()
    sys.exit()

if __name__ == '__main__':
	print "Starting factory"
	gnomeapplet.bonobo_factory("OAFIID:Gnome_Panel_Agm_Factory", AGM_applet.__gtype__, "An eye candy menu for gnome", "1.0", factory)

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
        
#        configFA=gtk.MenuItem()
#        configFABox=gtk.HBox(spacing=5)
#        configFAImage=gtk.Image()
#        configFAImage.set_from_stock(gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_MENU)
#        configFABox.pack_start(configFAImage, False, False)
#        configFABox.pack_start(gtk.Label("Config Fav apps"), False, False)
#        configFABox.show_all()
#        configFA.add(configFABox)
        
        
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
        exitBox.pack_start(gtk.Label("Reload"), False, False)
        exitBox.show_all()
        exit.add(exitBox)
        
        self.append(info)
        self.append(exit)
        self.append(config)
        #self.append(configFA)
        self.append(configGM)
    
        config.connect("button-press-event", self.config)
        configGM.connect("button-press-event", self.configGM)
        #configFA.connect("button-press-event", self.configFA)
        info.connect("button-press-event", self.info)        
        exit.connect("button-press-event", self.close)
        
        config.show()
        #configFA.show()
        configGM.show()
        info.show()
        exit.show()
        pass

    def config(self, obj=None, event=None):
        Config()

#    def configFA(self, obj=None, event=None):
#        from AGM.AGM_config_fav_apps import ConfigFavApps
#        ConfigFavApps()
        
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


