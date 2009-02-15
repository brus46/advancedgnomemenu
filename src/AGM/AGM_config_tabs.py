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

conf=config()
import AGM.AGM_utils as utils
import AGM.AGM_plugins as plugins
from AGM.AGM_color_config import ColorButton as ColorButtonTr
from AGM import localization
_=localization.Translate

def reload_conf():
    conf.read_conf()

def set_label_size_and_align(label, size=150):
    label.set_size_request(size, -1)
    x, y=label.get_alignment()
    label.set_text(_(label.get_text()))
    label.set_alignment(0.0, y)
    return label

class config_plugin(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)
        Plugins=gtk.HBox()
        self.pack_start(Plugins)
        self.avaible_plugins=plugin_list()        
        avaible_place=gtk.ScrolledWindow()
        avaible_place.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        avaible_place.add_with_viewport(self.avaible_plugins)
        frame_avaible=gtk.VBox()
        frame_avaible.pack_start(gtk.Label("Avaible pugins"), False, True)
        frame_avaible.pack_end(avaible_place)
        Plugins.add(frame_avaible)
        
        ActivateButtonBox=gtk.VBox()
        activate=gtk.Button()
        activateIcon=gtk.Image()
        activateIcon.set_from_pixbuf(utils.getPixbufFromName("go-next", 32))
        activate.set_image(activateIcon)
        activate.connect("clicked", self.activate)
        deactivate=gtk.Button()
        deactivateIcon=gtk.Image()
        deactivateIcon.set_from_pixbuf(utils.getPixbufFromName("go-previous", 32))
        deactivate.set_image(deactivateIcon)
        deactivate.connect("clicked", self.deactivate)
        ActivateButtonBox.add(activate)
        ActivateButtonBox.add(deactivate)
        #ActivateButtonBox.set_layout(gtk.BUTTONBOX_SPREAD)
        Plugins.pack_start(ActivateButtonBox, False, False)
        
        self.active_plugins=active_plugin_list()        
        active_place=gtk.ScrolledWindow()
        active_place.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        active_place.add_with_viewport(self.active_plugins)
        active_avaible=gtk.VBox()
        active_avaible.pack_start(gtk.Label("Active pugins"), False, True)
        active_avaible.pack_end(active_place)
        Plugins.add(active_avaible)
        
        self.active_plugins.connect("cursor-changed", self.list_active_changed)
        
        MoveButtonBox=gtk.VBox()
        moveup=gtk.Button()
        UpIcon=gtk.Image()
        UpIcon.set_from_pixbuf(utils.getPixbufFromName("go-up", 32))
        moveup.set_image(UpIcon)
        moveup.connect("clicked", self.move_up)
        movedw=gtk.Button()
        DwIcon=gtk.Image()
        DwIcon.set_from_pixbuf(utils.getPixbufFromName("go-down", 32))
        movedw.set_image(DwIcon)
        movedw.connect("clicked", self.move_dw)
        MoveButtonBox.pack_start(moveup)
        MoveButtonBox.pack_start(movedw)
        #MoveButtonBox.set_layout(gtk.BUTTONBOX_SPREAD)
        Plugins.pack_start(MoveButtonBox, False)
        
        self.plugin_info=gtk.Label()
        self.plugin_info.set_size_request(100, 80)
        
        self.pack_start(self.plugin_info,False, False)
        
        ConfigureBox=gtk.HButtonBox()
        self.ConfigureButton=gtk.Button("Configure plugin")
        self.ConfigureButton.connect("clicked", self.configure)
        InstallPlugin=gtk.Button("Install new plugin")
        InstallPlugin.connect("clicked", self.install_new_plugin)
        ConfigureBox.add(self.ConfigureButton)
        ConfigureBox.add(InstallPlugin)
        self.pack_start(ConfigureBox, False, False)
        self.ConfigureButton.set_sensitive(False)
    
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
                self.ConfigureButton.set_sensitive(True)
            else:
                self.ConfigureButton.set_sensitive(False)
            self.plugin_info.set_text(plugin.name+"\n"+plugin.description+"\n"+plugin.author+ " " + plugin.author_site)
        else: 
            self.ConfigureButton.set_sensitive(False)
            self.plugin_info.set_text("")
        pass
    
    def configure(self, obj):
        plugin=self.active_plugins.get_selected()
        avaible_plugins=plugins.get_child_plugins()
        if plugin!=None and avaible_plugins.has_key(plugin):
            if avaible_plugins[plugin].is_configurable:
                avaible_plugins[plugin].configure()
    
            
    def move_up(self, obj):
        self.active_plugins.moveup()
        
    def move_dw(self, obj):
        self.active_plugins.movedown()
    
    def activate(self, obj):
        self.active_plugins.add(self.avaible_plugins.get_selected())
        pass
    
    def deactivate(self, obj):
        self.active_plugins.remove()
        pass

    def save_string(self):
        lista_plugins=self.active_plugins.get_list()
        file_config="menu="
        for el in lista_plugins:
            file_config+=el+"#"
        file_config+="\n"
        return file_config

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
        for el in avaible_plugins:
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
        self.LeftBox.pack_start(self.commands, False)
        
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
   

