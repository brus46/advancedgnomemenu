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

from AGM.AGM_plugin import AGM_plugin as plugin
from AGM import AGM_plugin
from Alacarte.MenuEditor import MenuEditor
import os, gtk, gmenu, cgi, sys
#    This is a AGM plugin

class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Gnome menu plugin"
        self.description="This plugin shows your gnome menu"
        self.license="GPL"
        self.is_configurable=True
        self.type=AGM_plugin.TYPE_MENU
        
        self.menu=[]
        self.editor=MenuEditor()
        pass
    
    def configure(self):
        if (os.fork()==0):
            os.execvp("alacarte", ["alacarte"])
            sys.exit(-1)
        
    def get_menu(self, obj=None):
        self.menu=[]
        if obj==None:
            #print "Main menu"
            for menu in self.editor.getMenus():
                self.loadMenu(menu, 0)
        else:
            #print "Loading sub menu"
            self.loadMenu(obj, 1)
        return self.menu
    
    def loadMenu(self, parent, depth):
        if depth == 0:
            #print "depth", depth
            icon=self.getIcon(parent)
            #icon=parent.get_name()
            self.menu.append({
                              "icon":icon, 
                              "name":parent.get_name(),
                              "type":"enter",
                              "obj":parent,
                              "tooltip":parent.get_name()})
                    
                   
        if depth>0:
            for menu, show in self.editor.getMenus(parent):
                if show:
                    name = menu.get_name()
                    icon = self.getIcon(menu)
                    #icon=name
                    self.menu.append({
                      "icon":icon, 
                      "name":name,
                      "type":"enter",
                      "obj":menu,
                      "tooltip":name})
                        
            for item, show in self.editor.getItems(parent):
                if show and item.get_type() == gmenu.TYPE_ENTRY:
                    name = item.get_name()
                    icon = self.getIcon(item)
                    #icon=name
                    exec_string=item.get_exec()
                    self.menu.append({
                              "icon":icon, 
                              "name":name,
                              "type":"exec",
                              "obj":exec_string,
                              "tooltip":name})

    

    def getIcon(self, item):
        pixbuf = None
        if item == None:
            return None
        if isinstance(item, str):
            iconName = item
        else:
            iconName = item.get_icon()
        if iconName and not '/' in iconName and iconName[-3:] in ('png', 'svg', 'xpm'):
            iconName = iconName[:-4]
        icon_theme = gtk.icon_theme_get_default()
        return iconName
        #if item.get_type() == gmenu.TYPE_DIRECTORY:
           #return utils.getPixbufFromName(iconName)
        #else:
           #return utils.getPixbufFromName(iconName, type="application")