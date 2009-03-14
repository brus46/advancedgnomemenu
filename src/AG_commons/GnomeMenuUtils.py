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

import os, re, xml.dom.minidom, locale, gtk, gmenu

class Menu:
    tree = None
    visible_tree = None
    path = None
    dom = None

class GnomeMenu:
    def __init__(self):
        self.__loadMenus()
    
    def get_apps(self):
        return self.get_menus(self.applications.tree.root)
    
    def get_menus(self, parent=None):
        if parent == None:
            yield self.applications.tree.root
            yield self.settings.tree.root
        else:
            for menu in parent.get_contents():
                if menu.get_type() == gmenu.TYPE_DIRECTORY:
                    yield menu
    
    def get_items(self, menu):
        for item in menu.get_contents():
            if item.get_type() != gmenu.TYPE_SEPARATOR:
                if item.get_type() == gmenu.TYPE_ENTRY and item.get_desktop_file_id()[-19:] == '-usercustom.desktop':
                    continue
                if item.get_type() == gmenu.TYPE_ENTRY:
                    yield (item)
            
    def __loadMenus(self):
        self.applications = Menu()
        self.applications.tree = gmenu.lookup_tree('applications.menu')
        self.applications.visible_tree = gmenu.lookup_tree('applications.menu')
        self.applications.path = os.path.join(self.getUserMenuPath(), self.applications.tree.get_menu_file())
        if not os.path.isfile(self.applications.path):
            self.applications.dom = xml.dom.minidom.parseString(self.getUserMenuXml(self.applications.tree))
        else:
            self.applications.dom = xml.dom.minidom.parse(self.applications.path)

        self.settings = Menu()      
        self.settings.tree = gmenu.lookup_tree('settings.menu')     
        self.settings.visible_tree = gmenu.lookup_tree('settings.menu')      
        self.settings.path = os.path.join(self.getUserMenuPath(), self.settings.tree.get_menu_file())      
        if not os.path.isfile(self.settings.path):      
            self.settings.dom = xml.dom.minidom.parseString(self.getUserMenuXml(self.settings.tree))      
        else:      
            self.settings.dom = xml.dom.minidom.parse(self.settings.path)
    
    def getUserMenuPath(self):
        menu_dir = None
        if os.environ.has_key('XDG_CONFIG_HOME'):
            menu_dir = os.path.join(os.environ['XDG_CONFIG_HOME'], 'menus')
        else:
            menu_dir = os.path.join(os.environ['HOME'], '.config', 'menus')
        #move .config out of the way if it's not a dir, it shouldn't be there
        if os.path.isfile(os.path.split(menu_dir)[0]):
            os.rename(os.path.split(menu_dir)[0], os.path.split(menu_dir)[0] + '.old')
        if not os.path.isdir(menu_dir):
            os.makedirs(menu_dir)
        return menu_dir
    
    def getSystemMenuPath(self, file_name):
        if os.environ.has_key('XDG_CONFIG_DIRS'):
            for system_path in os.environ['XDG_CONFIG_DIRS'].split(':'):
                file_path = os.path.join(system_path, 'menus', file_name)
                if os.path.isfile(file_path):
                    return file_path
        file_path = os.path.join('/', 'etc', 'xdg', 'menus', file_name)
        if os.path.isfile(file_path):
            return file_path
        return False
    
    def getUserMenuXml(self, tree):
        system_file = self.getSystemMenuPath(tree.get_menu_file())
        name = tree.root.get_menu_id()
        menu_xml = "<!DOCTYPE Menu PUBLIC '-//freedesktop//DTD Menu 1.0//EN' 'http://standards.freedesktop.org/menu-spec/menu-1.0.dtd'>\n"
        menu_xml += "<Menu>\n  <Name>" + name + "</Name>\n  "
        menu_xml += "<MergeFile type=\"parent\">" + system_file +    "</MergeFile>\n</Menu>\n"
        return menu_xml
    
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