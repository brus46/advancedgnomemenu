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
from AGM import localization
_=localization.Translate
#    This is a AGM plugin

class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Home plugin"
        self.description="This plugin shows your home dir"
        self.license="GPL"
        self.is_configurable=False
    
    def configure(self):
        pass
    
    def get_menu(self, folder=None):
        menu=[]
        if folder==None:
            menu.append({
                      "icon":"user-home",
                      "name":_("Home"),
                      "type":"enter",
                      "obj":os.path.expanduser("~")+"/",
                      "other_options":[{"name":_("Open"), "command":["nautilus", os.path.expanduser("~")+"/"]}, 
                                       {"name":_("Open as root"), "command":["gksu", "nautilus --no-desktop " + (os.path.expanduser("~")+"/").replace(" ", "\ ") + ""]},
                                       {"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + (os.path.expanduser("~")+"/").replace(" ", "\ ")]}
                                       ], 
                      "tooltip":_("Browse your home")})
        else:
            listafile=os.listdir(folder)
            listafile.sort()
            
            for file in listafile:
                if gnomevfs.get_mime_type(folder+file).split("/")[0]=="x-directory":
                    if (file.split(".")[0]!=""):
                        el={
                          "icon":"folder",
                          "name":file,
                          "type":"open",
                          "obj":folder+file,
                          "other_options":[{"name":_("Open"), "command":["nautilus", folder+file]}, 
                                       {"name":_("Open as root"), "command":["gksu", "nautilus --no-desktop " + (folder+file).replace(" ", "\ ") + ""]},
                                       {"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + (folder+file).replace(" ", "\ ")]}
                                       ], 
                          "tooltip":_("Open folder")+": " + folder+file}
                        menu.append(el)
                elif gnomevfs.get_mime_type(folder+file).split("/")[0]!="x-directory":
                    if (file.split(".")[0]!=""):
                        mime=gnomevfs.get_mime_type(folder+file)
                        mime=mime.replace("/", "-")
                        el={
                          "icon":mime,
                          "name":file,
                          "type":"openFile",
                          "obj":folder+file,
                          "other_options":[{"name":_("Open folder"), "command":["nautilus", folder]},
                                       {"name":_("Open folder as root"), "command":["gksu", "nautilus --no-desktop " + (folder).replace(" ", "\ ") + ""]},
                                       {"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + folder.replace(" ", "\ ")]},
                                       {"name":_("Open as root"), "command":["gksu", "gnome-open " + (folder+file).replace(" ", "\ ") + ""]}
                                       ],
                          "tooltip":_("Open")+": " + folder+file}
                        menu.append(el)
                    
        return menu