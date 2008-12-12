#!/usr/bin/env python

#    Program name: AGM - Advanced Gnome Menu
#    Project version: 0.5
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
import gnomeapplet
import gtk
from AGM.AGM_Main_Window import AGM as agm
from AGM.AGM_focus_thread import FocusThread as ShowThread

conf=config()

class AGM_applet(gnomeapplet.Applet):
    def __init__(self,applet,iid):
        self.__gobject_init__()
        self.applet = applet
        self.AGM=agm(False, False, False)
        mybutton=gtk.HBox()
        self.icon=gtk.Image()
        size=self.get_size()
        self.icon.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(conf.applet_icon, size, size))
        self.label=gtk.Label()
        self.label.set_text(conf.applet_text)
        self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.applet_fg_color))
        self.icon.set_size_request(size, size)
        mybutton.add(self.icon)
        mybutton.add(self.label)
        
        width, height=self.label.size_request()
        self.applet.set_size_request(size+width+5, size)
        self.applet.add(mybutton)
        self.applet.connect("button_press_event", self.showMenu, applet)
        self.applet.connect("destroy",self.cleanup)
        #self.applet.connect("change-size", self.change_size)
        self.applet.connect("change-background", self.change_background)
        
        self.ShowThread=ShowThread(self.AGM.win.has_toplevel_focus, self.has_focus, self.AGM.get_hidden, self.AGM.set_hidden, self.AGM.setOnFocus)
        self.applet.show_all()
        self.on_change_size()
        self.ShowThread.start()
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
        pixbuf=gtk.gdk.pixbuf_new_from_file(conf.applet_icon)
        width=pixbuf.get_width()
        height=pixbuf.get_height()
        if height > size:
            width=width*size/height
            height=size
        pixbuf = pixbuf.scale_simple(width, height, gtk.gdk.INTERP_HYPER)
        self.icon.set_from_pixbuf(pixbuf)
        self.icon.set_size_request(width, size)
        widthL, heightL=self.label.size_request()
        self.applet.set_size_request( width+widthL+5,size)
        pass
    
    def change_background(self, applet, type, color, pixmap):
        applet.set_style(None)
        applet.modify_style(gtk.RcStyle())
        if (type == gnomeapplet.COLOR_BACKGROUND):
            applet.modify_bg(gtk.STATE_NORMAL, color)
        elif (type == gnomeapplet.PIXMAP_BACKGROUND):
            applet.get_style().bg_pixmap[gtk.STATE_NORMAL] = pixmap

    
    def cleanup(self, win):
        self.AGM.exit(None)
        self.ShowThread.stop()
        del self.applet

    def showMenu(self, widget, event, applet):
        if event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 3:
                self.create_menu(applet)
            else:
                if (self.AGM.get_hidden()):
                    self.ShowThread.set_visible()
                else:
                    self.AGM.setOnFocus()
    
    def create_menu(self, applet):
        propxml="""
                <popup name="button3">
                <menuitem name="Item 3" verb="About" label="_About" pixtype="stock" pixname="gtk-about"/>
                <menuitem name="Config" verb="Config" label="Config AGM" pixtype="stock" pixname="gtk-about"/>
                </popup>
                
                """
        verbs = [("About", self.showAboutDialog), ("Config", self.showConfigDialog)]
        self.applet.setup_menu(propxml, verbs, None)
    
    def showAboutDialog(self, *arguments, **keywords):
        from AGM.AGM_info import Info
        Info()
    
    def showConfigDialog(self, *arguments, **keywords):
        from AGM.AGM_config import Config
        Config()

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