#        if icon=="None": icon=command.split(" ")[0]
#        model, iter = self.treeselection.get_selected()
#        if iter:
#            model.set_value(iter, 0, utils.getPixbufFromName(icon, 24, "app"))
#            model.set_value(iter, 1, name)
#            model.set_value(iter, 2, icon)
#            model.set_value(iter, 3, command)
#            model.set_value(iter, 4, tooltip)
#            self.rewrite_config()
#        pass
    
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

class behavior(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, spacing=5)
        self.hide_after_launch_program=gtk.CheckButton(_("Hide menu after lunching a menu app"))
        self.hide_after_launch_program.set_active(conf.hide_on_program_launch)
        # add config. Hide menu fav-app launch.
        # in the default_config is the var: conf.hide_menu_after_launch_fav_app
        # save string must be: "hide_menu_after_launch_fav_app=False/True"
        self.pack_start(self.hide_after_launch_program, False)

        OpenFileCommand=gtk.HBox(spacing=5)
        self.open_file_command=gtk.Entry()
        OpenFileCommand.pack_start(set_label_size_and_align(gtk.Label("Open file command:")), False)
        OpenFileCommand.pack_start(self.open_file_command)
        self.pack_start(OpenFileCommand, False)
        
        OpenFolderCommand=gtk.HBox(spacing=5)
        self.open_folder_command=gtk.Entry()
        OpenFolderCommand.pack_start(set_label_size_and_align(gtk.Label("Open folder command:")), False)
        OpenFolderCommand.pack_start(self.open_folder_command)
        self.pack_start(OpenFolderCommand, False)
        
        self.open_file_command.set_text(conf.open_file_command)
        self.open_folder_command.set_text(conf.open_folder_command)
        
        SizeBox=gtk.HBox(spacing=5)
        SizeBox.pack_start(set_label_size_and_align(gtk.Label("Menu icon size:")), False)
        self.SizeVal=gtk.SpinButton()
        self.SizeVal.set_range(16, 128)
        self.SizeVal.set_increments(1, 10)
        SizeBox.pack_start(self.SizeVal, False)
        self.SizeVal.set_value(conf.menu_icon_size)
        self.pack_start(SizeBox, False)
        
        self.pack_end(UpdateToSvn(), False)
        #Gnome
        #open-file: gnome-open
        #open-folder: nautilus
        #KDE
        #open-file: kfile (?)
        #open-folder: dolphin
        #XFCE
        #open-file: ?
        #open-folder: thunar
    
    def save_string(self):
        config=""
        if (self.hide_after_launch_program.get_active()):
            config+= "hide_on_program_launch=True\n"
        else: config+= "hide_on_program_launch=False\n"
        config+="open_file_command=" + self.open_file_command.get_text() + "\n"
        config+="open_folder_command=" + self.open_folder_command.get_text() + "\n"
        config+="menu_icon_size=" + str( self.SizeVal.get_value_as_int()) + "\n"
        return config

class applet_conf(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, spacing=5)
        self.applet_text=gtk.Entry()
        self.applet_text.set_text(conf.applet_text)
        self.applet_icon=gtk.Button()
        self.icon=conf.applet_icon
                
        self.applet_fg_color=gtk.ColorButton()
        HBoxFgcolor=gtk.HBox(spacing=5)
        HBoxFgcolor.pack_start(set_label_size_and_align(gtk.Label("Applet text color:")), False, False)
        HBoxFgcolor.pack_start(self.applet_fg_color, False)
        self.applet_fg_color.set_color(gtk.gdk.color_parse(conf.applet_fg_color))
        
        icon=gtk.Image()
        icon.set_from_pixbuf(utils.getPixbufFromName(self.icon, 48, "app"))
        self.applet_icon.set_image(icon)
        self.applet_icon.connect("clicked", self.change_image)
        
        iconBox=gtk.HBox()
        iconBox.pack_start(set_label_size_and_align(gtk.Label("Applet icon:")), False)
        iconBox.pack_start(self.applet_icon, False)

        self.txtBox=gtk.CheckButton(_("Show text: 'Menu' in the applet"))
        self.txtBox.set_active(conf.applet_show_text)
        
        self.pack_start(iconBox, False)
        self.pack_start(self.txtBox, False)
        self.pack_start(HBoxFgcolor, False)
        self.pack_start(gtk.Label(_("All changes on the applet will be applied on rebooting")))
    
    def change_image(self, obj):
        filename=utils.OpenImage().get_file()
        if filename!=None:
            self.icon=filename
            icon=gtk.Image()
            icon.set_from_pixbuf(utils.getPixbufFromName(self.icon, 48, "app"))
            self.applet_icon.set_image(icon)
    
    def save_string(self):
        conf="applet_icon=" +self.icon +"\napplet_fg_color=" +self.applet_fg_color.get_color().to_string() + "\n"
        if (self.txtBox.get_active()==True):
            conf+="applet_show_text="+ "True" +"\n"
        else: conf+="applet_show_text="+ "False" +"\n"
        return conf

