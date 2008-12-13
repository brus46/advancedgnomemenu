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
conf=config()

class AGM_menu_button(gtk.EventBox):
    def __init__(self, element, ItemClicked):
        gtk.EventBox.__init__(self)
        self.element=element
        element=element["el"]
        self.ItemClicked=ItemClicked
        self.button_size=22
        self.container=gtk.HBox()
        self.layout=gtk.HBox(spacing=5)
        self.layoutL=gtk.VBox()
        self.layoutR=gtk.VBox()
        
        self.set_size_request(-1, conf.menu_icon_size+20)
        width, height=self.size_request()
        
        self.icon=gtk.Image()
        self.icon.set_from_pixbuf(element["icon"])
        self.label=gtk.Label(element["name"])
        
        self.label.set_size_request(150, -1)
        
        self.menu_list=[]
        if (element.has_key("other_options")):
            for el in element["other_options"]:
                if el.has_key("icon"):
                    self.menu_list.append([el["name"], el["command"], el["icon"]])
                else: self.menu_list.append([el["name"], el["command"], None])
        
        self.button1=gtk.Button()
        self.button2=gtk.Button()
        self.button3=gtk.Button()
        self.button4=gtk.Button()
        
        #Button positionating
        if len(self.menu_list)>=1:
            self.button1.set_tooltip_text(self.menu_list[0][0])
            self.layoutL.pack_start(self.button1, False)
            self.button1.set_size_request(self.button_size, self.button_size)
            self.button1.connect("button_press_event", self.clicked, self.menu_list[0][1])
            self.button1.connect("enter_notify_event", self.activate_event, self.menu_list[0][0])
        if len(self.menu_list)>=3:
            self.button3.set_tooltip_text(self.menu_list[2][0])
            self.layoutL.pack_end(self.button3, False)
            self.button3.set_size_request(self.button_size, self.button_size)
            self.button3.connect("button_press_event", self.clicked, self.menu_list[2][1])
            self.button3.connect("enter_notify_event", self.activate_event, self.menu_list[2][0])
        LSpacing=gtk.Label()
        LSpacing.set_size_request(self.button_size, -1)
        self.layoutL.pack_start(LSpacing)
        
        if len(self.menu_list)>=2:
            self.button2.set_tooltip_text(self.menu_list[1][0])
            self.layoutR.pack_start(self.button2, False)
            self.button2.set_size_request(self.button_size, self.button_size)
            self.button2.connect("button_press_event", self.clicked, self.menu_list[1][1])
            self.button2.connect("enter_notify_event", self.activate_event, self.menu_list[1][0])
        if len(self.menu_list)>=4:
            self.button4.set_tooltip_text(self.menu_list[3][0])
            self.layoutR.pack_end(self.button4, False)
            self.button4.set_size_request(self.button_size, self.button_size)
            self.button4.connect("button_press_event", self.clicked, self.menu_list[3][1])
            self.button4.connect("enter_notify_event", self.activate_event, self.menu_list[3][0])
        RSpacing=gtk.Label()
        RSpacing.set_size_request(self.button_size, -1)
        self.layoutR.pack_start(RSpacing)
        
        self.layout.pack_start(self.icon, False)
        self.layout.pack_start(self.label, False)
        
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.bgcolor))
        self.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor)) 
        self.set_tooltip_text(element["tooltip"])
        
        self.container.pack_start(self.layoutL, False)
        self.container.pack_start(self.layout)
        self.container.pack_end(self.layoutR, False)
        self.add(self.container)
        
        self.connect("button_press_event", self.clicked)
        
        self.connect("enter_notify_event", self.activate_event)
        self.connect("leave_notify_event", self.leave_event)
    
    def modify_bg(self, state, color):
        gtk.EventBox.modify_bg(self, state, color)
        self.layout.modify_bg(state, color)
        self.color(self.button1)
        self.color(self.button2)
        self.color(self.button3)
        self.color(self.button4)
        
    def modify_fg(self, state, color):
        self.label.modify_fg(state, color)
    
    def clicked(self, button, event, command=None):
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
    
    def activate_event(self, obj, event, text=""):
        if text=="":
            self.label.set_text(self.element["el"]["name"])
            self.icon.set_from_pixbuf(self.element["el"]["icon"])
        else:
            self.label.set_text(text)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.selectedbgcolor))
        self.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.selectedfgcolor))

    def leave_event(self, obj, event):
        self.label.set_text(self.element["el"]["name"])
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.bgcolor))
        self.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor))