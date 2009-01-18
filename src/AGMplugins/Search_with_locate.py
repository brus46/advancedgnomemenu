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
        self.name="Search in your home using locate"
        self.description="This plugin allow you to search in your home directory using the search-box using LOCATE"
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
    
    def scan_folder(self, key, folder):
        import commands
        found=[]
        list_file=[]
        list_folder=[]
        foundrows=commands.getoutput("locate " + key)
        #print foundrows
        for row in foundrows.split("\n"):
            good=True
            if row.find(folder)==0:
                path=row.split("/")
                for p in path:
                    if len(p)>0 and p[0]=="." :
                        good=False
                if good:
                    if (path[len(path)-1].lower().find(key.lower())>=0):
                        if os.path.isfile(row):
                            list_file.append(row)
                        else:
                            list_folder.append(row)
        list_file.sort()
        list_folder.sort()
        
        for folder in list_folder:
            print folder
            name=folder.split("/")
            name=name[len(name)-1]
            el={
              "icon":"folder",
              "name":name,
              "type":"open",
              "obj":folder,
              "other_options":[ 
                           {"name":_("Open as root"), "command":["gksu", "nautilus --no-desktop " + (folder).replace(" ", "\ ") + ""], "icon":"folder"},
                           {"name":_("Open a terminal here"), "command":["gnome-terminal", "--working-directory=" + (folder).replace(" ", "\ ")], "icon":"terminal"}], 
              "tooltip":_("Open folder")+": " + folder}
            found.append(el)            
        
        for file in list_file:
            mime=gnomevfs.get_mime_type(file)
            mime=mime.replace("/", "-")
            name=file.split("/")
            name=name[len(name)-1]
            el={
              "icon":mime,
              "name":name,
              "type":"openFile",
              "obj":file,
              "other_options":[{"name":_("Open as root"), "command":["gksu", "gnome-open " + (file).replace(" ", "\ ") + ""], "icon":"app"}
                               ],
              "tooltip":_("Open")+": " + file}
            found.append(el)
        return found