class config_themes(gtk.Notebook):
    def __init__(self):
        gtk.Notebook.__init__(self)
        self.opacity=gtk.SpinButton()
        self.opacity.set_range(0,100)
        self.opacity.set_increments(1,10)
        self.bgcolor=gtk.ColorButton()
        self.fgcolor=gtk.ColorButton()
        self.selectedbgcolor=gtk.ColorButton()
        self.selectedfgcolor=gtk.ColorButton()
        self.activebgcolor=gtk.ColorButton()
        self.activefgcolor=gtk.ColorButton()
        
        self.use_system_colors=gtk.CheckButton(label=_("Use system colors for buttons (need restart)"))
        
        ##THEME
        ThemeWinPanel = gtk.VBox(spacing=5)
        ThemeWinPanel.set_border_width(5)
        
        ThemeButtonPanel = gtk.VBox(spacing=5)
        ThemeButtonPanel.set_border_width(5)
        
        ThemeCairoPanel = gtk.VBox(spacing=5)
        ThemeCairoPanel.set_border_width(5)
        
        ## WINDOW
        HBoxOpacity=gtk.HBox(spacing=5)
        HBoxOpacity.pack_start(gtk.Label(_("Window opacity:")), False, False)
        HBoxOpacity.pack_start(self.opacity, False, False)    
        HBoxOpacity.pack_start(gtk.Label("%"), False, False)
        
        ThemeWinPanel.pack_start(HBoxOpacity, False)
        
        ##BUTTONS
        HBoxSysColor=gtk.HBox(spacing=5)
        HBoxSysColor.pack_start(self.use_system_colors)
        
        HBoxBgcolor=gtk.HBox(spacing=5)
        HBoxBgcolor.pack_start(gtk.Label(_("Background:")), False, False)
        HBoxBgcolor.pack_end(self.bgcolor, False, False)
        HBoxFgcolor=gtk.HBox(spacing=5)
        HBoxFgcolor.pack_start(gtk.Label(_("Foreground:")), False, False)
        HBoxFgcolor.pack_end(self.fgcolor, False, False)
        
        HBoxSelBgcolor=gtk.HBox(spacing=5)
        HBoxSelBgcolor.pack_start(gtk.Label(_("Selected background:")), False, False)
        HBoxSelBgcolor.pack_end(self.selectedbgcolor, False, False)
        HBoxSelFgcolor=gtk.HBox(spacing=5)
        HBoxSelFgcolor.pack_start(gtk.Label(_("Selected foreground:")), False, False)
        HBoxSelFgcolor.pack_end(self.selectedfgcolor, False, False)
        
        HBoxActBgcolor=gtk.HBox(spacing=5)
        HBoxActBgcolor.pack_start(gtk.Label(_("Active background:")), False, False)
        HBoxActBgcolor.pack_end(self.activebgcolor, False, False)
        HBoxActFgcolor=gtk.HBox(spacing=5)
        HBoxActFgcolor.pack_start(gtk.Label(_("Active foreground:")), False, False)
        HBoxActFgcolor.pack_end(self.activefgcolor, False, False)
        
        ThemeButtonPanel.pack_start(HBoxSysColor, False)
        ThemeButtonPanel.pack_start(HBoxBgcolor, False)
        ThemeButtonPanel.pack_start(HBoxFgcolor, False)
        ThemeButtonPanel.pack_start(HBoxSelBgcolor, False)
        ThemeButtonPanel.pack_start(HBoxSelFgcolor, False)
        ThemeButtonPanel.pack_start(HBoxActBgcolor, False)
        ThemeButtonPanel.pack_start(HBoxActFgcolor, False)
        
        ##CAIRO
        self.gradient_color1=ColorButtonTr(_("Gradient color 1"), conf.gradient_color1)
        self.gradient_color2=ColorButtonTr(_("Gradient color 2"), conf.gradient_color2)
        self.gradient_color3=ColorButtonTr(_("Gradient color 3"), conf.gradient_color3)
        self.gradient_use_color3=gtk.CheckButton(label=_("Use the third color (will be the center color)"))
        self.gradient_direction=gradient_direction()
        self.lightingbgcolor=ColorButtonTr(_("Top light color"), conf.lightingcolor)
        self.show_light=gtk.CheckButton(label=_("Show top light"))
        #self.iconbordercolor=ColorButtonTr(_("Icon border color"), conf.iconbordercolor)
        self.iconbgcolor=ColorButtonTr(_("Icon bg color"), conf.iconbgcolor)        
        
        
        ThemeCairoPanel.pack_start(self.gradient_color1, False)
        ThemeCairoPanel.pack_start(self.gradient_color2, False)
        ThemeCairoPanel.pack_start(self.gradient_use_color3, False)
        ThemeCairoPanel.pack_start(self.gradient_color3, False)
        ThemeCairoPanel.pack_start(self.gradient_direction, False)
        ThemeCairoPanel.pack_start(self.show_light, False)
        ThemeCairoPanel.pack_start(self.lightingbgcolor, False)
        #ThemeCairoPanel.pack_start(self.iconbordercolor, False)
        ThemeCairoPanel.pack_start(self.iconbgcolor, False)

        ##THEME INFO
        SaveThemePanel=gtk.VBox()
        ThemeButtonBox = gtk.HButtonBox()
        ThemeButtonBox.set_layout(gtk.BUTTONBOX_END)
        ExportTheme=gtk.Button(_("Export Theme"))
        ExportTheme.connect("clicked", self.ExportTheme)
        SaveTheme=gtk.Button(_("Save Theme"))
        
        SaveTheme.connect("clicked", self.SaveTheme)
        ThemeButtonBox.add(ExportTheme)
        ThemeButtonBox.add(SaveTheme)
        self.themeName=gtk.Entry()
        SaveThemePanel.pack_end(ThemeButtonBox, False)
        SaveThemePanel.pack_end(self.themeName, False)
        SaveThemePanel.pack_end(gtk.Label(_("Theme name:")), False)
        
        ThemeInfoPanel=gtk.HBox()
        SaveThemePanel.pack_start(ThemeInfoPanel)
        
        ScreenshotPanel=gtk.VBox()
        self.screenshot_path="None"
        self.screenshot=gtk.Image()
        ScreenshotPlace=gtk.ScrolledWindow()
        ScreenshotPlace.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        ScreenshotPlace.add_with_viewport(self.screenshot)
        ScreenshotPanel.pack_start(ScreenshotPlace)
        ScreenshotOption=gtk.HButtonBox()
        LoadScreenshot=gtk.Button(_("New"))
        LoadScreenshot.connect("clicked", self.LoadScreenshot)
        ClearScreenshot=gtk.Button(_("Clear"))
        ClearScreenshot.connect("clicked", self.ClearScreenshot)        
        ShowScreenshot=gtk.Button(_("Show"))
        ShowScreenshot.connect("clicked", self.EnlargeScreenshot)
        ScreenshotOption.add(LoadScreenshot)
        ScreenshotOption.add(ClearScreenshot)
        ScreenshotOption.add(ShowScreenshot)
        ScreenshotPanel.pack_end(ScreenshotOption, False)
        
        DescriptionPane=gtk.VBox()
        DescriptionPane.pack_start(gtk.Label(_("Theme description: ")), False)
        self.description=gtk.TextView()
        DescriptionPlace=gtk.ScrolledWindow()
        DescriptionPlace.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        DescriptionPlace.add_with_viewport(self.description)
        DescriptionPane.pack_start(DescriptionPlace)
        
        ThemeInfoPanel.add(ScreenshotPanel)
        ThemeInfoPanel.add(DescriptionPane)
        
        ## Edit theme notebook
        themeNotebook=gtk.Notebook()
        themeNotebook.set_scrollable(True)
        themeNotebook.append_page(ThemeWinPanel , gtk.Label(_("Window")))
        themeNotebook.append_page(ThemeButtonPanel , gtk.Label(_("Buttons")))
        themeNotebook.append_page(ThemeCairoPanel , gtk.Label(_("Background")))
        themeNotebook.append_page(SaveThemePanel , gtk.Label(_("Theme")))
        ##END THEME       
        
        ## THEMES AVAIBLE
        themes=gtk.VBox()
        ImportButtonBox = gtk.HButtonBox()
        ImportButtonBox.set_layout(gtk.BUTTONBOX_END)
        ImportButtonBox.set_spacing(5)
        ImportTheme=gtk.Button(_("Import Theme"))
        ImportTheme.connect("clicked", self.ImportTheme)
        DeleteTheme=gtk.Button(_("Delete Theme"))
        DeleteTheme.connect("clicked", self.DeleteTheme)
        #LoadTheme=gtk.Button("Load Theme")
        #LoadTheme.connect("clicked", self.LoadSelected)
        #ImportButtonBox.add(LoadTheme)
        ImportButtonBox.add(ImportTheme)
        ImportButtonBox.add(DeleteTheme)
        themes.pack_start(ImportButtonBox, False)
        self.ThemesList=theme_list()
        self.ThemesList.connect("cursor_changed", self.LoadSelected)
        ScrolledList=gtk.ScrolledWindow()
        ScrolledList.add_with_viewport(self.ThemesList)
        themes.pack_start(ScrolledList)
        ## END THEMES AVAIBLE        
        
        self.append_page(themes, gtk.Label(_("Themes")))
        editTheme=gtk.HBox()
        editTheme.add(themeNotebook)
        self.append_page(editTheme, gtk.Label(_("Edit Theme")))
        
        self.load_config()
    
    def LoadScreenshot(self, obj=None):
        filename=utils.OpenImage().get_file()
        if filename!=None:
            self.screenshot_path=filename
            self.screenshot.set_from_file(self.screenshot_path)
        pass
    
    def ClearScreenshot(self, obj=None):
        self.screenshot.set_from_file(conf.install_data_dir+"pictures/AGMtheme.png")
        self.screenshot_path=None
        pass
    
    def EnlargeScreenshot(self, obj=None):
        if self.screenshot_path!=None and os.path.isfile(self.screenshot_path):
            if os.fork()==0:
               os.execvp("gnome-open", ["gnome-open", self.screenshot_path])
    
    def SaveTheme(self, obj=None):
        path=conf.theme
        if path!=None and self.themeName.get_text()!="":
            theme_name=self.themeName.get_text()
            theme_path=conf.theme_path.split("/")
            create_dir="/"
            for dir in theme_path:
                if dir!="":
                    create_dir+=dir+"/"
                    try:
                        os.mkdir(create_dir)
                    except: pass
            file_theme=self.save_config()
            try:
                os.mkdir(conf.theme_path + theme_name + "/")
            except: pass
            
            try:
                file=open(conf.theme_path + theme_name + "/theme.agmtheme", "w")
                file.write(file_theme)
                file.close()
            except:
                print "Cannot write config!!! BIG TROUBLE!!"
            
            try:
                description=""
                buffer=self.description.get_buffer()
                description=buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
                file=open(conf.theme_path + theme_name + "/description", "w")
                file.write(description)
                file.close()
            except:
                print "Cannot write description!!! minor trouble!!"
            #Copy screenshot
            if self.screenshot_path!=conf.theme_path + theme_name + "/":
                os.system("cp " + self.screenshot_path + " " + conf.theme_path + theme_name + "/" + "screenshot.png")
            self.ThemesList.refresh()
        pass
    
    def ExportTheme(self, obj=None):
        if self.themeName.get_text()=="": return None
        path=utils.GetFolder().get_folder()
        path+="/"
        if path!=None:
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
            theme_name=self.themeName.get_text()
            try:
                os.mkdir("/tmp/AGM/"+ theme_name)
            except: print "Cannot create temp-dir"
            file_theme=self.save_config()
            
            try:
                file=open("/tmp/AGM/"+ theme_name + "/theme.agmtheme", "w")
                file.write(file_theme)
                file.close()
            except:
                print "Cannot write config!!! BIG TROUBLE!!"
            
            try:
                description=""
                buffer=self.description.get_buffer()
                description=buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
                file=open("/tmp/AGM/"+ theme_name + "/description", "w")
                file.write(description)
                file.close()
            except:
                print "Cannot write description!!! minor trouble!!"
            #Copy screenshot
            os.system("cp " + self.screenshot_path + " " + "/tmp/AGM/"+ theme_name +"/"+"screenshot.png")
            
            #Tar the file
            os.system("cd /tmp/AGM/ && tar -cvf "+ theme_name+ ".tar "+ theme_name+ "/")
            #Export the file
            os.system("cp /tmp/AGM/" + theme_name+ ".tar "+ path + theme_name + ".agmtheme")
    
    def LoadSelected(self, obj=None):
        folder=self.ThemesList.get_selected()
        if folder!=None and os.path.isdir(folder):
            if (conf.read_conf( folder + "theme.agmtheme")):
                conf.theme=folder
                self.load_config()
    
    def DeleteTheme(self, obj=None):
        folder=self.ThemesList.get_selected()
        print folder
        if folder!=None and os.path.isdir(folder):
            os.system("rm -R " + folder)
            self.ThemesList.refresh()
            pass
    
    def ImportTheme(self, obj=None):
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
              
    def load_config(self):
        #self.ThemesList.refresh()
        if conf.theme!=None:
            themeName=conf.theme.split("/")
            themeName=themeName[len(themeName)-2]
            self.themeName.set_text(themeName)
            description=""
            try:
                file=open(conf.theme+"/description")
                description=file.read()
            except: pass
            self.description.get_buffer().set_text(description)
            self.screenshot_path=conf.theme+"screenshot.png"
            self.screenshot.set_from_pixbuf(utils.getPixbufFromName(self.screenshot_path, 300,"theme"))
        self.opacity.set_value(conf.opacity*100)
        
        self.bgcolor.set_color(gtk.gdk.color_parse(conf.bgcolor))
        self.fgcolor.set_color(gtk.gdk.color_parse(conf.fgcolor))

        self.selectedbgcolor.set_color(gtk.gdk.color_parse(conf.selectedbgcolor))
        self.selectedfgcolor.set_color(gtk.gdk.color_parse(conf.selectedfgcolor))

        self.activebgcolor.set_color(gtk.gdk.color_parse(conf.activebgcolor))
        self.activefgcolor.set_color(gtk.gdk.color_parse(conf.activefgcolor))
        
        self.gradient_color1.set_complete_color(conf.gradient_color1)
        self.gradient_color2.set_complete_color(conf.gradient_color2)
        self.gradient_color3.set_complete_color(conf.gradient_color3)
        self.lightingbgcolor.set_complete_color(conf.lightingcolor)
        self.iconbgcolor.set_complete_color(conf.iconbgcolor)
        #self.iconbordercolor.set_complete_color(conf.iconbordercolor)
        
        self.use_system_colors.set_active(conf.use_system_color)
        
        self.show_light.set_active(conf.show_lighting)
        self.gradient_use_color3.set_active(conf.gradient_enable_3color)
        
    def save_config(self):
        file_config=""
        file_config+="opacity=" + str(self.opacity.get_value()/100) + "\n"
        file_config+="bgcolor=" + self.bgcolor.get_color().to_string() + "\n"
        file_config+="selectedbgcolor=" + self.selectedbgcolor.get_color().to_string() + "\n"
        file_config+="activebgcolor=" + self.activebgcolor.get_color().to_string() + "\n"
        file_config+="fgcolor=" + self.fgcolor.get_color().to_string() + "\n"
        file_config+="selectedfgcolor=" + self.selectedfgcolor.get_color().to_string() + "\n"
        file_config+="activefgcolor=" + self.activefgcolor.get_color().to_string() + "\n"
        
        file_config+="gradient_color1=" + self.gradient_color1.parse_color() + "\n"
        file_config+="gradient_color2=" + self.gradient_color2.parse_color() + "\n"
        file_config+="gradient_color3=" + self.gradient_color3.parse_color() + "\n"
        file_config+="lightingbgcolor=" + self.lightingbgcolor.parse_color() + "\n"
        file_config+="iconbgcolor=" + self.iconbgcolor.parse_color() + "\n"
        #file_config+="iconbordercolor=" + self.iconbordercolor.parse_color() + "\n"
        
        if (self.use_system_colors.get_active()):
            file_config+="use_system_color=True\n"
        else:
            file_config+="use_system_color=False\n"
        if (self.gradient_use_color3.get_active()):
            file_config+="gradient_enable_3color=True\n"
        else:
            file_config+="gradient_enable_3color=False\n"
            
        if (self.show_light.get_active()):
            file_config+="show_lighting=True\n"
        else:
            file_config+="show_lighting=False\n"
        file_config+=self.gradient_direction.to_string()+"\n"
        if conf.theme!=None: file_config+="theme="+conf.theme + "\n"
        return file_config
    
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

