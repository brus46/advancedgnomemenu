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
import AGM.AGM_plugins as plugins
import AGM.AGM_utils as utils
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
        
        self.gradient_start_position=AGM_config_tabs.gradient_combo(conf.gradient_direction.get_start_point())
        self.gradient_end_position=AGM_config_tabs.gradient_combo(conf.gradient_direction.get_end_point())
        self.ConfigObj.get_widget("gradient_start_position").add(self.gradient_start_position)
        self.ConfigObj.get_widget("gradient_end_position").add(self.gradient_end_position)
        
        self.ConfigObj.get_widget("Top_icon").set_from_pixbuf(utils.getPixbufFromName(conf.top_icon_other_logo, 48))
        self.ConfigObj.get_widget("Applet_icon").set_from_pixbuf(utils.getPixbufFromName(conf.applet_icon, 48))
        
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
                "MoveUpPlugin": self.move_up,
                "MoveDwPlugin": self.move_dw,
                "ActivePlugin": self.activate,
                "DeactivePlugin": self.deactivate,
                "ConfigurePlugin": self.configure,
                "InstallNewPlugin": self.install_new_plugin,
        ##GLOBAL COMMANDS
            #Ok, Cancel, Apply buttons
                "on_ok_clicked" : self.ok_pressed,
                "on_apply_clicked" : self.apply_pressed,
                "on_cancel_clicked" : self.cancel_pressed,
            #Main Window management
                "on_main_window_delete_event" : self.cancel_pressed,
                "on_main_window_destroy_event" : self.cancel_pressed }
        
        self.ConfigObj.signal_autoconnect(events)
        self.active_plugins.connect("cursor-changed", self.list_active_changed)
        
        if conf.show_update_from_svn==False:
            self.ConfigObj.get_widget("UpdateSVN").hide()
        if conf.show_update_from_svn_stable==False:
            self.ConfigObj.get_widget("UpdateStable").hide()

        
        if self.stand_alone:
            gtk.main()
            
    def loadConfig(self):
        # GENERAL
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

        self.set_complete_color(conf.welcome_color, self.ConfigObj.get_widget("welcome_message_color"))        
        self.set_complete_color(conf.applet_fg_color, self.ConfigObj.get_widget("Applet_text_color"))
        
        # LOOK
        self.set_complete_color(conf.gradient_color1, self.ConfigObj.get_widget("Gradient_1"))
        self.set_complete_color(conf.gradient_color2, self.ConfigObj.get_widget("Gradient_2"))
        self.set_complete_color(conf.gradient_color3, self.ConfigObj.get_widget("Gradient_3"))
        self.set_complete_color(conf.iconbgcolor, self.ConfigObj.get_widget("Icon_BG"))
        self.set_complete_color(conf.bgcolor, self.ConfigObj.get_widget("bg_color"))
        self.set_complete_color(conf.selectedbgcolor, self.ConfigObj.get_widget("sel_bg_color"))
        self.set_complete_color(conf.fgcolor, self.ConfigObj.get_widget("fg_color"))
        self.set_complete_color(conf.selectedfgcolor, self.ConfigObj.get_widget("sel_fg_color"))
        self.ConfigObj.get_widget("use_3_gradient").set_active(conf.gradient_enable_3color)
        
        self.ConfigObj.get_widget("WindowOpacity").set_value(conf.opacity*100)
        self.ConfigObj.get_widget("icon_dimension").set_value(conf.menu_icon_size)
        
        
        self.ConfigObj.get_widget("smart_top_icon").set_active(conf.top_icon_enable_smart_mode)
        
        # FAV APPS
        
        # THEMES
        
        # PLUGINS
        
        
    def change_config(self):
        # GENERAL
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
        
        conf.welcome_color=self.ConfigObj.get_widget("welcome_message_color").get_color().to_string()
        conf.applet_fg_color=self.ConfigObj.get_widget("Applet_text_color").get_color().to_string()
        
        # LOOK
        conf.gradient_color1=self.parse_color(self.ConfigObj.get_widget("Gradient_1"))
        conf.gradient_color2=self.parse_color(self.ConfigObj.get_widget("Gradient_2"))
        conf.gradient_color3=self.parse_color(self.ConfigObj.get_widget("Gradient_3"))
        
        conf.iconbgcolor=self.parse_color(self.ConfigObj.get_widget("Icon_BG"))
        
        conf.bgcolor=self.ConfigObj.get_widget("bg_color").get_color().to_string()
        conf.selectedbgcolor=self.ConfigObj.get_widget("sel_bg_color").get_color().to_string()
        conf.fgcolor=self.ConfigObj.get_widget("fg_color").get_color().to_string()
        conf.selectedfgcolor=self.ConfigObj.get_widget("sel_fg_color").get_color().to_string()
        
        conf.gradient_enable_3color=self.ConfigObj.get_widget("use_3_gradient").get_active()
        conf.opacity=self.ConfigObj.get_widget("WindowOpacity").get_value()/100
        conf.menu_icon_size=self.ConfigObj.get_widget("icon_dimension").get_value_as_int()
        
        conf.top_icon_enable_smart_mode=self.ConfigObj.get_widget("smart_top_icon").get_active()
        # FAV APPS
        
        # THEMES
        
        # PLUGINS
        
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

    def install_new_plugin(self, obj):
        from AGM_utils import OpenPlugin
        path=OpenPlugin().get_file()
        print path
        if path!=None and os.path.isfile(path):
            try:
                os.mkdir("/tmp/AGM/")
            except: print "Cannot create temp-dir"
            
            try:
                os.system("cp " + path + " /tmp/AGM/plugin.tar")
                os.system("cd /tmp/AGM/ && tar -xvf /tmp/AGM/plugin.tar")
                os.system("rm /tmp/AGM/plugin.tar")
                command="gksu 'cp /tmp/AGM/*.py " + conf.plugin_folder +"'"
                print command
                os.system(command)
            except: print "Cannot extract plugin in temp-dir"
            os.system("rm -R /tmp/AGM/")
        self.avaible_plugins.clean_list()
        self.avaible_plugins.load()

    def list_active_changed(self, obj=None, row=None):
        plugin=self.active_plugins.get_selected()
        avaible_plugins=plugins.get_child_plugins()
        if plugin!=None and avaible_plugins.has_key(plugin):
            plugin=avaible_plugins[plugin]
            if plugin.is_configurable:
                self.ConfigObj.get_widget("ConfigurePlugin").set_sensitive(True)
            else:
                self.ConfigObj.get_widget("ConfigurePlugin").set_sensitive(False)
            self.ConfigObj.get_widget("DescriptionPlugin").set_text(plugin.name+"\n"+plugin.description+"\n"+plugin.author+ " " + plugin.author_site)
        else: 
            self.ConfigObj.get_widget("ConfigurePlugin").set_sensitive(False)
            self.ConfigObj.get_widget("DescriptionPlugin").set_text("")
        pass
    
    def configure(self, obj):
        plugin=self.active_plugins.get_selected()
        avaible_plugins=plugins.get_child_plugins()
        if plugin!=None and avaible_plugins.has_key(plugin):
            if avaible_plugins[plugin].is_configurable:
                avaible_plugins[plugin].configure()
    
            
    def move_up(self, obj):
        print "moving"
        self.active_plugins.moveup()
        
    def move_dw(self, obj):
        self.active_plugins.movedown()
    
    def activate(self, obj):
        self.active_plugins.add(self.avaible_plugins.get_selected())
        pass
    
    def deactivate(self, obj):
        self.active_plugins.remove()
        pass


    #COLOR BUTTONS
    def set_complete_color(self, color, colorbutton):
        colorbutton.set_color(self.get_color_no_opacity(color))
        colorbutton.set_alpha(self.get_opacity(color))
    
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
        #return 255*256
        #else: print color
        return 0
    
    def parse_color(self, colorbutton):
        color="#"
        colore=colorbutton.get_color().to_string()
        color+=colore[1]+colore[2]
        color+=colore[5]+colore[6]
        color+=colore[9]+colore[10]
        #opacity
        alpha=colorbutton.get_alpha()
        alpha=alpha/256
        alpha=""+hex(alpha)
        color+=alpha.replace("0x", "")
        return color