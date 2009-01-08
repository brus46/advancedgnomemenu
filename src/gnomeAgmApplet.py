#!/usr/bin/env python

#    Program name: AGM - Advanced Gnome Menu
#    Project version: 0.8
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
#from AGM.AGM_focus_thread import FocusThread as ShowThread

conf=config()

class AGM_applet(gnomeapplet.Applet):
    def __init__(self,applet,iid):
        self.__gobject_init__()
        self.applet = applet
        self.AGM=agm(False, False, False, applet=True)
        self.mybutton=gtk.HBox()
        self.icon=gtk.Image()
        size=self.get_size()
        self.icon.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(conf.applet_icon, size, size))
        self.label=gtk.Label()
        if (conf.applet_show_text): self.label.set_text(conf.applet_text)
        self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.applet_fg_color))
        self.icon.set_size_request(size, size)
        self.mybutton.add(self.icon)
        self.mybutton.add(self.label)
        
        self.X, self.Y=0, 0
        self.popup=AGM.AGM_default_config.popup_style()
        self.top_icon=AGM.AGM_default_config.top_position()
        self.gravity=gtk.gdk.GRAVITY_NORTH_WEST
        
        self.orientation = self.applet.get_orient()
        
        self.applet.add(self.mybutton)
        self.applet.add_events(gtk.gdk.MOTION_NOTIFY | gtk.gdk.BUTTON_PRESS)

        self.applet.connect("motion_notify_event", self.motion_notify)
        self.applet.connect("button_press_event", self.showHelpMenu, applet)
        self.applet.connect("destroy-event",self.cleanup)
        self.applet.connect("delete-event",self.cleanup)
        self.applet.connect("change-size", self.on_change_size)
        self.applet.connect("change-background", self.change_background)
        self.applet.connect("change-orient",self.change_orientation)
        #self.ShowThread=ShowThread(self.AGM.win.has_toplevel_focus, self.has_focus, self.AGM.get_hidden, self.AGM.set_hidden, self.AGM.setOnFocus)
        self.applet.show_all()
        self.change_orientation(None, None)

        #self.ShowThread.start()
        pass
    
    def has_focus(self):
        return self.label.is_focus()
    
    def get_size(self):
        try:
            size=self.applet.get_size()
        except: size=24
        if size<24:
            size=24
        return size
    
    def on_change_size (self):
        size=self.get_size()
        w, h=self.label.size_request()
        pixbuf=gtk.gdk.pixbuf_new_from_file(conf.applet_icon)
        width=pixbuf.get_width()
        height=pixbuf.get_height()
        if self.orientation == gnomeapplet.ORIENT_UP or self.orientation == gnomeapplet.ORIENT_DOWN:
            if height > size:
                width=width*size/height
                height=size
        else:
            if width > size:
                height=height*size/width
                width=size
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
        pass
    
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
        self.mybutton = tmpbox
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
        #self.ShowThread.stop()
        del self.applet
    
    def showHelpMenu(self, widget, event, applet):
        if event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 3:
                self.create_menu(applet)
            else: self.showMenu()
    
    def showMenu(self):
        if (self.AGM.get_hidden()):
           self.define_menu()
           
           self.AGM.show(self.X, self.Y, self.popup, self.top_icon, self.gravity)
           #self.AGM.show()
        else:
           self.AGM.hide()
    
    def create_menu(self, applet):
        propxml="""
                <popup name="button3">
                <menuitem name="About" verb="About" label="_About" pixtype="stock" pixname="gtk-about"/>
                <menuitem name="EditGnomeMenu" verb="EditGnomeMenu" label="Edit Gnome Menu" pixtype="stock" pixname="gtk-preferences"/>
                <menuitem name="ConfigFavApps" verb="ConfigFavApps" label="Config FavApps" pixtype="stock" pixname="gtk-preferences"/>
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
    AGM_applet(applet,iid)
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