class gradient_direction(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self)
        self.spacing=5
        
        list=conf.gradient_direction.get_list()
        
        self.start=gtk.combo_box_new_text()
        self.start.append_text(list[conf.gradient_direction.get_start_point()])
        for pos in list:
            if pos!=conf.gradient_direction.get_start_point():
                self.start.append_text(list[pos])

        self.end=gtk.combo_box_new_text()
        self.end.append_text(list[conf.gradient_direction.get_end_point()])
        for pos in list:
            if pos!=conf.gradient_direction.get_end_point():
                self.end.append_text(list[pos])
        
        self.start.connect("changed", self.change_direction)
        self.end.connect("changed", self.change_direction)
        
        self.pack_start(gtk.Label(_("Start pos:")), False)
        self.pack_start(self.start)
        self.pack_start(gtk.Label(_("End pos:")), False)
        self.pack_start(self.end)
        
    def change_direction(self, obj):
        start=self.start.get_active_text()
        end=self.end.get_active_text()
        if start!=None and end!=None:
            conf.gradient_direction.read_string(start+";"+end+";")
        
    def to_string(self):
        list=conf.gradient_direction.get_list()
        return "gradient_direction="+list[conf.gradient_direction.get_start_point()]+";"+list[conf.gradient_direction.get_end_point()]+";"
        pass

