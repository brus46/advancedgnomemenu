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
from AGMplugins import ConfigureBrowseFiles
from AGM import localization
_=localization.Translate

class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Search in home"
        self.description="This plugin allow you to search in your home directory using the search-box, with only 2 deep folders."
        self.license="GPL"
        self.type=AGM_plugin.TYPE_SEARCH
        self.is_configurable=True
        self.max_deep=2
    
    def configure(self):
        ConfigureBrowseFiles.Configure()
    
    def search(self, key):
        found=self.scan_folder(key, os.path.expanduser("~")+"/")
        return found
    
    def scan_folder(self, key, folder, deep=1):
        found=[]
        deep+=1     
        listafile=os.listdir(folder)
        listafile.sort()
        key=key.lower()
        i=0
        show_root, show_term=ConfigureBrowseFiles.read_config()
        while i<len(listafile):
            file=listafile[i]
            if (file.split(".")[0]!=""):
                if os.path.isdir(folder+file):
                    if deep<=self.max_deep:
                        newfound=self.scan_folder(key, folder+file+"/", deep)
                        for newel in newfound:
                            found.append(newel)
                    if file.lower().find(key)>=0:
                        other_options=[]
                        if show_root:
                            other_options.append({"name":_("Open as root"), "command":["gksu", "nautilus --no-desktop " + (folder+file).replace(" ", "\ ") + ""], "icon":"folder"})
                        if show_term:
                            other_options.append({"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + (folder+file).replace(" ", "\ ")], "icon":"terminal"})
                        el={
                          "icon":"folder",
                          "name":file,
                          "type":"open",
                          "obj":folder+file,
                          "other_options":other_options, 
                          "tooltip":_("Open folder")+": " + folder+file}
                        found.append(el)
                        listafile.remove(file)
                    else:
                        listafile.remove(file)
                elif file.lower().find(key)<0:
                    listafile.remove(file)
                else: i+=1
            else: listafile.remove(file)
                        

        for file in listafile:
            mime=gnomevfs.get_mime_type(folder+file)
            mime=mime.replace("/", "-")
            show_options=[]
            if show_root:
                show_options.append({"name":_("Open as root"), "command":["gksu", "gnome-open " + (folder+file).replace(" ", "\ ") + ""], "icon":"app"})
            el={
              "icon":mime,
              "name":file,
              "type":"openFile",
              "obj":folder+file,
              "other_options":other_options,
              "tooltip":_("Open")+": " + folder+file}
            found.append(el)
        return found