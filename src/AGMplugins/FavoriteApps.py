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
import AGM.AGM_default_config as config
from AGM.AGM_plugin import AGM_plugin as plugin
from AGM import AGM_plugin
from AGM import localization
_=localization.Translate
import gnomevfs, os
#    This is a AGM plugin
conf=config.conf()
class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Favorite Apps plugin"
        self.description="This plugin shows your favorite apps"
        self.license="GPL"
        self.is_configurable=False
        self.type=AGM_plugin.TYPE_MENU
        
        pass
    
    def set_parent(self, parent):
        self.start_parent=parent
    
    def set_lastid(self, lastid):
        self.lastid=lastid
    
    def configure(self):
        pass
    
    def get_menu(self, show=None):
        menu=[]
        if show!="show":
            icon=utils.getPixbufFromName("emblem-favorite")
            menu.append({
                  "icon":icon,
                  "name":_("Favorite"),
                  "type":"enter",
                  "obj":"show",
                  "tooltip":_("Your favorites apps.")})
        else:
            for app in conf.fav_apps:    
                command=app["command"].split("#")
                print command
                menu.append({
                  "icon":utils.getPixbufFromName(app["icon"]),
                  "name":app["name"],
                  "type":command[0],
                  "obj":command[1],
                  "tooltip":app["name"]})
        return menu