class top_icon_config(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)
        self.set_spacing(5)
        self.use_user_login_logo=gtk.RadioButton(label=_("Use user login image"))
        self.use_other_image=gtk.RadioButton(group=self.use_user_login_logo, label=_("Use this image: "))
        self.use_user_login_logo.set_size_request(150, -1)
        self.use_other_image.set_size_request(150, -1)
        self.iconButton=gtk.Button()
        self.iconName="None"
        self.icon=gtk.Image()
        self.icon.set_from_pixbuf(utils.getPixbufFromName(self.iconName, 48, "app"))
        self.iconButton.set_image(self.icon)
        self.iconButton.connect("clicked", self.click, "set_image")

        self.show_logo=gtk.CheckButton(_("Show icon in menu"))
        self.show_logo.connect("toggled", self.changed)
        
#        self.command_on_logo_clicked=gtk.Entry()
        
        self.pack_start(self.show_logo, False)
        
        self.frame_logo=gtk.Frame(_("Menu icon"))
        logos=gtk.VBox(spacing=5)
        logos.set_border_width(5)
        self.frame_logo.add(logos)
        self.pack_start(self.frame_logo, False)
        
        HBox2=gtk.HBox()
        HBox2.pack_start(self.use_user_login_logo, False)
        user_logo=gtk.Image()
        user_logo.set_from_pixbuf(utils.getPixbufFromName(conf.home_logo_path, 48, "app"))
        HBox2.pack_start(user_logo, False)
        logos.pack_start(HBox2, False)
        #HBox3=gtk.HBox()
        HBox2.pack_end(self.iconButton, False)
        HBox2.pack_end(self.use_other_image, False)
        #logos.pack_start(HBox3, False)
