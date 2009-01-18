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

import gtk
from AGM.AGM_default_config import conf as config
conf=config()
import AGM.AGM_utils as utils
import localization
_=localization.Translate

import AGM_Entry

class search_box(gtk.HBox):
    def __init__(self, search_function, get_gradient):
        gtk.HBox.__init__(self)
        self.search_text=AGM_Entry.Entry(get_gradient)
        self.label=gtk.Label(_("Search")+":")
        self.search_text.set_tooltip_text(_("Search"))
        self.search = search_function
        self.search_text.connect("activate", self.change)
        
        #self.search_text.set_size_request(conf.window_width -70 - 32, -1)
        
        self.search_button=gtk.Button()
        Sicon=gtk.Image()
        icon=utils.getPixbufFromName("search", 22, "app")
        Sicon.set_from_pixbuf(icon)
        self.search_button.set_image(Sicon)
        
        self.label.set_size_request(50, -1)
        self.search_button.set_relief(gtk.RELIEF_NONE)
        
        
        self.pack_end(self.search_button, False)
        self.pack_end(self.search_text)
        self.pack_start(self.label, False)
    
    def change(self, new_text):
        self.search(self.search_text.get_text())
        
    def set_text(self, text=""):
        self.search_text.set_text(text)
    
    def get_text(self):
        return self.search_text.get_text()
    
    def modify_bg(self, state, color):
        #self.search_text.do_expose_event()
        self.search_button.modify_bg(state, color)
    def modify_fg(self, state, color):
        #self.search_text.do_expose_event()
        self.label.modify_fg(state, color)
