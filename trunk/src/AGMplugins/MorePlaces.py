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
import AGMplugins.Home
import AGMplugins.Bookmarks
import AGMplugins.LastUsedFiles
import gnomevfs, os
#    This is a AGM plugin

class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="More places plugin"
        self.description="This plugin shows your fast-access places, your home, your bookmarks and your last used files."
        self.license="GPL"
        self.is_configurable=False
        
        self.home_plugin=AGMplugins.Home.Plugin()
        self.bookmark_plugin=AGMplugins.Bookmarks.Plugin()
        self.last_used_files=AGMplugins.LastUsedFiles.Plugin()
    
    def configure(self):
        pass
    
    def get_menu(self, gointo=None):
        menu=[]
        if gointo==None:
            icon="gnome-fs-directory-accept"
            menu.append({"icon":icon,
                      "name":"Places",
                      "type":"enter",
                      "obj":"show",
                      "tooltip":"Your fast-access pc-places"})
        
        if (gointo=="show"):
            icon="user-home"
            menu.append({"icon":icon,
                      "name":"Home",
                      "type":"enter",
                      "obj":"home",
                      "other_options":[{"name":"Open", "command":["nautilus", os.path.expanduser("~")+"/"]}, 
                                       {"name":"Open as root", "command":["gksu", "'nautilus " + os.path.expanduser("~")+"/" + "'"]},
                                       {"name":"Open a terminal here", "command":["gnome-terminal", "--working-directory=" + os.path.expanduser("~")+"/"]}
                                       ], 
                      "tooltip":"Your home folder"})
                        
            icon="computer"
            menu.append({"icon":icon,
                      "name":"Computer",
                      "type":"open",
                      "obj":"computer:///",
                      "other_options":[{"name":"Open", "command":["nautilus", "/"]}, 
                                       {"name":"Open as root", "command":["gksu", "'nautilus " + "/" + "'"]},
                                       {"name":"Open a terminal here", "command":["gnome-terminal", "--working-directory=" + "/"]}
                                       ], 
                      "tooltip":"Your computer"})
            
            icon="media-optical"
            menu.append({"icon":icon,
                      "name":"Create cd/dvd",
                      "type":"exec",
                      "obj":"nautilus --no-desktop burn:///",
                      "tooltip":"Create cd/dvd"})
            
            icon="network-workgroup"
            menu.append({"icon":icon,
                      "name":"Network",
                      "type":"exec",
                      "obj":"nautilus --no-desktop network:",
                      "tooltip":"Show network"})
            
            icon="favorite"
            menu.append({"icon":icon,
                      "name":"Bookmarks",
                      "type":"enter",
                      "obj":"bookmarks",
                      "tooltip":"Your bookmarks"})
            
            menu.append({"icon":"document-open-recent",
                      "name":"Recently used files",
                      "type":"enter",
                      "obj":"last_used",
                      "tooltip":"Last files you've used"})
            
        elif (gointo=="home"):
            menu=self.home_plugin.get_menu(os.path.expanduser("~")+"/")
        elif (gointo=="bookmarks"):
            menu=self.bookmark_plugin.get_menu("show")
        elif (gointo=="last_used"):
            menu=self.last_used_files.get_menu("show")
        
        return menu