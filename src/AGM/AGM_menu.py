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
        return self.history!=[]
    
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
            self.change_icon(self.history_icon[len(self.history_icon)-1])
            prec=self.history[len(self.history)-1]
        else:
            self.history=[]
            self.history_icon=[]
            self.change_icon()
            self.currentPlugin=None
            prec=None
        #print prec, self.history
        self.refresh(prec)
    
    def goHome(self):
        self.currentPlugin=None
        self.history=[]
        self.history_icon=[]
        self.change_icon()
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
           self.history_icon.append(caller.get_image())
           self.refresh(obj)
           self.change_icon(caller.get_image())
       elif "exec"==type: 
           print "Execute->" + obj
           obj=obj.replace("%U", "")
           obj=obj.replace("%u", "")
           if os.fork()==0:
               obj=obj.replace("\n", "")
               command=obj.split(" ")
               try:
                   os.chdir(os.path.expanduser("~"))
                   os.execvp(command[0], command)
               except: print "Command fail: " + str(command)
               sys.exit(-1)
       elif "open"==type:
           print "open folder->" + obj
           if (os.fork()):
               command=conf.open_folder_command.split(" ")
               mycommand=[]
               for cmd in command:
                   cmd=cmd.replace("%u", obj)
                   cmd=cmd.replace("%U", obj)
                   mycommand.append(cmd)
               #print mycommand
               os.execvp(mycommand[0], mycommand)
               sys.exit(-1)
       elif "openFile"==type:
           print "open file->" + obj
           if (os.fork()):
               command=conf.open_file_command.split(" ")
               mycommand=[]
               for cmd in command:
                   if cmd.find("%U")>=0 or cmd.find("%u")>=0:
                       cmd=cmd.replace("%u", obj)
                       cmd=cmd.replace("%U", obj)
                   mycommand.append(cmd)
               os.execvp(mycommand[0], mycommand)
               sys.exit(-1)
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
            self.history_icon=[None, "stock_search"] #image_search
            self.change_icon("stock_search")
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
            self.change_icon()
            self.refresh()