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

import AGM.AGM_utils as utils
from AGM.AGM_plugin import AGM_plugin as plugin
import gnomevfs, os
#    This is a AGM plugin

class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Place plugin"
        self.description="This plugin shows your fast-acces places"
        self.license="GPL"
        self.is_configurable=False
    
    def configure(self):
        pass
    
    def get_menu(self, show=None):
        menu=[]
        if show!="show":
            icon=utils.getPixbufFromName("gnome-fs-directory-accept")
            menu.append({
                      "icon":icon,
                      "name":"Places",
                      "type":"enter",
                      "obj":"show",
                      "tooltip":"Your fast-access pc-places"})
        else:
            icon=utils.getPixbufFromName("user-home")
            menu.append({
                      "icon":icon,
                      "name":"Home folder",
                      "type":"open",
                      "obj":os.path.expanduser("~")+ "/",
                       "other_options":[{"name":"Open", "command":["nautilus", os.path.expanduser("~")+"/"]}, 
                                       {"name":"Open as root", "command":["gksu", "'nautilus " + os.path.expanduser("~")+"/" + "'"]},
                                       {"name":"Open a terminal here", "command":["gnome-terminal", "--working-directory=" + os.path.expanduser("~")+"/"]}
                                       ], 
                       "other_options":[{"name":"Open", "command":["nautilus", "/"]}, 
                                       {"name":"Open as root", "command":["gksu", "'nautilus " + "/" + "'"]},
                                       {"name":"Open a terminal here", "command":["gnome-terminal", "--working-directory=" + "/"]}
                                       ], 
                      "tooltip":"Home folder"})
            
            
            icon=utils.getPixbufFromName("computer")
            menu.append({
                      "icon":icon,
                      "name":"Computer",
                      "type":"open",
                      "obj":"/",
                      "tooltip":"Your computer"})        
            
            icon=utils.getPixbufFromName("media-optical")
            menu.append({
                      "icon":icon,
                      "name":"Create Cd-Dvd",
                      "type":"exec",
                      "obj":"nautilus --no-desktop burn:///",
                      "tooltip":"Create cd"})        
            icon=utils.getPixbufFromName("network-workgroup")
            menu.append({
                      "icon":icon,
                      "name":"Network",
                      "type":"exec",
                      "obj":"nautilus --no-desktop network:",
                      "tooltip":"Show network"})        
        return menu