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

import gtk, sys, os, gtk.glade
from AGM.AGM_default_config import conf as config
from AGM import AGM_config_tabs
import localization
_=localization.Translate

conf=config()

class Config():
    def __init__(self, stand_alone=False, win=None):
        self.stand_alone=stand_alone
        self.win=win
        
        self.ConfigObj = gtk.glade.XML(conf.install_data_dir + "AGM_configurator.glade")
        self.MainWindow=self.ConfigObj.get_widget("main_window")
        self.MainWindow.set_icon_from_file(conf.default_logo_path)
        
        self.FavApps=AGM_config_tabs.config_fav_apps()
        self.ConfigObj.get_widget("FavAppsPlace").pack_start(self.FavApps)
        
        self.avaible_plugins=AGM_config_tabs.plugin_list()
        self.active_plugins=AGM_config_tabs.active_plugin_list()
        self.ConfigObj.get_widget("AvaiblePlugins").add_with_viewport(self.avaible_plugins)
        self.ConfigObj.get_widget("ActivePlugins").add_with_viewport(self.active_plugins)
        
        self.ThemesList=AGM_config_tabs.theme_list()
        self.ConfigObj.get_widget("Themes").add_with_viewport(self.ThemesList)
        
        self.loadConfig()
        self.MainWindow.show_all()
        
        events = {
        ## TAB GENERAL
            #Update from svn
                "update_from_svn":self.update_svn,
                "update_from_svn_stable":self.update_stable,
        ## TAB LOOK and FEEL
        ## TAB FAV APPS
        ## TAB THEMES
        ## TAB PLUGINS
        ##GLOBAL COMMANDS
            #Ok, Cancel, Apply buttons
                "on_ok_clicked" : self.ok_pressed,
                "on_apply_clicked" : self.apply_pressed,
                "on_cancel_clicked" : self.cancel_pressed,
            #Main Window management
                "on_main_window_delete_event" : self.cancel_pressed,
                "on_main_window_destroy_event" : self.cancel_pressed }
        
        self.ConfigObj.signal_autoconnect(events)
        
        if self.stand_alone:
            gtk.main()
            
    def loadConfig(self):
        self.ConfigObj.get_widget("welcome_message").set_text(conf.welcome)
        self.ConfigObj.get_widget("Applet_text").set_text(conf.applet_text)
                
        self.ConfigObj.get_widget("Show_fav_apps").set_active(conf.fav_apps_show)
        self.ConfigObj.get_widget("Show_search_box").set_active(conf.search_box_show)
        self.ConfigObj.get_widget("Show_welcome_message").set_active(conf.show_welcome)
        self.ConfigObj.get_widget("Show_execution_box").set_active(conf.execution_box_show)
        self.ConfigObj.get_widget("Show_user_icon").set_active(conf.top_icon_show_logo)
        self.ConfigObj.get_widget("Show_fav_apps_name").set_active(conf.fav_apps_show_text)
        self.ConfigObj.get_widget("Show_applet_text").set_active(conf.applet_show_text)
        
        self.ConfigObj.get_widget("Hide_menu_after_launch_app").set_active(conf.hide_on_program_launch)
        self.ConfigObj.get_widget("Open_folder_command").set_text(conf.open_folder_command)
        self.ConfigObj.get_widget("Open_file_command").set_text(conf.open_file_command)
            
    def change_config(self):
        conf.welcome=self.ConfigObj.get_widget("welcome_message").get_text()
        conf.applet_text=self.ConfigObj.get_widget("Applet_text").get_text()
        
        conf.fav_apps_show=self.ConfigObj.get_widget("Show_fav_apps").get_active()
        conf.search_box_show=self.ConfigObj.get_widget("Show_search_box").get_active()    
        conf.show_welcome=self.ConfigObj.get_widget("Show_welcome_message").get_active()
        conf.execution_box_show=self.ConfigObj.get_widget("Show_execution_box").get_active()
        conf.top_icon_show_logo=self.ConfigObj.get_widget("Show_user_icon").get_active()
        conf.fav_apps_show_text=self.ConfigObj.get_widget("Show_fav_apps_name").get_active()
        conf.applet_show_text=self.ConfigObj.get_widget("Show_applet_text").get_active()

        conf.hide_on_program_launch=self.ConfigObj.get_widget("Hide_menu_after_launch_app").get_active()        
        conf.open_folder_command=self.ConfigObj.get_widget("Open_folder_command").get_text()
        conf.open_file_command=self.ConfigObj.get_widget("Open_file_command").get_text()
    
    def writeConfig(self):
        self.change_config()
        conf.rewrite() 
           
        file_fav_app=self.FavApps.to_string()
        
        try:
            file=open(conf.favorites_path, "w")
            file.write(file_fav_app)
            file.close()
        except:
            print "Cannot write fav apps!!! BIG TROUBLE!!"
    
    def apply_pressed(self, obj=None):
        #self.theme.SaveTheme()
        self.writeConfig()            

    def ok_pressed(self, obj):
        self.apply_pressed()
        self.cancel_pressed()

    def cancel_pressed(self, obj=None, event=None):
        self.MainWindow.hide_all()
        if self.stand_alone:
            gtk.main_quit()
            
    def update_stable(self, obj):
        update="/usr/bin/agm_update"
        if os.path.isfile(update):
            utils.ExecCommand(["gnome-terminal", "-e", update])
        pass
    
    def update_svn(self, obj):
        update="/usr/bin/agm_update_unstable"
        if os.path.isfile(update):
            utils.ExecCommand(["gnome-terminal", "-e", update])

