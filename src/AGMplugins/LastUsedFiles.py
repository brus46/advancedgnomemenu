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
import xml.dom.minidom
from AGMplugins import ConfigureBrowseFiles
from AGM import localization
_=localization.Translate
#    This is a AGM plugin

class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Recently used files plugin"
        self.description="This plugin shows your last-used files"
        self.license="GPL"
        self.is_configurable=True
    
    def configure(self):
        ConfigureBrowseFiles.Configure()
    
    def get_menu(self, show=None):
        menu=[]
        if show!="show":
            menu.append({
                      "icon":"document-open-recent",
                      "name":_("Recently used files"),
                      "type":"enter",
                      "obj":"show",
                      "tooltip":_("Last files you've used")})
        else:
            doc=xml.dom.minidom.parse(os.path.expanduser("~")+ "/" + ".recently-used.xbel")
            list=[]
            for xbel in doc.childNodes:
                if xbel.nodeType == xbel.ELEMENT_NODE and xbel.localName == "xbel":
                    for e in xbel.childNodes:
                        if e.nodeType == xbel.ELEMENT_NODE and e.localName == "bookmark":
                            URI= e.getAttribute("href")
                            URI=URI.replace("file:///", "/")
                            if os.path.exists(URI):
                                mime=gnomevfs.get_mime_type(URI)
                                mime=mime.replace("/", "-")
                                name=URI.split("/")
                                name=name[len(name)-1]
                                list.append({"URI":URI, "MIME":mime, "NAME":name})
            list.reverse()
            other_options=[]
            show_root, show_term=ConfigureBrowseFiles.read_config()
            if show_root:
                other_options.append({"name":_("Open as root"), "command":["gksu", "'gnome-open " + el["URI"].replace(" ", "\ ") + "'"]})
            for el in list:
                icon=el["MIME"]
                menu.append({
                      "icon":icon,
                      "name":el["NAME"],
                      "type":"openFile",
                      "obj":el["URI"],
                      "other_options":other_options,
                      "tooltip":el["URI"]})
            

        return menu