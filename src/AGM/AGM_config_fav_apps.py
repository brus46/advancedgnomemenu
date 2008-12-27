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
from AGM.AGM_default_config import conf as config
from AGM import AGM_config_tabs
conf=config()

class ConfigFavApps(gtk.Window):
    def __init__(self, stand_alone=False, win=None):
        gtk.Window.__init__(self)
        conf.read_conf()
        AGM_config_tabs.reload_conf()
        self.main_win=win
        self.stand_alone=stand_alone
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("AGM FavApps")
        self.set_icon_from_file(conf.default_logo_path)
        
        self.fav_apps=AGM_config_tabs.config_fav_apps()
        
        VBox=gtk.VBox(spacing=5)
        
        VBox.add(self.fav_apps)
        
        Hbuttonbox=gtk.HButtonBox()
        VBox.pack_end(Hbuttonbox, False)
        
        apply_button=gtk.Button(stock=gtk.STOCK_APPLY)
        apply_button.set_use_stock(True)
        apply_button.connect("clicked", self.Apply)
        ok_button=gtk.Button(stock=gtk.STOCK_OK)
        ok_button.set_use_stock(True)
        ok_button.connect("clicked", self.Ok)
        cancel_button=gtk.Button(stock=gtk.STOCK_CANCEL)
        cancel_button.set_use_stock(True)
        cancel_button.connect("clicked", self.Cancel)
        
        Hbuttonbox.set_layout(gtk.BUTTONBOX_END)
        Hbuttonbox.set_spacing(5)
        Hbuttonbox.add(apply_button)
        Hbuttonbox.add(ok_button)
        Hbuttonbox.add(cancel_button)
        
        self.add(VBox)
        self.set_size_request(500, 500)
        self.show_all()
    
    def Apply(self, obj):
        self.writeConfig()
    
    def Cancel(self, obj):
        self.hide_all()
    
    def Ok(self, obj):
        self.Apply(obj)
        self.Cancel(obj)

    def writeConfig(self):
        #Writing config
        file_fav_app=self.fav_apps.to_string()
        
        try:
            file=open(conf.favorites_path, "w")
            file.write(file_fav_app)
            file.close()
        except:
            print "Cannot write fav apps!!! BIG TROUBLE!!"
    