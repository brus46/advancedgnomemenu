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
import gnomevfs, os
from AGM import localization
_=localization.Translate

class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Search in home"
        self.description="This plugin allow you to search in your home directory using the search-box"
        self.license="GPL"
        self.type=AGM_plugin.TYPE_SEARCH
        self.is_configurable=False
        self.max_deep=2
    
    def configure(self):
        #get deep
        
        pass
    
    def search(self, key):
        found=self.scan_folder(key, os.path.expanduser("~")+"/")
        return found
    
    def scan_folder(self, key, folder, deep=1):
        found=[]
        deep+=1     
        listafile=os.listdir(folder)
        listafile.sort()
        key=key.lower()
        for file in listafile:
            if os.path.isdir(folder+file):
                if (file.split(".")[0]!=""):
                    if deep<=self.max_deep:
                        newfound=self.scan_folder(key, folder+file+"/", deep)
                        for newel in newfound:
                            found.append(newel)
                    if file.lower().find(key)>=0:                            
                        el={
                          "icon":"folder",
                          "name":file,
                          "type":"open",
                          "obj":folder+file,
                          "other_options":[ 
                                       {"name":_("Open as root"), "command":["gksu", "nautilus --no-desktop " + (folder+file).replace(" ", "\ ") + ""], "icon":"folder"},
                                       {"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + (folder+file).replace(" ", "\ ")], "icon":"terminal"}
                                       ], 
                          "tooltip":_("Open folder")+": " + folder+file}
                        found.append(el)

        for file in listafile:
            if os.path.isdir(folder+file)==False:
                if (file.split(".")[0]!="") and file.lower().find(key)>=0:
                    mime=gnomevfs.get_mime_type(folder+file)
                    mime=mime.replace("/", "-")
                    el={
                      "icon":mime,
                      "name":file,
                      "type":"openFile",
                      "obj":folder+file,
                      "other_options":[{"name":_("Open folder"), "command":["nautilus", folder], "icon":"folder"},
                                       {"name":_("Open folder as root"), "command":["gksu", "nautilus --no-desktop " + (folder).replace(" ", "\ ") + ""], "icon":"folder"},
                                       {"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + folder.replace(" ", "\ ")], "icon":"terminal"},
                                       {"name":_("Open as root"), "command":["gksu", "gnome-open " + (folder+file).replace(" ", "\ ") + ""], "icon":"app"}
                                       ],
                      "tooltip":_("Open")+": " + folder+file}
                    found.append(el)
        return found