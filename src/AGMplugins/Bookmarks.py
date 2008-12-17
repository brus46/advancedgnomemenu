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
from AGM import AGM_plugin
import os
#    This is a AGM plugin

class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Bookmarks plugin"
        self.description="This plugin shows your bookmarks and allow you to browse into them."
        self.license="GPL"
        self.type=AGM_plugin.TYPE_MENU
        self.is_configurable=False
        pass
    
    def configure(self):
        pass
    
    def get_menu(self, show=None):
        menu=[]
        try:
            file=open(os.path.expanduser("~")+ "/" + ".gtk-bookmarks")
            file=file.readlines()  
            print show
            if (show!="show"):
                menu.append({
                      "icon":utils.getPixbufFromName("emblem-favorite"),
                      "name":"Bookmarks",
                      "type":"enter",
                      "obj":"show",
                      "tooltip":"Browse your bookmarks"})            
            else:
                icon=utils.getPixbufFromName("gnome-fs-directory-accept")
                for line in file:    
                    path=line.split("/")
                    line=line.replace("file://", "")
                    line=line.replace("\n", "")
                    filename=path[len(path)-1].replace("\n", "")
                    name=filename.split(" ")[0]
                    line=""
                    for piece in path:
                        if (piece.replace("\n", "")==filename):
                            line+=name
                        else:
                            line+=piece
                    menu.append({
                      "icon":icon,
                      "name":name,
                      "type":"open",
                      "obj":line,
                      "other_options":[{"name":"Open", "command":["nautilus", line]}, 
                                       {"name":"Open as root", "command":["gksu", "'nautilus " + (line).replace(" ", "\ ") + "'"]},
                                       {"name":"Open a terminal here", "command":["gnome-terminal", "--working-directory=" + (line).replace(" ", "\ ")]}
                                       ], 
                      "tooltip":"Open " + line})            
                
        except: 
            print "error"
        
        return menu