#        
#        label=set_label_size_and_align(gtk.Label("Command to execute when menu icon is clicked"), 250)
#        logos.pack_start(label, False)
#        logos.pack_start(self.command_on_logo_clicked, False)
        
        self.use_smart_top_icon=gtk.CheckButton(_("Use smart top icon"))
        self.use_smart_top_icon.set_active(conf.top_icon_enable_smart_mode)
        logos.pack_start(self.use_smart_top_icon, False)
        
        self.load_config()
        self.changed()
 
    def changed(self, obj=None):
        self.frame_logo.set_sensitive(self.show_logo.get_active())
            
    def click(self, obj, action):
        if action=="set_image":
            self.use_other_image.set_active(True)
            filename=utils.OpenImage().get_file()
            if filename!=None and os.path.isfile(filename):
                self.iconName=filename
                self.icon.set_from_pixbuf(utils.getPixbufFromName(self.iconName, 48, "app"))
                self.iconButton.set_image(self.icon)
    
    def load_config(self):
        if (conf.top_icon_mode==conf.USE_OTHER_LOGO):
            self.use_other_image.set_active(True)
        else:
            self.use_user_login_logo.set_active(True)
        
        self.show_logo.set_active(conf.top_icon_show_logo)
        
        if conf.top_icon_other_logo!=None and os.path.isfile(conf.top_icon_other_logo):
            self.iconName=conf.top_icon_other_logo
            self.icon.set_from_pixbuf(utils.getPixbufFromName(self.iconName, 48, "app"))
        #self.command_on_logo_clicked.set_text(conf.command_on_logo_clicked)
        
    def to_string(self):
        config=""
        if self.use_other_image.get_active():
            config+="top_icon_mode=" + conf.USE_OTHER_LOGO + "\n"        
        else:
            config+="top_icon_mode=" + conf.USE_USER_LOGO + "\n"
        
        if  self.show_logo.get_active():
            config+="top_icon_show_logo=True\n"
        else: config+="top_icon_show_logo=False\n"
        
        config+="top_icon_other_logo=" + self.iconName + "\n"
        
        config+="command_on_logo_clicked="+ conf.command_on_logo_clicked+"\n"
        
        if (self.use_smart_top_icon.get_active()):
            config+="top_icon_enable_smart_mode=" + "True" + "\n"
        else: config+="top_icon_enable_smart_mode=" + "False" + "\n"
        
        return config

