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

import gnomevfs, os
#    This is a AGM plugin
conf=config.conf()
class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Search in Favorite Apps"
        self.description="This plugin allow the search in your favorite apps"
        self.license="GPL"
        self.is_configurable=False
        self.type=AGM_plugin.TYPE_SEARCH
        
        pass
    
    def set_parent(self, parent):
        self.start_parent=parent
    
    def set_lastid(self, lastid):
        self.lastid=lastid
    
    def configure(self):
        pass
    
    def search(self, key):
        found=[]
        key=key.lower()
        for app in conf.fav_apps:
            if app["name"].lower().find(key)>=0:
                command=app["command"].split("#")
                found.append({
                  "icon":app["icon"],
                  "name":app["name"],
                  "type":command[0],
                  "obj":command[1],
                  "tooltip":app["name"]})
        return found