# -*- coding: utf-8 -*-

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
import AGM.AGM_default_config as default_config
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
        
        self.FavApps=config_fav_apps()
        self.ConfigObj.get_widget("FavAppsPlace").pack_start(self.FavApps)
        
        self.avaible_plugins=plugin_list()
        self.active_plugins=active_plugin_list()
        self.ConfigObj.get_widget("AvaiblePlugins").add_with_viewport(self.avaible_plugins)
        self.ConfigObj.get_widget("ActivePlugins").add_with_viewport(self.active_plugins)
        
        self.gradient_start_position=gradient_combo(conf.gradient_direction.get_start_point())
        self.gradient_end_position=gradient_combo(conf.gradient_direction.get_end_point())
        self.ConfigObj.get_widget("gradient_start_position").add(self.gradient_start_position)
        self.ConfigObj.get_widget("gradient_end_position").add(self.gradient_end_position)
        
        self.ThemesList=theme_list()
        self.ConfigObj.get_widget("Themes").add_with_viewport(self.ThemesList)
        
        self.loadConfig()
        self.MainWindow.show_all()
        
        events = {
        ## TAB GENERAL
            #Update from svn
                "update_from_svn":self.update_svn,
                "update_from_svn_stable":self.update_stable,
        ## TAB LOOK and FEEL
                "change_top_icon": self.change_top_icon,
                "change_applet_icon": self.change_applet_icon,
        ## TAB FAV APPS
                #Nothing
        ## TAB THEMES
                "EditTheme": self.edit_theme,
                "ImportTheme": self.import_theme,
                "DeleteTheme": self.delete_theme,
                "ApplyTheme": self.apply_theme,
        ## TAB PLUGINS
                "MoveUpPlugin": self.move_up_plugin,
                "MoveDwPlugin": self.move_dw_plugin,
                "ActivePlugin": self.activate_plugin,
                "DeactivePlugin": self.deactivate_plugin,
                "ConfigurePlugin": self.configure_plugin,
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
        self.active_plugins.connect("cursor-changed", self.list_plugin_changed, "active")
        self.avaible_plugins.connect("cursor-changed", self.list_plugin_changed, "avaible")
        
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
        
        self.ConfigObj.get_widget("Top_icon").set_from_pixbuf(utils.getPixbufFromName(conf.top_icon_other_logo, 48))
        self.ConfigObj.get_widget("Applet_icon").set_from_pixbuf(utils.getPixbufFromName(conf.applet_icon, 48))
        self.ConfigObj.get_widget("smart_top_icon").set_active(conf.top_icon_enable_smart_mode)
        
        # FAV APPS
        if conf.fav_apps_orientation=="H" or conf.fav_apps_orientation=="HT" or conf.fav_apps_orientation=="TopHorizontal":
            self.ConfigObj.get_widget("Top_Hor").set_active(True)
        elif conf.fav_apps_orientation=="HB" or conf.fav_apps_orientation=="BottomHorizontal":
            self.ConfigObj.get_widget("Bot_Hor").set_active(True)
        if conf.fav_apps_orientation=="V" or conf.fav_apps_orientation=="VR" or conf.fav_apps_orientation=="RightVertical":
            self.ConfigObj.get_widget("Rig_Ver").set_active(True)
        elif conf.fav_apps_orientation=="VL" or conf.fav_apps_orientation=="LeftVertical":
            self.ConfigObj.get_widget("Lef_Ver").set_active(True)
            
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
        
        conf.gradient_direction.read_string(self.gradient_start_position.get_selected()+";"+self.gradient_end_position.get_selected()+";")
        
        conf.top_icon_enable_smart_mode=self.ConfigObj.get_widget("smart_top_icon").get_active()
        # FAV APPS
        if self.ConfigObj.get_widget("Top_Hor").get_active():
            conf.fav_apps_orientation="H"
        elif self.ConfigObj.get_widget("Bot_Hor").get_active():
            conf.fav_apps_orientation="HB"
        elif self.ConfigObj.get_widget("Rig_Ver").get_active():
            conf.fav_apps_orientation="V"
        elif self.ConfigObj.get_widget("Lef_Ver").get_active():
            conf.fav_apps_orientation="VL"
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
    
    ## CHANGE PICTURES
    
    def change_top_icon(self, obj):
        new_icon=utils.OpenImage().get_file()
        if new_icon!=None and os.path.isfile(new_icon):
            conf.top_icon_other_logo=new_icon
            self.ConfigObj.get_widget("Top_icon").set_from_pixbuf(utils.getPixbufFromName(conf.top_icon_other_logo, 48))         
            
    def change_applet_icon(self, obj):
        new_icon=utils.OpenImage().get_file()
        if new_icon!=None and os.path.isfile(new_icon):
            conf.applet_icon=new_icon
            self.ConfigObj.get_widget("Applet_icon").set_from_pixbuf(utils.getPixbufFromName(conf.applet_icon, 48))
    
    ## UPDATE
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

    
    # PLUGINS
    def list_plugin_changed(self, obj=None,  list="avaible"):
        if list=="avaible":
            plugin=self.avaible_plugins.get_selected()
        else:
            plugin=self.active_plugins.get_selected()
        avaible_plugins=plugins.get_child_plugins()
        if plugin!=None and avaible_plugins.has_key(plugin):
            plugin=avaible_plugins[plugin]
            if list!="avaible":
                if plugin.is_configurable:
                    self.ConfigObj.get_widget("ConfigurePlugin").set_sensitive(True)
                else:
                    self.ConfigObj.get_widget("ConfigurePlugin").set_sensitive(False)
            else:
                self.ConfigObj.get_widget("ConfigurePlugin").set_sensitive(False)
            buffer=self.ConfigObj.get_widget("DescriptionPlugin").get_buffer().set_text(_(plugin.name+"\n"+plugin.description+"\n"+plugin.author+ " " + plugin.author_site))
        else: 
            self.ConfigObj.get_widget("ConfigurePlugin").set_sensitive(False)
            buffer=self.ConfigObj.get_widget("DescriptionPlugin").get_buffer().set_text("")
        pass
    
    def configure_plugin(self, obj):
        plugin=self.active_plugins.get_selected()
        avaible_plugins=plugins.get_child_plugins()
        if plugin!=None and avaible_plugins.has_key(plugin):
            if avaible_plugins[plugin].is_configurable:
                avaible_plugins[plugin].configure()
    
            
    def move_up_plugin(self, obj):
        print "moving"
        self.active_plugins.moveup()
        
    def move_dw_plugin(self, obj):
        self.active_plugins.movedown()
    
    def activate_plugin(self, obj):
        self.active_plugins.add(self.avaible_plugins.get_selected())
    
    def deactivate_plugin(self, obj):
        self.active_plugins.remove()

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

    def edit_theme(self, obj):
        pass
    
    def import_theme(self, obj):
        path=utils.OpenFile()
        path=path.get_file()
        if path!=None and os.path.isfile(path):
            theme_path=conf.theme_path.split("/")
            create_dir="/"
            for dir in theme_path:
                if dir!="":
                    create_dir+=dir+"/"
                    try:
                        os.mkdir(create_dir)
                    except: pass

            try:
                os.mkdir("/tmp/AGM/")
            except: print "Cannot create temp-dir"
            theme_name=path.split("/")
            theme_name=theme_name[len(theme_name)-1].replace(".tar", "")
            theme_name=theme_name.replace(".agmtheme", "")
            try:
                os.system("cp " + path + " /tmp/AGM/theme.tar")
                os.system("cd /tmp/AGM/ && tar -xvf /tmp/AGM/theme.tar")
                os.system("rm /tmp/AGM/theme.tar")
                os.system("cp -R /tmp/AGM/* " + conf.theme_path)
            except: print "Cannot extract theme in temp-dir"
            os.system("rm -R /tmp/AGM/")  
            self.ThemesList.refresh()
            
    def delete_theme(self, obj):
        folder=self.ThemesList.get_selected()
        if folder!=None and os.path.isdir(folder):
            os.system("rm -R " + folder)
            self.ThemesList.refresh()
    
    def apply_theme(self, obj):
        folder=self.ThemesList.get_selected()
        if folder!=None and os.path.isdir(folder):
            config_path=folder+"/theme.agmtheme"
            conf.read_conf(config_path)
            self.loadConfig()
        pass

    
class plugin_list(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)
        
        self.model = gtk.ListStore (str, str)
        COL_NAME, COL_KEY = (0, 1)
        
        self.set_model(self.model)
        self.treeselection = self.get_selection()
        self.treeselection.set_mode (gtk.SELECTION_SINGLE)

    
        cell = gtk.CellRendererText ()
        column = gtk.TreeViewColumn ('Plugin name', cell, text = COL_NAME)
        self.append_column (column)
        
        self.load()
    
    def load(self):
        avaible_plugins=plugins.get_child_plugins()
        keys=avaible_plugins.keys()
        keys.sort()
        for el in keys:
            self.model.append([avaible_plugins[el].name, el])
    
    def get_selected(self):
        model, iter = self.treeselection.get_selected()
        if iter:
           return model.get_value (iter, 1)
        return None
        
    def clean_list(self):
        self.model.clear()
        pass

class active_plugin_list(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)
        
        self.model = gtk.ListStore (str, str)
        COL_NAME, COL_KEY = (0, 1)
        
        self.set_model(self.model)
        self.treeselection = self.get_selection()
        self.treeselection.set_mode (gtk.SELECTION_SINGLE)

    
        cell = gtk.CellRendererText ()
        column = gtk.TreeViewColumn ('Plugin name', cell, text = COL_NAME)
        self.append_column (column)
        
        self.load()
        
    def load(self):
        avaible_plugins=plugins.get_child_plugins()
        for el in conf.menu_order:
            if el!="" and avaible_plugins.has_key(el):
                self.model.append([avaible_plugins[el].name, el])
    
    def get_selected(self):
        model, iter = self.treeselection.get_selected()
        if iter:
           return model.get_value (iter, 1)
        return None
        
    def refresh(self):
        self.clean_list()
        self.load()
    
    def clean_list(self):
        self.model.clear()
        pass

    def moveup(self):
        model, iter = self.treeselection.get_selected()
        if iter:
           first=None
           temp = self.model.get_iter_first ()
           last=None
           while temp:
                
                if (self.model.get_value(iter,1)==self.model.get_value (temp, 1)):
                    first=last
                    break;
                last=temp
                temp=self.model.iter_next(temp)
           
           if first!=None:
               model.swap(iter, first)
        
    
    def movedown(self):
        model, iter = self.treeselection.get_selected()
        if iter:
           first=model.iter_next(iter)
           if first!=None:
               model.swap(iter, first)

    def add(self, key):
        print key
        avaible_plugins=plugins.get_child_plugins()
        if avaible_plugins.has_key(key):
            conf.menu_order.append(key)
            self.refresh()
        pass

    def remove(self):
        model, iter = self.treeselection.get_selected()
        if iter:
           key=model.get_value (iter, 1)
           conf.menu_order.remove(key)
           self.refresh()

    def get_list(self):
        lista = []
        iter = self.model.get_iter_first ()
        while iter:
                lista.append(self.model.get_value (iter, 1))
                iter=self.model.iter_next(iter)

        return lista
    
class config_fav_apps(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self, spacing=5)
        self.list=fav_apps_list()
        self.list.connect("cursor-changed", self.el_changed)
        self.add(self.list)
        
        
        self.commands=gtk.VButtonBox()
        add=gtk.Button(gtk.STOCK_ADD)
        add.set_use_stock(True)
        add.connect("clicked", self.click, "add")
        edit=gtk.Button(gtk.STOCK_EDIT)
        edit.set_use_stock(True)
        edit.connect("clicked", self.click, "edit")
        delete=gtk.Button(gtk.STOCK_DELETE)
        delete.set_use_stock(True)
        delete.connect("clicked", self.click, "delete")
        moveup=gtk.Button(gtk.STOCK_GO_UP)
        moveup.set_use_stock(True)
        moveup.connect("clicked", self.click, "moveup")
        movedw=gtk.Button(gtk.STOCK_GO_DOWN)
        movedw.set_use_stock(True)
        movedw.connect("clicked", self.click, "movedw")
    
        self.commands.add(add)
        self.commands.add(edit)
        self.commands.add(delete)
        self.commands.add(moveup)
        self.commands.add(movedw)
        
        self.LeftBox=gtk.VBox()
        self.LeftBox.pack_start(gtk.Label())
        self.LeftBox.pack_start(self.commands, False)
        self.LeftBox.pack_end(gtk.Label())        
        
        self.pack_end(self.LeftBox, False)
    
    def click(self, obj, action):
        print action
        if action=="add":
            self.list.add()
        elif action=="edit":
            self.list.edit()
        elif action=="delete":
            self.list.remove()
        elif action=="moveup":
            self.list.moveup()
        elif action=="movedw":
            self.list.movedown()
        elif action=="set_image":
            filename=utils.OpenImage().get_file()
            if filename!=None and os.path.isfile(filename):
                self.iconName=filename
                self.icon.set_from_pixbuf(utils.getPixbufFromName(self.iconName, 48, "app"))
                self.iconButton.set_image(self.icon)
    def to_string(self):
        file_fav_app=""
        for fav_app in conf.fav_apps:
            file_fav_app+= fav_app["name"] + ";" + fav_app["icon"] + ";" + fav_app["tooltip"] + ";" + fav_app["command"] + "\n"
        return file_fav_app
    
    def el_changed(self, obj=None):
        name=""
        icon="None"
        command=""
        tooltip=""
        el_sel = self.list.get_selected()
        if el_sel!=None:
            (name, icon, command, tooltip)=el_sel
    
    def refreshList(self):
        self.list.refresh()
        pass

class fav_apps_list(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)
        
        self.model = gtk.ListStore (gtk.gdk.Pixbuf, str, str, str, str)
        COL_ICON, COL_NAME, COL_ICON_NAME, COL_COMMAND, COL_TOOLTIP = (0, 1, 2, 3, 4)
        
        self.set_model(self.model)
        self.treeselection = self.get_selection()
        self.treeselection.set_mode (gtk.SELECTION_SINGLE)

        cell = gtk.CellRendererPixbuf ()
        column = gtk.TreeViewColumn ('#', cell, pixbuf = COL_ICON)
        self.append_column (column)
    
        cell = gtk.CellRendererText ()
        column = gtk.TreeViewColumn ('Name', cell, text = COL_NAME)
        self.append_column (column)
        
        self.load()
        
    def load(self):
        for fav_app in conf.fav_apps:
            command=fav_app["command"]
            self.model.append([utils.getPixbufFromName(fav_app["icon"], 24, "app"), fav_app["name"], fav_app["icon"],  command, fav_app["tooltip"]])
    
    def get_selected(self):
        model, iter = self.treeselection.get_selected()
        if iter:
           return model.get_value (iter, 1), model.get_value (iter, 2), model.get_value (iter, 3), model.get_value(iter, 4)
        return None
        
    def refresh(self):
        self.clean_list()
        self.load()
    
    def rewrite_config(self):
        conf.fav_apps=[]
        for el in self.get_list():
            if len(el)==3:
                conf.fav_apps.append({"name":el[0], "icon":el[1], "command":el[2], "tooltip":el[0]})
            else:
                conf.fav_apps.append({"name":el[0], "icon":el[1], "command":el[2], "tooltip":el[3]})
    
    def clean_list(self):
        self.model.clear()
        pass

    def moveup(self):
        model, iter = self.treeselection.get_selected()
        if iter:
           first=None
           temp = self.model.get_iter_first ()
           last=None
           while temp:
                
                if (self.model.get_value(iter,1)==self.model.get_value (temp, 1)):
                    first=last
                    break;
                last=temp
                temp=self.model.iter_next(temp)
           
           if first!=None:
               model.swap(iter, first)
           self.rewrite_config()
        
    
    def movedown(self):
        model, iter = self.treeselection.get_selected()
        if iter:
           first=model.iter_next(iter)
           if first!=None:
               model.swap(iter, first)
           self.rewrite_config()
    
    def edit (self):
        (name, icon, command, tooltip)=self.get_selected()
        if name!=None:
            import AGM_edit_fav_app, AGM_Fav_app
            (name2, icon2, tooltip2, command2)=AGM_edit_fav_app.editFavApp(AGM_Fav_app.FavApp(name, icon, tooltip, command)).get_fav_app()
            model, iter = self.treeselection.get_selected()
            if iter:
                model.set_value(iter, 0, utils.getPixbufFromName(icon2, 24, "app"))
                model.set_value(iter, 1, name2)
                model.set_value(iter, 2, icon2)
                model.set_value(iter, 3, command2)
                model.set_value(iter, 4, tooltip2)
                self.rewrite_config()
    
    def add(self):
        import AGM_new_fav_app
        import AGM_Fav_app
        NewFA=AGM_new_fav_app.newFavApp().get_new_fav_app()
        if NewFA!=None and isinstance(NewFA, AGM_Fav_app.FavApp):
            conf.fav_apps.append({"name":NewFA.FA_name, "icon":NewFA.FA_icon, "command": NewFA.FA_command, "tooltip": NewFA.FA_tooltip})

            self.refresh()
        else: print "Cancel pressed"

    def remove(self):
        (name, icon, command, tooltip)=self.get_selected()
        if name!=None:
            try:
                conf.fav_apps.remove({"name":name, "icon":icon, "command": command, "tooltip":tooltip})
            except: print name, "not in list."
            self.refresh()

    def get_list(self):
        lista = []
        iter = self.model.get_iter_first ()
        while iter:
                lista.append([self.model.get_value (iter, 1), self.model.get_value (iter, 2), self.model.get_value (iter, 3)])
                iter=self.model.iter_next(iter)

        return lista

class theme_list(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)

        self.model = gtk.ListStore (gtk.gdk.Pixbuf, str, str)
        COL_ICON, COL_NAME= (0, 1)
        
        self.set_model(self.model)
        self.treeselection = self.get_selection()
        self.treeselection.set_mode (gtk.SELECTION_SINGLE)

        cell = gtk.CellRendererPixbuf ()
        column = gtk.TreeViewColumn (_('Screenshot'), cell, pixbuf = COL_ICON)
        self.append_column (column)

        cell = gtk.CellRendererText ()
        column = gtk.TreeViewColumn (_('Description'), cell, text = COL_NAME)
        self.append_column (column)
        
        self.load()
    
    def refresh(self):
        self.model.clear()
        self.load()
        pass
    
    def load(self):
        #Read themes.
        theme_folder=conf.theme_path
        if os.path.isdir(theme_folder):
            themes=os.listdir(theme_folder)
            for theme in themes:
                if os.path.isdir(theme_folder+theme):
                    description=""
                    try:
                        file=open(theme_folder+theme+"/description")
                        description=file.read()
                    except: pass
                    description=_("Theme name")+": " + theme + "\n\n"+description
                    self.model.append([utils.getPixbufFromName(theme_folder + theme + "/screenshot.png", 128, "theme"), description, theme_folder+theme+"/"])
    
    def get_selected(self):
        model, iter = self.treeselection.get_selected()
        if iter:
           return model.get_value (iter, 2)
        return None

class gradient_combo(gtk.HBox):
    def __init__(self, position):
        gtk.HBox.__init__(self)
        list=conf.gradient_direction.get_list()
        
        self.start=gtk.combo_box_new_text()
        self.start.append_text(list[position])
        for pos in list:
            if pos!=position:
                self.start.append_text(list[pos])
        self.add(self.start)
        self.start.set_active(0)
    
    def get_selected(self):
        return self.start.get_active_text()