class menu(gtk.Notebook):
    def __init__(self):
        gtk.Notebook.__init__(self)
        self.menu_behaviour=behavior()
        self.menu_behaviour.set_border_width(5)
        self.menu_elements=config_plugin()
        self.menu_elements.set_border_width(5)
        
        self.append_page(self.menu_behaviour, gtk.Label(_("Behaviour")))
        self.append_page(self.menu_elements, gtk.Label(_("Elements")))
    
    def save_string(self):
        return self.menu_behaviour.save_string() + self.menu_elements.save_string()
    
class general_config(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, spacing=5)
        
        
        self.welcome_text=gtk.Entry()
        HBoxWelcome=gtk.HBox(spacing=5)
        HBoxWelcome.pack_start(set_label_size_and_align(gtk.Label("Welcome text:")), False, False)
        HBoxWelcome.pack_start(self.welcome_text)
        self.pack_start(HBoxWelcome, False)
        self.welcome_text.set_text(conf.welcome)
        
        
        self.show_fav_bar=gtk.CheckButton(_("Show favourite applications"))
        self.show_fav_bar.set_active(conf.fav_apps_show)
        self.pack_start(self.show_fav_bar, False)
        
        self.show_search_bar=gtk.CheckButton(_("Show search box"))
        self.show_search_bar.set_active(conf.search_box_show)
        self.pack_start(self.show_search_bar, False)
        
        self.show_exec_bar=gtk.CheckButton(_("Show execution box"))
        self.show_exec_bar.set_active(conf.execution_box_show)
        self.pack_start(self.show_exec_bar, False)
        
        self.top_icon_config=top_icon_config()
        self.pack_start(self.top_icon_config, False)
        
            
        ## POPUP POSITION
