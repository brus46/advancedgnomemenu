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

class Config(gtk.Window):
    def __init__(self, stand_alone=False, win=None):
        gtk.Window.__init__(self)
        conf.read_conf()
        AGM_config_tabs.reload_conf()
        self.main_win=win
        self.stand_alone=stand_alone
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("AGM Configuration")
        self.set_icon_from_file(conf.default_logo_path)
        
        ButtonBox = gtk.HButtonBox()
        ButtonBox.set_layout(gtk.BUTTONBOX_END)
        ButtonBox.set_spacing(5)
        applyButton=gtk.Button(stock=gtk.STOCK_APPLY)
        applyButton.set_use_stock(True)
        applyButton.connect("clicked", self.apply_pressed)

        okButton=gtk.Button(stock=gtk.STOCK_OK)
        okButton.set_use_stock(True)
        okButton.connect("clicked", self.ok_pressed)
        
        cancelButton=gtk.Button(stock=gtk.STOCK_CANCEL)
        cancelButton.set_use_stock(True)
        cancelButton.connect("clicked", self.cancel_pressed)
        
        ButtonBox.pack_end(okButton)
        ButtonBox.pack_end(applyButton)
        ButtonBox.pack_end(cancelButton)
        
        ##GENERAL
        self.bars_conf=AGM_config_tabs.general_config()
        
        ##POSITION
        self.positions=AGM_config_tabs.window_config()
        
        ##FAV APPS
        self.fav_apps=AGM_config_tabs.config_fav_apps()
        
        ##THEME
        self.theme = AGM_config_tabs.config_themes()
        
        ##MENU
        self.menu=AGM_config_tabs.menu()
        
        notebook=gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_LEFT)
        notebook.set_scrollable(True)
        
        self.bars_conf.set_border_width(5)
        notebook.append_page(self.bars_conf , gtk.Label("General"))
        
        theme_label=gtk.Label("Themes")
        theme_label.set_size_request(80, -1)
        notebook.append_page(self.theme , theme_label)
        
        self.positions.set_border_width(5)
        notebook.append_page(self.positions , gtk.Label("Window"))
        
        self.fav_apps.set_border_width(5)
        notebook.append_page(self.fav_apps , gtk.Label("Fav apps"))
        self.menu.set_border_width(5)
        notebook.append_page(self.menu , gtk.Label("Menu"))
        
        VBox=gtk.VBox(spacing=5)
        VBox.set_border_width(5)
        VBox.pack_start(notebook)
        VBox.pack_end(ButtonBox, False, False)
        self.add(VBox)
        self.set_size_request(700,550)
        self.show_all()
        if self.stand_alone:
            gtk.main()
        pass
    
    def writeConfig(self):
        #Writing config
        file_config=""
        file_config+=self.theme.save_config()
        file_config+=self.menu.save_string()
        
        file_config+=self.positions.save_string()
        file_config+=self.bars_conf.to_string()
        
        try:
            file=open(conf.config_path, "w")
            file.write(file_config)
            file.close()
        except:
            print "Cannot write config!!! BIG TROUBLE!!"
            
        file_fav_app=self.fav_apps.to_string()
        
        try:
            file=open(conf.favorites_path, "w")
            file.write(file_fav_app)
            file.close()
        except:
            print "Cannot write fav apps!!! BIG TROUBLE!!"
    
    def apply_pressed(self, obj=None):
        self.theme.SaveTheme()
        self.writeConfig()            

    def ok_pressed(self, obj):
        self.theme.SaveTheme()
        self.writeConfig()  
        self.cancel_pressed()

    def cancel_pressed(self, obj=None):
        self.hide_all()
        if self.stand_alone:
            gtk.main_quit()

