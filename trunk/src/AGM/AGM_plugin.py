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

#    All plugins must extend this class

TYPE_MENU="type_menu"
TYPE_SEARCH="type_search"
TYPE_MIX="type_mix"

class AGM_plugin:
    def __init__(self):
        self.author=""
        self.author_site=""
        self.name=""
        self.description=""
        self.license=""
        self.type=TYPE_MIX
        self.is_configurable=False
    
    def configure(self):
        pass
    
    def search(self, key):
        return []
    
    def get_menu(self, show=None):
        return []