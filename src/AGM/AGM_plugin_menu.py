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

import gtk, sys, os

class PluginMenu(gtk.Menu):
    def __init__(self, menu_dict=None):
        gtk.Menu.__init__(self)
        self.menu_list=[]
        if menu_dict!=None:
            for el in menu_dict:
                menu_item=gtk.MenuItem()
                Label=gtk.Label(el["name"])
                Label.show()
                menu_item.add(Label)
                self.append(menu_item)
                menu_item.connect("activate", self.clicked, el["command"])
                menu_item.show()
                self.menu_list.append(menu_item)
                pass
    
    def clicked(self, obj, command):
        if (os.fork()==0):
            os.execvp(command[0], command)
            sys.exit(-1)
    
    def show(self, button_clicked=None):
        self.popup(None, None, None, 0, 0)
        pass