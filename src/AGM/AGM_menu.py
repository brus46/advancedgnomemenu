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
import os, sys
from AGM.AGM_default_config import conf as config
import AGM.AGM_utils as utils
from AGM_plugin_menu import PluginMenu
from AGM import AGM_plugin
from AGM_menu_button import AGM_menu_button
import localization

_=localization.Translate

conf=config()

class Menu(gtk.ScrolledWindow):
    def __init__(self, prec_parent_change_function, hideWin, change_icon):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.icon_theme = gtk.icon_theme_get_default()
        
        self.prec_parent_change_function=prec_parent_change_function
        self.onFocusFunction=hideWin
        self.change_icon=change_icon
        
        self.menu=gtk.VBox()
        
        self.child_widgets_list=[]
        
        self.menus=[]
        self.history=[]
        self.history_icon=[]
        self.currentPlugin=None
        self.loadMenus()
        self.refresh(0)
        self.add_with_viewport(self.menu)
    
    def reload(self):
        conf.read_conf()
        self.loadMenus()
        self.refresh()
        
    def show_prec(self):
        return [self.history, self.history_icon]
    
    def refresh(self, newParent=None, searchMode=None):
        #conf.read_conf()
        
        self.prec_parent_change_function(self.show_prec())
        #self.current_parent=newParent
        
        for widget in self.child_widgets_list: self.menu.remove(widget)
        self.child_widgets_list=[]
        if searchMode==None:
            if self.currentPlugin==None:
                menu=[]
                for plugin in self.menus:
                    el=plugin.get_menu()
                    for element in el:
                        menu.append({"el":element, "plugin":plugin})
            else:
                menu=[]
                el=self.currentPlugin.get_menu(newParent)
                for element in el:
                    menu.append({"el":element, "plugin":self.currentPlugin})
        else:
            menu=searchMode
            pass
        
        #self.show_all()        
        for element in menu:
                bottone=AGM_menu_button(element, self.ItemClicked, self.onFocusFunction)
                self.child_widgets_list.append(bottone)
                self.menu.pack_start(bottone, False, True)
                bottone.show_all()
                bottone.clear_icons()

        
     
    def goToParent(self):
        #print self.history
        if len(self.history)>2:
            self.history.pop(len(self.history)-1)
            self.history_icon.pop(len(self.history_icon)-1)
            self.change_icon(self.history_icon[len(self.history_icon)-1]["icon"], self.history_icon[len(self.history_icon)-1]["name"])
            prec=self.history[len(self.history)-1]
        else:
            self.history=[]
            self.history_icon=[]
            self.change_icon(None, None)
            self.currentPlugin=None
            prec=None
        #print prec, self.history
        self.refresh(prec)
    
    def goTo(self, index):
        i=index
        where=self.history[index-1]
        while i<len(self.history):
            self.history.pop(i)
            self.history_icon.pop(i)
        self.refresh(where)
        pass
    
    def goHome(self):
        if len(self.history)!=0:
                self.currentPlugin=None
                self.history=[]
                self.history_icon=[]
                self.change_icon(None, None)
                self.refresh()
    
    def ShowMenu(self, obj, event, menu):
        if event.button==3:
            menu.popup(None, None, None, 0, 0)
            if conf.hide_on_program_launch: self.onFocusFunction()
    
    def ItemClicked(self, caller, plugin, type, obj):
       self.currentPlugin=plugin
       if "enter"==type:
           print "Go into menu->", obj
           if self.history==[]:
               self.history.append(None)
               self.history_icon.append(None)
           self.history.append(obj)
           self.history_icon.append({"icon":caller.get_image(), "name":caller.get_name()})
           self.refresh(obj)
           self.change_icon(caller.get_image(), caller.get_name())
       elif "exec"==type: 
           print "Execute->" + obj
           obj=obj.replace("%U", "")
           obj=obj.replace("%u", "")
           obj=obj.replace("%F", "")
           obj=obj.replace("%f", "")
           obj=obj.replace("\n", "")
           utils.ExecCommand(obj)
       elif "open"==type:
           print "open folder->" + obj
           command=conf.open_folder_command
           command=command.replace("%u", obj)
           command=command.replace("%U", obj)
           command=command.replace("%f", obj)
           command=command.replace("%F", obj)
           
           utils.ExecCommand(command)
           
       elif "openFile"==type:
           print "open file->" + obj
           command=conf.open_file_command
           command=command.replace("%u", obj)
           command=command.replace("%U", obj)
           command=command.replace("%f", obj)
           command=command.replace("%F", obj)
           utils.ExecCommand(command)
           
       if type!="enter":
           if conf.hide_on_program_launch: self.onFocusFunction()
       
    
    def loadMenus(self):    
        self.menus=[]
        import AGM_plugins as plugins
        plugin_avaible=plugins.get_child_plugins()
        for plugin_name in conf.menu_order:
            if plugin_name!="":
                if plugin_avaible.has_key(plugin_name):
                    Plugin = plugin_avaible.get(plugin_name)
                    print "loading: " +Plugin.name
                    self.menus.append(Plugin)
                else:
                    print "cannot find plugin: " + plugin_name

    def search(self, key):
        if key!="":
            self.history=[]
            self.history.append(None)
            self.history.append("search#"+key)
            self.history_icon=[None, {"name":_("Search"),"icon":"stock_search"}] #image_search
            self.change_icon("stock_search", _("Search"))
            found_list=[]
            for plugin in self.menus:
                if plugin.type==AGM_plugin.TYPE_SEARCH or plugin.type==AGM_plugin.TYPE_MIX:
                    found=plugin.search(key)
                    found.sort()
                    for f in found:
                        found_list.append({"el":f, "plugin":plugin})
            self.refresh(searchMode=found_list)
        else:
            self.currentPlugin=None
            self.history=[]
            self.history_icon=[]
            self.change_icon(None, None)
            self.refresh()