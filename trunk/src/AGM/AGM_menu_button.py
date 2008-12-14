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

from AGM.AGM_default_config import conf as config
import AGM.AGM_utils as utils
conf=config()

class AGM_menu_button(gtk.EventBox):
    def __init__(self, element, ItemClicked):
        gtk.EventBox.__init__(self)
        conf.read_conf()
        self.element=element
        element=element["el"]
        self.ItemClicked=ItemClicked
        self.button_size=32
        self.container=gtk.HBox()
        self.layout=gtk.HBox(spacing=5)
        self.layoutL=gtk.VBox()
        self.layoutR=gtk.VBox()
        self.row1=gtk.HBox()
        self.row2=gtk.HBox()
        self.layoutR.pack_start(self.row1, False)
        self.layoutR.pack_end(self.row2, False)
                
        h=conf.menu_icon_size+20
        if h<self.button_size*2:
            h=self.button_size*2
        self.set_size_request(-1, h)
        width, height=self.size_request()
        
        self.icon=gtk.Image()
        self.icon.set_from_pixbuf(element["icon"])
        self.label=gtk.Label(element["name"])
        
        self.label.set_size_request(150, -1)
        
        self.menu_list=[]
        if (element.has_key("other_options")):
            for el in element["other_options"]:
                self.menu_list.append(el)
        
        self.buttons=[gtk.Button(), gtk.Button(), gtk.Button(), gtk.Button()]
        self.images=[gtk.Image(), gtk.Image(), gtk.Image(), gtk.Image()]
        
        #Button positionating
        if len(self.menu_list)>=1:
            self.configure_button(0)
            self.row1.pack_start(self.buttons[0], False)
        if len(self.menu_list)>=3:
            self.configure_button(2)
            self.row1.pack_start(self.buttons[2], False)
        LSpacing=gtk.Label()
        LSpacing.set_size_request(self.button_size, -1)
        #self.layoutL.pack_start(LSpacing)
        
        if len(self.menu_list)>=2:
            self.configure_button(1)
            self.row2.pack_start(self.buttons[1], False)
        if len(self.menu_list)>=4:
            self.configure_button(3)
            self.row2.pack_start(self.buttons[3], False)
        RSpacing=gtk.Label()
        RSpacing.set_size_request(self.button_size, -1)
        #self.layoutR.pack_start(RSpacing)
        
        self.layout.set_border_width(5)
        self.layout.pack_start(self.icon, False)
        self.layout.pack_start(self.label, False)
        
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.bgcolor))
        self.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor)) 
        self.set_tooltip_text(element["tooltip"])
        
        #self.container.pack_start(self.layoutL, False)
        self.container.pack_start(self.layout)
        self.container.pack_end(self.layoutR, False)
        self.add(self.container)
        
        self.connect("button_press_event", self.clicked)
        
        self.connect("enter_notify_event", self.activate_event)
        self.connect("leave_notify_event", self.leave_event)
    
    def configure_button(self, index):
        name=self.menu_list[index]["name"]
        command=self.menu_list[index]["command"]
        if self.menu_list[index].has_key("icon"): 
            icon=self.menu_list[index]["icon"]
        else: icon=None
        
        self.images[index].set_from_pixbuf(utils.getPixbufFromName(icon, self.button_size-15, "app"))
        self.buttons[index].set_image(self.images[index])
        
        self.buttons[index].set_tooltip_text(name)
        self.buttons[index].set_size_request(self.button_size, self.button_size)
        self.buttons[index].connect("button_press_event", self.clicked, command)
        self.buttons[index].connect("enter_notify_event", self.activate_event, name, icon)
    
    def clear_icons(self):
        for i in range(0,4):
            self.images[i].hide()
            self.buttons[i].set_relief(gtk.RELIEF_NONE)
    
    def put_icons(self):
        for i in range(0,4):
            self.images[i].show()
            self.buttons[i].set_relief(gtk.RELIEF_NORMAL)

    def modify_bg(self, state, color):
        gtk.EventBox.modify_bg(self, state, color)
        self.layout.modify_bg(state, color)
        for button in self.buttons:
            self.color(button)
                    
    def modify_fg(self, state, color):
        self.label.modify_fg(state, color)
    
    def clicked(self, button, event, command=None):
        if event.button == 1:
            if command==None:
                self.ItemClicked(button, self.element["plugin"], self.element["el"]["type"], self.element["el"]["obj"])
            else: 
                if (os.fork()==0):
                    os.execvp(command[0], command)
                    sys.exit(-1)
    
    def color(self, obj):
        try:
            obj.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.bgcolor))
            obj.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse(conf.activebgcolor))
            obj.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse(conf.selectedbgcolor))
        except: pass
        try:
            obj.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor))
            obj.get_child().modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse(conf.activefgcolor))
            obj.get_child().modify_fg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse(conf.selectedfgcolor))
        except: pass
        try:
            obj.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor))
            obj.modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse(conf.activefgcolor))
            obj.modify_fg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse(conf.selectedfgcolor))
        except: pass
    
    def activate_event(self, obj, event, text="", icon=None):
        if text=="":
            self.label.set_text(self.element["el"]["name"])
        else:
            self.label.set_text(text)

        if icon!=None:
            self.icon.set_from_pixbuf(utils.getPixbufFromName(icon, conf.menu_icon_size, "app"))
        else:
            self.icon.set_from_pixbuf(self.element["el"]["icon"])
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.selectedbgcolor))
        self.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.selectedfgcolor))
        self.put_icons()

    def leave_event(self, obj, event):        
        self.label.set_text(self.element["el"]["name"])
        self.icon.set_from_pixbuf(self.element["el"]["icon"])
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.bgcolor))
        self.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor))
        self.clear_icons()
