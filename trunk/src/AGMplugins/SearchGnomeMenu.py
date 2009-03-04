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
from AGM.GnomeMenuUtils import GnomeMenu
import os, gtk, sys
#    This is a AGM plugin

class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Search in Gnome menu"
        self.description="This plugin allow to search into your gnome menu"
        self.license="GPL"
        self.is_configurable=False
        self.type=AGM_plugin.TYPE_SEARCH
        
        self.menu=[]
        self.Menu=GnomeMenu()
        pass
    
    def configure(self):
        pass
    
    def search(self, key):
        key=key.lower()
        found=self.recursive_search(key)
        return found
    
    def recursive_search(self, key, obj=None):
        found=[]
        if obj==None:
            for menu in self.Menu.get_menus():
                newfound=self.recursive_search(key, menu)
                for newel in newfound:
                    found.append(newel)
        else:
            for menu in self.Menu.get_menus(obj):
                newfound=self.recursive_search(key, menu)
                for newel in newfound:
                    found.append(newel)
            for item in self.Menu.get_items(obj):
                name = item.get_name()
                if (name.lower().find(key)>=0):
                    icon = self.getIcon(item)
                    #icon=name
                    exec_string=item.get_exec()
                    found.append({
                              "icon":icon, 
                              "name":name,
                              "type":"exec",
                              "obj":exec_string,
                              "tooltip":name})
        return found    

    def getIcon(self, item):
        pixbuf = None
        size=48
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
        #   return utils.getPixbufFromName(iconName, size)
        #else:
        #   return utils.getPixbufFromName(iconName, size, type="application")