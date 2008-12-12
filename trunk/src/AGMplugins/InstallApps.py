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
from AGM.AGM_plugin import AGM_plugin as plugin
#    This is a AGM plugin

class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Install apps throught synaptic plugin"
        self.description="This plugin open the synaptic package manager"
        self.license="GPL"
        self.is_configurable=False
    
    def configure(self):
        pass
    
    def get_menu(self, parent=None):
        menu=[]
        menu.append({
                  "icon":utils.getPixbufFromName("synaptic", type="app"),
                  "name":"Install programs",
                  "type":"exec",
                  "obj":"gksu 'synaptic'",
                  "tooltip":"Install programs on your pc."})
        return menu