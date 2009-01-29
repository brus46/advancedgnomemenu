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
        self.name="Browse bookmarks plugin"
        self.description="This plugin shows your bookmarks"
        self.license="GPL"
        self.is_configurable=False
        pass
    
    def configure(self):
        pass
    
    def get_menu(self, show=None):
        menu=[]
        file=open(os.path.expanduser("~")+ "/" + ".gtk-bookmarks")
        file=file.readlines()  
        print show
        if (show==None):
            menu.append({
                  "icon":"emblem-favorite",
                  "name":_("Bookmarks"),
                  "type":"enter",
                  "obj":"show",
                  "tooltip":_("Browse your bookmarks")})            
        elif (show=="show"):
            icon="gnome-fs-directory-accept"
            for line in file:    
                line=line.replace("file://", "")
                line=line.replace("\n", "")
                path=line.split("/")
                filename=path[len(path)-1].replace("\n", "")
                name=filename.split(" ")[0]
                line=""
                for piece in path:
                    if (piece.replace("\n", "")==filename):
                        line+=name
                    else:
                        line+=piece+"/"
                menu.append({
                  "icon":icon,
                  "name":name,
                  "type":"enter",
                  "obj":line,
                  "other_options":[{"name":_("Open"), "command":["nautilus", line], "icon":"folder"}, 
                                   {"name":_("Open as root"), "command":["gksu", "nautilus --no-desktop " + line.replace(" ", "\ ") + ""], "icon":"folder"},
                                   {"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + line.replace(" ", "\ ")], "icon":"terminal"}
                                   ],
                  "tooltip":_("Open") +" " + filename})            
        else:
            
            folder=show+"/"
            print folder
            listafile=os.listdir(folder)
            listafile.sort()
            i=0
            while i<len(listafile):
                file=listafile[i]
                if (file.split(".")[0]!=""):
                    if os.path.isdir(folder+file):
                        current_folder=folder+file
                        el={
                          "icon":"folder",
                          "name":file,
                          "type":"enter",
                          "obj":current_folder,
                          "other_options":[{"name":_("Open"), "command":["nautilus", current_folder], "icon":"folder"}, 
                                       {"name":_("Open as root"), "command":["gksu", "nautilus --no-desktop " + current_folder.replace(" ", "\ ") + ""], "icon":"folder"},
                                       {"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + current_folder.replace(" ", "\ ")], "icon":"terminal"}
                                       ],
                          "tooltip":_("Open folder")+": " + file}
                        menu.append(el)
                        listafile.remove(file)
                    else: i+=1
                else: listafile.remove(file)
            for file in listafile:
                mime=gnomevfs.get_mime_type(folder+file)
                mime=mime.replace("/", "-")
                current_file=folder+file
                el={
                  "icon":mime,
                  "name":file,
                  "type":"openFile",
                  "obj":current_file,
                  "other_options":[{"name":_("Open as root"), "command":["gksu", "gnome-open " + current_file.replace(" ", "\ ") + ""], "icon":"app"}],
                  "tooltip":_("Open")+": " + file}
                menu.append(el)
        
        return menu