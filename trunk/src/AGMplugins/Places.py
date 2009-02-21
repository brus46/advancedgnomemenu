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
import gnomevfs, os
from AGMplugins import ConfigureBrowseFiles
from AGM import localization
_=localization.Translate
#    This is a AGM plugin

class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Place plugin"
        self.description="This plugin shows your fast-acces places"
        self.license="GPL"
        self.is_configurable=True
    
    def configure(self):
        ConfigureBrowseFiles.Configure()
    
    def get_menu(self, show=None):
        menu=[]
        if show!="show":
            icon="gnome-fs-directory-accept"
            menu.append({
                      "icon":icon,
                      "name":_("Places"),
                      "type":"enter",
                      "obj":"show",
                      "tooltip":_("Your fast-access pc-places")})
        else:
            icon="user-home"
            menu.append({
                      "icon":icon,
                      "name":_("Home folder"),
                      "type":"open",
                      "obj":os.path.expanduser("~")+ "/",
                       "other_options":[{"name":_("Open"), "command":["nautilus", os.path.expanduser("~")+"/"], "icon":"folder"}, 
                                       {"name":_("Open as root"), "command":["gksu", "'nautilus --no-desktop " + os.path.expanduser("~")+"/" + "'"], "icon":"folder"},
                                       {"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + os.path.expanduser("~")+"/"], "icon":"terminal"}
                                       ], 
                       "other_options":[{"name":_("Open"), "command":["nautilus", "/"], "icon":"folder"}, 
                                       {"name":_("Open as root"), "command":["gksu", "'nautilus " + "/" + "'"], "icon":"folder"},
                                       {"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + "/"], "icon":"terminal"}
                                       ], 
                      "tooltip":_("Home folder")})
            
            
            icon="computer"
            menu.append({
                      "icon":icon,
                      "name":_("Computer"),
                      "type":"open",
                      "obj":"computer:///",
                      "tooltip":_("Your computer")})        
            
            icon="media-optical"
            menu.append({
                      "icon":icon,
                      "name":_("Create Cd-Dvd"),
                      "type":"exec",
                      "obj":"nautilus --no-desktop burn:///",
                      "tooltip":_("Create cd")})        
            icon="network-workgroup"
            menu.append({
                      "icon":icon,
                      "name":_("Network"),
                      "type":"exec",
                      "obj":"nautilus --no-desktop network:",
                      "tooltip":_("Show network")})        
        return menu