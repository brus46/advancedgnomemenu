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
import AGM.AGM_utils as utils
import gnomevfs, os
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
        #try:
        if 1:
            file=open(os.path.expanduser("~")+ "/" + ".gtk-bookmarks")
            file=file.readlines()  
            print show
            if (show==None):
                menu.append({
                      "icon":utils.getPixbufFromName("emblem-favorite"),
                      "name":"Bookmarks",
                      "type":"enter",
                      "obj":"show",
                      "tooltip":"Browse your bookmarks"})            
            elif (show=="show"):
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
                      "type":"enter",
                      "obj":line,
                      "other_options":[{"name":"Open", "command":["nautilus", line]}, 
                                       {"name":"Open as root", "command":["gksu", "'nautilus " + line.replace(" ", "\ ") + "'"]},
                                       {"name":"Open a terminal here", "command":["gnome-terminal", "--working-directory=" + line.replace(" ", "\ ")]}
                                       ],
                      "tooltip":"Open " + filename})            
            else:
                
                folder=show+"/"
                print folder
                listafile=os.listdir(folder)
                listafile.sort()
                for file in listafile:
                    if gnomevfs.get_mime_type(folder+file).split("/")[0]=="x-directory":
                        if (file.split(".")[0]!=""):
                            current_folder=folder+file
                            el={
                              "icon":utils.getPixbufFromName(""),
                              "name":file,
                              "type":"enter",
                              "obj":current_folder,
                              "other_options":[{"name":"Open", "command":["nautilus", current_folder]}, 
                                           {"name":"Open as root", "command":["gksu", "'nautilus " + current_folder.replace(" ", "\ ") + "'"]},
                                           {"name":"Open a terminal here", "command":["gnome-terminal", "--working-directory=" + current_folder.replace(" ", "\ ")]}
                                           ],
                              "tooltip":"Open folder: " + file}
                            menu.append(el)
        
                for file in listafile:
                    if gnomevfs.get_mime_type(folder+file).split("/")[0]!="x-directory":
                        if (file.split(".")[0]!=""):
                            mime=gnomevfs.get_mime_type(folder+file)
                            mime=mime.replace("/", "-")
                            current_file=folder+file
                            el={
                              "icon":utils.getPixbufFromName(mime, type="file"),
                              "name":file,
                              "type":"openFile",
                              "obj":current_file,
                              "other_options":[{"name":"Open folder", "command":["nautilus", folder]},
                                               {"name":"Open folder as root", "command":["gksu", "'nautilus " + folder.replace(" ", "\ ") + "'"]},
                                               {"name":"Open a terminal here", "command":["gnome-terminal", "--working-directory=" + folder.replace(" ", "\ ")]},
                                               {"name":"Open as root", "command":["gksu", "'gnome-open " + current_file.replace(" ", "\ ") + "'"]}
                                               ],
                              "tooltip":"Open: " + file}
                            menu.append(el)
        #except: 
        #    print "error"
        
        return menu