#        HBoxPopup=gtk.HBox(spacing=5)
#        self.height=gtk.SpinButton()
#        self.height.set_range(0, 100)
#        self.height.set_value(conf.popupstyle.height)
#        self.height.set_increments(1, 100)
#        HBoxPopup.pack_start(set_label_size_and_align(gtk.Label("Popup height:")), False, False)
#        HBoxPopup.pack_start(self.height, False)
#        self.pack_start(HBoxPopup, False)
        
        ##WINDOW DIMENSION
#        self.win_height=gtk.SpinButton()
#        self.win_width=gtk.SpinButton()
#        self.win_height.set_range(200, gtk.gdk.screen_height())
#        self.win_height.set_value(conf.window_height)
#        self.win_height.set_increments(1, 100)
#        
#        self.win_width.set_range(200, gtk.gdk.screen_width())        
#        self.win_width.set_value(conf.window_width)
#        self.win_width.set_increments(1, 100)
#        
#        dimension=gtk.HBox(spacing=5)
#        dimension.pack_start(set_label_size_and_align(gtk.Label("Win height:")), False)
#        dimension.pack_start(self.win_height, False)
#        dimension.pack_start(set_label_size_and_align(gtk.Label("Win width:")), False)
#        dimension.pack_start(self.win_width, False)
#        self.pack_start(dimension, False)
        ##END WINDOW DIMENSION
        
          
        
        applet_frame=gtk.Frame(_("Applet config"))
        self.applet_conf=applet_conf()
        applet_frame.add(self.applet_conf)
        self.pack_start(applet_frame, False)
        
        
        ## SAFE_MODE
        self.safe_mode=gtk.CheckButton(_("Safe mode, will work without rounded borders."))
        self.safe_mode.set_active(conf.safe_mode)
        self.pack_start(self.safe_mode, False)
        ## END SAFE_MODE 
    
    def to_string(self):
        config=""
        if (self.show_fav_bar.get_active()):
            config+="fav_apps_show=" + "True" + "\n"
        else: config+="fav_apps_show=" + "False" + "\n"
        if (self.show_search_bar.get_active()):
            config+="search_box_show=" + "True" + "\n"
        else: config+="search_box_show=" + "False" + "\n"
        if (self.show_exec_bar.get_active()):
            config+="execution_box_show=" + "True" + "\n"
        else: config+="execution_box_show=" + "False" + "\n"
        
        config+="position=" + conf.startposition.to_string() + "\n"
        config+="top_position="  + conf.top_position.get_str() + "\n"
        config+="popup_style=" + conf.popupstyle.get_str() + "_" + str(conf.popupstyle.width) + "_" + str(conf.popupstyle.height) +  "\n"
        #config+="window_height=" + str(self.win_height.get_value()) +"\n"
        #config+="window_width=" + str(self.win_width.get_value()) + "\n"
        config+="window_height=" + str(conf.window_height) +"\n"
        config+="window_width=" + str(conf.window_width) + "\n"
        config+="welcome_text=" + self.welcome_text.get_text() + "\n"
        if (self.safe_mode.get_active()):
            config+= "safe_mode=True\n"
        else: config+= "safe_mode=False\n"
        config+=self.top_icon_config.to_string()
        config+=self.applet_conf.save_string()
        
        return config

class UpdateToSvn(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)
        stable_svn=gtk.Button(_("Update to the latest stable version"))
        trunk_svn=gtk.Button(_("Update to the latest version of the SVN"))
        VButtonBox=gtk.VButtonBox()
        VButtonBox.add(stable_svn)
        VButtonBox.add(trunk_svn)
        VButtonBox.set_spacing(5)
        VButtonBox.set_layout(gtk.BUTTONBOX_SPREAD)
        stable_svn.connect("clicked", self.update_stable)
        trunk_svn.connect("clicked", self.update_svn)        
        
        self.add(VButtonBox)
        
    def update_stable(self, obj):
    	update="/usr/bin/agm_update"
    	if os.path.isfile(update):
    		utils.ExecCommand(["gnome-terminal", "-e", update])
        pass
    
    def update_svn(self, obj):
        update="/usr/bin/agm_update_unstable"
    	if os.path.isfile(update):
    		utils.ExecCommand(["gnome-terminal", "-e", update])
