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

class ColorButton(gtk.HBox):
    def __init__(self, title="", color="#FFFFFFFF"):
        gtk.HBox.__init__(self, spacing=5)
        titleLabel=gtk.Label(title)
        titleLabel.set_size_request(100, 30)
        self.pack_start(titleLabel, False, False)
        self.Color=gtk.ColorButton()
        self.Color.set_use_alpha(True)
        
        self.set_complete_color(color)
        
        self.pack_end(self.Color, False, False)
        self.parse_color()
    
    def set_complete_color(self, color):
        self.Color.set_color(self.get_color_no_opacity(color))
        self.Color.set_alpha(self.get_opacity(color))
    
    def get_color_no_opacity(self, color):
        if len(color)<=7:
            for i in range(len(color), 7):
                color+="f"
        else:
            color=color[0]+color[1]+color[2]+color[3]+color[4]+color[5]+color[6]
        return gtk.gdk.color_parse(color)
    
    def get_opacity(self, color):
        if len(color)>=9:
            color=color[7]+color[8]
            return int(int(color, 16))*256
        return 255*256
    def parse_color(self):
        color="#"
        colore=self.Color.get_color().to_string()
        color+=colore[1]+colore[2]
        color+=colore[5]+colore[6]
        color+=colore[9]+colore[10]
        #opacity
        alpha=self.Color.get_alpha()
        alpha=alpha/256
        alpha=""+hex(alpha)
        color+=alpha.replace("0x", "")
        return color