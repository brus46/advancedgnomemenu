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
        self.name="Browse files plugin"
        self.description="This plugin shows your home dir"
        self.license="GPL"
        self.is_configurable=True
    
    def configure(self):
        ConfigureBrowseFiles.Configure()
    
    def get_menu(self, folder=None):
        menu=[]
        show_root, show_term=ConfigureBrowseFiles.read_config()
        if folder==None:
            folder=os.path.expanduser("~")
            other_options=[{"name":_("Open folder"), "command":["nautilus", folder], "icon":"folder"}]
            if show_root:
               other_options.append({"name":_("Open folder as root"), "command":["gksu", "nautilus --no-desktop " + folder.replace(" ", "\ ") + ""], "icon":"folder"})
            if show_term:
               other_options.append({"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + folder.replace(" ", "\ ")], "icon":"terminal"})
                           
            menu.append({
                      "icon":"user-home",
                      "name":_("Home"),
                      "type":"enter",
                      "obj":folder,
                      "other_options":other_options, 
                      "tooltip":_("Browse your home")})
        else:
            folder+="/"
            listafile=os.listdir(folder)
            listafile.sort()
            i=0
            while i<len(listafile):
                file=listafile[i]
                i+=1
                if (file.split(".")[0]!=""):
                    if os.path.isdir(folder+file):
                        current_folder=folder+file
                        other_options=[{"name":_("Open folder"), "command":["nautilus", current_folder], "icon":"folder"}]
                        if show_root:
                           other_options.append({"name":_("Open folder as root"), "command":["gksu", "nautilus --no-desktop " + current_folder.replace(" ", "\ ") + ""], "icon":"folder"})
                        if show_term:
                           other_options.append({"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + current_folder.replace(" ", "\ ")], "icon":"terminal"})
                                      
                        el={
                          "icon":"folder",
                          "name":file,
                          "type":"enter",
                          "obj":current_folder,
                          "other_options":other_options,
                          "tooltip":_("Open folder")+": " + file}
                        menu.append(el)
                        listafile.remove(file)
                        i-=1
                else:
                    listafile.remove(file)
                    i-=1
              
            for file in listafile:
                mime=gnomevfs.get_mime_type(folder+file)
                mime=mime.replace("/", "-")
                current_file=folder+file
                other_options=[]
                if show_root:
                   other_options.append({"name":_("Open as root"), "command":["gksu", "gnome-open " + current_folder.replace(" ", "\ ") + ""], "icon":"folder"})
                        
                el={
                  "icon":mime,
                  "name":file,
                  "type":"openFile",
                  "obj":current_file,
                  "other_options":other_options,
                  "tooltip":_("Open")+": " + file}
                menu.append(el)
        return menu