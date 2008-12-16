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

def set_label_size_and_align(label, size=150):
    label.set_size_request(size, -1)
    x, y=label.get_alignment()
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
                command="gksu cp /tmp/AGM/*.py " + conf.plugin_folder
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
        gtk.HBox.__init__(self)
        self.list=fav_apps_list()
        self.list.connect("cursor-changed", self.el_changed)
        self.add(self.list)
        
        self.edit_place=gtk.VBox(spacing=5)
        self.iconButton=gtk.Button()
        self.iconName="None"
        self.icon=gtk.Image()
        self.icon.set_from_pixbuf(utils.getPixbufFromName(self.iconName, 48, "app"))
        self.iconButton.set_image(self.icon)
        self.iconButton.connect("clicked", self.click, "set_image")
        ButtonPlace=gtk.VButtonBox()
        ButtonPlace.add(self.iconButton)
        
        name=gtk.HBox()
        name.pack_start(gtk.Label("Name:"), False)
        self.name_app=gtk.Entry()
        name.add(self.name_app)
        
        command=gtk.HBox()
        command.pack_start(gtk.Label("Command:"), False)
        self.command=gtk.Entry()
        command.add(self.command)
        
        self.edit_place.pack_start(ButtonPlace, False)
        self.edit_place.pack_start(name, False)
        self.edit_place.pack_start(command, False)
        
        
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
        self.LeftBox.pack_start(self.edit_place, False)
        self.LeftBox.pack_end(self.commands, False)
        
        self.pack_end(self.LeftBox, False)
    
    def click(self, obj, action):
        print action
        if action=="add":
            if (self.name_app.get_text()!="" and self.command.get_text()!=""):
                self.list.add(self.name_app.get_text(), self.iconName, self.command.get_text())
        elif action=="edit":
            if (self.name_app.get_text()!="" and self.command.get_text()!=""):
                self.list.edit(self.name_app.get_text(), self.iconName, self.command.get_text())
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
            file_fav_app+= fav_app["name"] + ";" + fav_app["icon"] + ";" + fav_app["command"] + "\n"
        return file_fav_app
    
    def el_changed(self, obj=None):
        name=""
        icon="None"
        command=""
        el_sel = self.list.get_selected()
        if el_sel!=None:
            (name, icon, command)=el_sel
        self.name_app.set_text(name)
        self.command.set_text(command.replace("\n", ""))
        self.iconName=icon
        self.icon.set_from_pixbuf(utils.getPixbufFromName(self.iconName, 48, "app"))
        self.iconButton.set_image(self.icon)
        pass
    
    def refreshList(self):
        self.list.refresh()
        pass
    
class fav_apps_list(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)
        
        self.model = gtk.ListStore (gtk.gdk.Pixbuf, str, str, str)
        COL_ICON, COL_NAME, COL_ICON_NAME, COL_COMMAND = (0, 1, 2, 3)
        
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
            self.model.append([utils.getPixbufFromName(fav_app["icon"], 24, "app"), fav_app["name"], fav_app["icon"], fav_app["command"].replace("exec#", "")])
    
    def get_selected(self):
        model, iter = self.treeselection.get_selected()
        if iter:
           return model.get_value (iter, 1), model.get_value (iter, 2), model.get_value (iter, 3)
        return None
        
    def refresh(self):
        self.clean_list()
        self.load()
    
    def rewrite_config(self):
        conf.fav_apps=[]
        for el in self.get_list():
            conf.fav_apps.append({"name":el[0], "icon":el[1], "command":el[2]})
    
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
    
    def edit (self, name, icon, command):
        if icon=="None": icon=command.split(" ")[0]
        model, iter = self.treeselection.get_selected()
        if iter:
            model.set_value(iter, 0, utils.getPixbufFromName(icon, 24, "app"))
            model.set_value(iter, 1, name)
            model.set_value(iter, 2, icon)
            model.set_value(iter, 3, command)
            self.rewrite_config()
        pass
    
    def add(self, name, icon, command):
        if icon=="None": icon=command.split(" ")[0]
        conf.fav_apps.append({"name":name, "icon":icon, "command": "exec#"+command})
        self.refresh()
        pass

    def remove(self):
        (name, icon, command)=self.get_selected()
        if name!=None:
            conf.fav_apps.remove({"name":name, "icon":icon, "command": "exec#"+command})
            self.refresh()

    def get_list(self):
        lista = []
        iter = self.model.get_iter_first ()
        while iter:
                lista.append([self.model.get_value (iter, 1), self.model.get_value (iter, 2), "exec#" + self.model.get_value (iter, 3)])
                iter=self.model.iter_next(iter)

        return lista

class config_fav_apps_apparence(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, spacing=5)
        self.show_apps=gtk.CheckButton()
        self.show_apps.set_label("Show apps bar")
        self.show_apps.set_active(conf.fav_apps_show)
        self.show_apps_text=gtk.CheckButton()
        self.show_apps_text.set_label("Show apps name")
        self.show_apps_text.set_active(conf.fav_apps_show_text)
        self.show_text_bold=gtk.CheckButton()
        self.show_text_bold.set_label("Apps name in bold")
        self.show_text_bold.set_active(conf.fav_apps_text_bold)
        self.orientation_horizontal=gtk.CheckButton()
        self.orientation_horizontal.set_label("Horizontal bar orientation")
        self.orientation_horizontal.set_active(conf.fav_apps_orientation=="H")
        self.icon_dimension=gtk.SpinButton()
        self.icon_dimension.set_range(20, 100)
        self.icon_dimension.set_value(conf.fav_apps_icon_dimension)
        self.icon_dimension.set_increments(1, 100)
        
        self.pack_start(self.show_apps, False)
        self.pack_start(self.show_apps_text, False)
        self.pack_start(self.show_text_bold, False)
        self.pack_start(self.orientation_horizontal, False)
        icon_box=gtk.HBox()
        icon_box.pack_start(gtk.Label("Icon size:"), False)
        icon_box.pack_start(self.icon_dimension, False)
        self.pack_start(icon_box, False)
    
    def save_string(self):
        config=""
        if (self.show_apps_text.get_active()):
            config+="fav_apps_show_text=" + "True" + "\n"
        else: config+="fav_apps_show_text=" + "False" + "\n"
        if (self.show_text_bold.get_active()):
            config+="fav_apps_text_bold=" + "True" + "\n"
        else: config+="fav_apps_text_bold=" + "False" + "\n"
        config+="fav_apps_icon_dimension=" + str(self.icon_dimension.get_value()) + "\n"
        if (self.orientation_horizontal.get_active()):
            config+="fav_apps_orientation=H\n"
        else: config+="fav_apps_orientation=V\n"
        if (self.show_apps.get_active()):
            config+="fav_apps_show=" + "True" + "\n"
        else: config+="fav_apps_show=" + "False" + "\n"
        
        return config

class behavior(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, spacing=5)
        self.hide_after_launch_program=gtk.CheckButton("Hide menu after lunching a menu app")
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

        txtBox=gtk.HBox()
        txtBox.pack_start(set_label_size_and_align(gtk.Label("Applet text:")), False)
        txtBox.pack_start(self.applet_text, False)
        
        self.pack_start(iconBox, False)
        self.pack_start(txtBox, False)
        self.pack_start(HBoxFgcolor, False)
        self.pack_start(gtk.Label("All changes on the applet will be applied on rebooting"))
    
    def change_image(self, obj):
        filename=utils.OpenImage().get_file()
        if filename!=None:
            self.icon=filename
            icon=gtk.Image()
            icon.set_from_pixbuf(utils.getPixbufFromName(self.icon, 48, "app"))
            self.applet_icon.set_image(icon)
    
    def save_string(self):
        return "applet_text=" + self.applet_text.get_text() +"\napplet_icon=" +self.icon +"\napplet_fg_color=" +self.applet_fg_color.get_color().to_string() + "\n"
    
class window_config(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, spacing=10)
        
        labelsize=150
        
        ##WINDOW
        self.welcome_text=gtk.Entry()
        HBoxWelcome=gtk.HBox(spacing=5)
        HBoxWelcome.pack_start(set_label_size_and_align(gtk.Label("Welcome text:")), False, False)
        HBoxWelcome.pack_start(self.welcome_text)
        self.pack_start(HBoxWelcome, False)
        self.welcome_text.set_text(conf.welcome)
        ##END WINDOW
        
        ## STARTUP POSITION
        Position=gtk.HBox(spacing=5)
        Position.pack_start(set_label_size_and_align(gtk.Label("Startup position:")), False)
                
        position_cod, x, y=conf.startposition.get_position()
        
        self.positions=gtk.combo_box_new_text()
        self.positions.append_text(conf.startposition.get_pos_name())
        for pos in conf.startposition.get_list():
            if pos!=conf.startposition.get_pos_name():
                self.positions.append_text(pos)
                
        Position.pack_start(self.positions, False)
        
        self.XYBox=gtk.HBox(spacing=5)
        self.XYBox.pack_start(gtk.Label("X: "), False)
        self.XVal=gtk.SpinButton()
        self.XVal.set_range(-1, gtk.gdk.screen_width())
        self.XVal.set_increments(1, 100)
        self.XYBox.pack_start(self.XVal, False)
        self.XVal.set_value(x)
        
        self.XYBox.pack_start(gtk.Label("Y: "), False)
        self.YVal=gtk.SpinButton()
        self.YVal.set_range(-1, gtk.gdk.screen_height())
        self.YVal.set_value(y)
        self.YVal.set_increments(1, 100)
        self.XYBox.pack_start(self.YVal, False)
        
        if position_cod!=conf.startposition.MANUAL:
            self.XYBox.set_sensitive(False)
        else: self.XYBox.set_sensitive(True)
        Position.pack_end(self.XYBox, False)
        self.pack_start(Position, False)
        
        self.XVal.connect("change-value", self.change_sp)
        self.YVal.connect("change-value", self.change_sp)
        self.positions.connect("changed", self.change_sp)
        
        ## END STARTUP POSITION
        
        ## POPUP POSITION
        style, width, height=conf.popupstyle.get_style()
        PopUp=gtk.HBox(spacing=5)
        self.popup=gtk.combo_box_new_text()
        self.popup.append_text(conf.popupstyle.get_str())
        for pop in conf.popupstyle.get_list():
            if pop!=conf.popupstyle.get_str():
                self.popup.append_text(pop)
        PopUp.pack_start(set_label_size_and_align(gtk.Label("Popup style:")), False)
        
        self.popup.connect("changed", self.change_pop)
        self.width=gtk.SpinButton()
        self.width.set_range(10, 400)
        self.width.set_value(width)
        self.width.set_increments(1, 100)
        
        self.height=gtk.SpinButton()
        self.height.set_range(10, 100)
        self.height.set_value(height)
        self.height.set_increments(1, 100)

        PopUp.pack_start(self.popup, False)
        
        WidthBox=gtk.HBox()
        WidthBox.pack_start(gtk.Label("Popup width: "), False)
        WidthBox.pack_start(self.width, False)
        HeightBox=gtk.HBox()
        HeightBox.pack_start(gtk.Label("Popup height: "), False)
        HeightBox.pack_start(self.height, False)
        
        if style!=conf.popupstyle.NONE:
            self.width.set_sensitive(True)
            self.height.set_sensitive(True)
        else:
            self.width.set_sensitive(False)
            self.height.set_sensitive(False)   
        
        PopUp.pack_end(WidthBox, False)
        PopUp.pack_end(HeightBox, False)
        
        self.pack_start(PopUp, False)
        ## END POPUP
        
        ## TOP STYLE
        TopStyle=gtk.HBox(spacing=5)
        TopStyle.pack_start(set_label_size_and_align(gtk.Label("Top style:")), False)
        self.top=gtk.combo_box_new_text()
        self.top.append_text(conf.top_position.get_str())
        for top in conf.top_position.get_list():
            if top!=conf.top_position.get_str():
                self.top.append_text(top)
        
        self.top.connect("changed", self.change_top)
        TopStyle.pack_start(self.top, False)
        self.pack_start(TopStyle, False)
        ## END TOP STYLE
        
        ##WINDOW DIMENSION
        self.win_height=gtk.SpinButton()
        self.win_width=gtk.SpinButton()
        self.win_height.set_range(350, gtk.gdk.screen_height())
        self.win_height.set_value(conf.window_height)
        self.win_height.set_increments(1, 100)
        
        self.win_width.set_range(350, gtk.gdk.screen_width())        
        self.win_width.set_value(conf.window_width)
        self.win_width.set_increments(1, 100)
        
        dimension=gtk.HBox(spacing=5)
        dimension.pack_start(set_label_size_and_align(gtk.Label("Win height:")), False)
        dimension.pack_start(self.win_height, False)
        dimension.pack_start(set_label_size_and_align(gtk.Label("Win width:")), False)
        dimension.pack_start(self.win_width, False)
        self.pack_start(dimension, False)
        ##END WINDOW DIMENSION
        
        ## SAFE_MODE
        self.safe_mode=gtk.CheckButton("Safe mode, will work without rounded borders.")
        self.safe_mode.set_active(conf.safe_mode)
        self.pack_start(self.safe_mode, False)
        ## END SAFE_MODE
        
        PreviewFrame=gtk.Frame()
        PreviewFrame.set_label("Preview:")
        self.preview=gtk.Image()
        PreviewFrame.add(self.preview)
        self.pack_end(PreviewFrame)
        self.set_preview()
        

    def id(self, str, list):
        pos=0
        if str!=None:
            str_pos=str
            for str in list:
                if str==str_pos:
                    break
                pos+=1
        return pos
    
    def change_pop(self, obj, scroll=None):
        pop=self.id(self.popup.get_active_text(), conf.popupstyle.get_list())
        conf.popupstyle.read_string(self.popup.get_active_text()+ "_" + str(self.width.get_value()))
        if pop!=conf.popupstyle.NONE:
            self.width.set_sensitive(True)
            self.height.set_sensitive(True)
        else:
            self.width.set_sensitive(False)
            self.height.set_sensitive(False)
        self.set_preview()    
            
    def change_sp(self, obj, scroll=None):
        pos=self.id(self.positions.get_active_text(), conf.startposition.get_list())
        conf.startposition.set_position(pos, self.XVal.get_value(), self.YVal.get_value())
        if pos!=conf.startposition.MANUAL:
            self.XYBox.set_sensitive(False)
        else: self.XYBox.set_sensitive(True)
        self.set_preview()
    
    def change_top(self, obj):
        top=self.id(self.top.get_active_text(), conf.top_position.get_list())
        conf.top_position.read_string(self.top.get_active_text())
        self.set_preview()
    
    def set_preview(self):
        # TODO: must use not N pictures but only few pictures and move them in order to obtain the current preview.
        pop=conf.popupstyle.get_str().replace(" ", "_")
        pos=conf.startposition.get_pos_name().replace(" ", "_")
        top=conf.top_position.get_str().replace(" ", "_")
        config=str(pop)+"#"+str(pos)+"#"+str(top)
        picture=conf.install_picture_dir+"pictures/"+config+".png"
        if os.path.isfile(picture)==False:
            picture=conf.install_picture_dir+"pictures/"+"None.png"
        self.preview.set_from_pixbuf(utils.getPixbufFromName(picture, 200, "app"))
        pass
    
    def save_string(self):
        config=""
        config+="position=" + conf.startposition.get_pos_name() + "_" + str(self.XVal.get_value()) + "_" + str(self.YVal.get_value()) + "\n"
        config+="top_position="  + conf.top_position.get_str() + "\n"
        config+="popup_style=" + conf.popupstyle.get_str() + "_" + str(self.width.get_value()) + "_" + str(self.height.get_value()) +  "\n"
        config+="window_height=" + str(self.win_height.get_value()) +"\n"
        config+="window_width=" + str(self.win_width.get_value()) + "\n"
        config+="welcome_text=" + self.welcome_text.get_text() + "\n"
        if (self.safe_mode.get_active()):
            config+= "safe_mode=True\n"
        else: config+= "safe_mode=False\n"
        return config

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
        
        self.use_system_colors=gtk.CheckButton(label="Use system colors for buttons (need restart)")
        
        ##THEME
        ThemeWinPanel = gtk.VBox(spacing=5)
        ThemeWinPanel.set_border_width(5)
        
        ThemeButtonPanel = gtk.VBox(spacing=5)
        ThemeButtonPanel.set_border_width(5)
        
        ThemeCairoPanel = gtk.VBox(spacing=5)
        ThemeCairoPanel.set_border_width(5)
        
        ## WINDOW
        HBoxOpacity=gtk.HBox(spacing=5)
        HBoxOpacity.pack_start(gtk.Label("Window opacity:"), False, False)
        HBoxOpacity.pack_start(self.opacity, False, False)    
        HBoxOpacity.pack_start(gtk.Label("%"), False, False)
        
        ThemeWinPanel.pack_start(HBoxOpacity, False)
        
        ##BUTTONS
        HBoxSysColor=gtk.HBox(spacing=5)
        HBoxSysColor.pack_start(self.use_system_colors)
        
        HBoxBgcolor=gtk.HBox(spacing=5)
        HBoxBgcolor.pack_start(gtk.Label("Background:"), False, False)
        HBoxBgcolor.pack_end(self.bgcolor, False, False)
        HBoxFgcolor=gtk.HBox(spacing=5)
        HBoxFgcolor.pack_start(gtk.Label("Foreground:"), False, False)
        HBoxFgcolor.pack_end(self.fgcolor, False, False)
        
        HBoxSelBgcolor=gtk.HBox(spacing=5)
        HBoxSelBgcolor.pack_start(gtk.Label("Selected background:"), False, False)
        HBoxSelBgcolor.pack_end(self.selectedbgcolor, False, False)
        HBoxSelFgcolor=gtk.HBox(spacing=5)
        HBoxSelFgcolor.pack_start(gtk.Label("Selected foreground:"), False, False)
        HBoxSelFgcolor.pack_end(self.selectedfgcolor, False, False)
        
        HBoxActBgcolor=gtk.HBox(spacing=5)
        HBoxActBgcolor.pack_start(gtk.Label("Active background:"), False, False)
        HBoxActBgcolor.pack_end(self.activebgcolor, False, False)
        HBoxActFgcolor=gtk.HBox(spacing=5)
        HBoxActFgcolor.pack_start(gtk.Label("Active foreground:"), False, False)
        HBoxActFgcolor.pack_end(self.activefgcolor, False, False)
        
        ThemeButtonPanel.pack_start(HBoxSysColor, False)
        ThemeButtonPanel.pack_start(HBoxBgcolor, False)
        ThemeButtonPanel.pack_start(HBoxFgcolor, False)
        ThemeButtonPanel.pack_start(HBoxSelBgcolor, False)
        ThemeButtonPanel.pack_start(HBoxSelFgcolor, False)
        ThemeButtonPanel.pack_start(HBoxActBgcolor, False)
        ThemeButtonPanel.pack_start(HBoxActFgcolor, False)
        
        ##CAIRO
        self.gradient_color1=ColorButtonTr("Gradient color 1", conf.gradient_color1)
        self.gradient_color2=ColorButtonTr("Gradient color 2", conf.gradient_color2)
        self.gradient_color3=ColorButtonTr("Gradient color 3", conf.gradient_color3)
        self.gradient_use_color3=gtk.CheckButton(label="Use the third color (will be the center color)")
        self.gradient_direction=gradient_direction()
        self.lightingbgcolor=ColorButtonTr("Top light color", conf.lightingcolor)
        self.show_light=gtk.CheckButton(label="Show top light")
        self.iconbordercolor=ColorButtonTr("Icon border color", conf.iconbordercolor)
        self.iconbgcolor=ColorButtonTr("Icon bg color", conf.iconbgcolor)        
        
        
        ThemeCairoPanel.pack_start(self.gradient_color1, False)
        ThemeCairoPanel.pack_start(self.gradient_color2, False)
        ThemeCairoPanel.pack_start(self.gradient_use_color3, False)
        ThemeCairoPanel.pack_start(self.gradient_color3, False)
        ThemeCairoPanel.pack_start(self.gradient_direction, False)
        ThemeCairoPanel.pack_start(self.show_light, False)
        ThemeCairoPanel.pack_start(self.lightingbgcolor, False)
        ThemeCairoPanel.pack_start(self.iconbordercolor, False)
        ThemeCairoPanel.pack_start(self.iconbgcolor, False)

        ##THEME INFO
        SaveThemePanel=gtk.VBox()
        ThemeButtonBox = gtk.HButtonBox()
        ThemeButtonBox.set_layout(gtk.BUTTONBOX_END)
        ExportTheme=gtk.Button("Export Theme")
        ExportTheme.connect("clicked", self.ExportTheme)
        SaveTheme=gtk.Button("Save Theme")
        
        SaveTheme.connect("clicked", self.SaveTheme)
        ThemeButtonBox.add(ExportTheme)
        ThemeButtonBox.add(SaveTheme)
        self.themeName=gtk.Entry()
        SaveThemePanel.pack_end(ThemeButtonBox, False)
        SaveThemePanel.pack_end(self.themeName, False)
        SaveThemePanel.pack_end(gtk.Label("Theme name:"), False)
        
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
        LoadScreenshot=gtk.Button("New")
        LoadScreenshot.connect("clicked", self.LoadScreenshot)
        ClearScreenshot=gtk.Button("Clear")
        ClearScreenshot.connect("clicked", self.ClearScreenshot)        
        ShowScreenshot=gtk.Button("Show")
        ShowScreenshot.connect("clicked", self.EnlargeScreenshot)
        ScreenshotOption.add(LoadScreenshot)
        ScreenshotOption.add(ClearScreenshot)
        ScreenshotOption.add(ShowScreenshot)
        ScreenshotPanel.pack_end(ScreenshotOption, False)
        
        DescriptionPane=gtk.VBox()
        DescriptionPane.pack_start(gtk.Label("Theme description: "), False)
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
        themeNotebook.append_page(ThemeWinPanel , gtk.Label("Window"))
        themeNotebook.append_page(ThemeButtonPanel , gtk.Label("Buttons"))
        themeNotebook.append_page(ThemeCairoPanel , gtk.Label("Background"))
        themeNotebook.append_page(SaveThemePanel , gtk.Label("Theme"))
        ##END THEME       
        
        ## THEMES AVAIBLE
        themes=gtk.VBox()
        ImportButtonBox = gtk.HButtonBox()
        ImportButtonBox.set_layout(gtk.BUTTONBOX_END)
        ImportButtonBox.set_spacing(5)
        ImportTheme=gtk.Button("Import Theme")
        ImportTheme.connect("clicked", self.ImportTheme)
        DeleteTheme=gtk.Button("Delete Theme")
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
        
        self.append_page(themes, gtk.Label("Themes"))
        editTheme=gtk.HBox()
        editTheme.add(themeNotebook)
        self.append_page(editTheme, gtk.Label("Edit Theme"))
        
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
        self.iconbordercolor.set_complete_color(conf.iconbordercolor)
        
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
        file_config+="iconbordercolor=" + self.iconbordercolor.parse_color() + "\n"
        
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
        column = gtk.TreeViewColumn ('Screenshot', cell, pixbuf = COL_ICON)
        self.append_column (column)

        cell = gtk.CellRendererText ()
        column = gtk.TreeViewColumn ('Description', cell, text = COL_NAME)
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
                    description="Theme name: " + theme + "\n\n"+description
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
        
        self.pack_start(gtk.Label("Start pos:"), False)
        self.pack_start(self.start)
        self.pack_start(gtk.Label("End pos:"), False)
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

class search_box_config(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, spacing=5)
        self.show_bar=gtk.CheckButton("Show search box")
        self.show_bar.set_active(conf.search_box_show)
        self.pack_start(self.show_bar, False)
        
        self.show_bar_top=gtk.RadioButton()
        self.show_bar_top.set_label("Top position")
        self.show_bar_bottom=gtk.RadioButton(self.show_bar_top)
        self.show_bar_bottom.set_label("Bottom position")
        self.show_bar_top.set_active(conf.search_box_top_position)
        
        self.frame_pos=gtk.Frame()
        self.frame_pos.set_label("Search box position:")
        pos=gtk.VBox()
        self.frame_pos.add(pos)
        
        pos.pack_start(self.show_bar_top, False)
        pos.pack_start(self.show_bar_bottom, False)
        
        self.pack_start(self.frame_pos, False)
        self.show_bar.connect("toggled", self.changed)
        self.changed()
        
    def changed(self, obj=None):
        self.frame_pos.set_sensitive(self.show_bar.get_active())
        
    def save_string(self):
        config=""
        if (self.show_bar.get_active()):
            config+= "search_box_show=True\n"
        else: config+= "search_box_show=False\n"
        
        if (self.show_bar_top.get_active()):
            config+= "search_box_top_position=True\n"
        else: config+= "search_box_top_position=False\n"
        
        return config
    
class top_icon_config(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)
        self.set_spacing(5)
        self.use_agm_logo=gtk.RadioButton(label="Use agm logo")
        self.use_distro_logo=gtk.RadioButton(group=self.use_agm_logo, label="Use distributor logo")
        self.use_user_login_logo=gtk.RadioButton(group=self.use_agm_logo, label="Use user login image")
        self.use_other_image=gtk.RadioButton(group=self.use_agm_logo, label="Use this image: ")
        self.use_agm_logo.set_size_request(200, -1)
        self.use_distro_logo.set_size_request(200, -1)
        self.use_user_login_logo.set_size_request(200, -1)
        self.use_other_image.set_size_request(200, -1)
        self.iconButton=gtk.Button()
        self.iconName="None"
        self.icon=gtk.Image()
        self.icon.set_from_pixbuf(utils.getPixbufFromName(self.iconName, 80, "app"))
        self.iconButton.set_image(self.icon)
        self.iconButton.connect("clicked", self.click, "set_image")

        self.show_logo=gtk.CheckButton("Show top-icon")
        self.show_logo.connect("toggled", self.changed)
        
        self.command_on_logo_clicked=gtk.Entry()
        
        self.pack_start(self.show_logo, False)
        
        self.frame_logo=gtk.Frame("Logo appearence and behaviour:")
        logos=gtk.VBox(spacing=5)
        logos.set_border_width(5)
        self.frame_logo.add(logos)
        self.pack_start(self.frame_logo, False)
        
        HBox1=gtk.HBox()
        HBox1.pack_start(self.use_agm_logo, False)
        agm_logo=gtk.Image()
        agm_logo.set_from_pixbuf(utils.getPixbufFromName(conf.default_logo_path, 80, "app"))
        HBox1.pack_start(agm_logo, False)
        logos.pack_start(HBox1, False)
        HBox4=gtk.HBox()
        HBox4.pack_start(self.use_distro_logo, False)
        distro_logo=gtk.Image()
        distro_logo.set_from_pixbuf(utils.getPixbufFromName("distributor-logo", 80, "app"))
        HBox4.pack_start(distro_logo, False)
        logos.pack_start(HBox4, False)
        HBox2=gtk.HBox()
        HBox2.pack_start(self.use_user_login_logo, False)
        user_logo=gtk.Image()
        user_logo.set_from_pixbuf(utils.getPixbufFromName(conf.home_logo_path, 80, "app"))
        HBox2.pack_start(user_logo, False)
        logos.pack_start(HBox2, False)
        HBox3=gtk.HBox()
        HBox3.pack_start(self.use_other_image, False)
        HBox3.pack_start(self.iconButton, False)
        logos.pack_start(HBox3, False)
        
        label=set_label_size_and_align(gtk.Label("Command to launch when left-click on the logo :"), 250)
        logos.pack_start(label, False)
        logos.pack_start(self.command_on_logo_clicked, False)
        
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
                self.icon.set_from_pixbuf(utils.getPixbufFromName(self.iconName, 80, "app"))
                self.iconButton.set_image(self.icon)
    
    def load_config(self):
        if (conf.top_icon_mode==conf.USE_USER_LOGO):
            self.use_user_login_logo.set_active(True)
        elif (conf.top_icon_mode==conf.USE_DISTRO_LOGO):
            self.use_distro_logo.set_active(True)
        elif (conf.top_icon_mode==conf.USE_OTHER_LOGO):
            self.use_other_image.set_active(True)
        else:
            self.use_agm_logo.set_active(True)
        
        self.show_logo.set_active(conf.top_icon_show_logo)
        
        if conf.top_icon_other_logo!=None and os.path.isfile(conf.top_icon_other_logo):
            self.iconName=conf.top_icon_other_logo
            self.icon.set_from_pixbuf(utils.getPixbufFromName(self.iconName, 80, "app"))
        self.command_on_logo_clicked.set_text(conf.command_on_logo_clicked)
        
    def to_string(self):
        config=""
        if self.use_user_login_logo.get_active():
            config+="top_icon_mode=" + conf.USE_USER_LOGO + "\n"
        elif self.use_distro_logo.get_active():
            config+="top_icon_mode=" + conf.USE_DISTRO_LOGO + "\n"   
        elif self.use_other_image.get_active():
            config+="top_icon_mode=" + conf.USE_OTHER_LOGO + "\n"        
        else:
            config+="top_icon_mode=" + conf.USE_AGM_LOGO + "\n"
        
        if  self.show_logo.get_active():
            config+="top_icon_show_logo=True\n"
        else: config+="top_icon_show_logo=False\n"
        
        config+="top_icon_other_logo=" + self.iconName + "\n"
        
        config+="command_on_logo_clicked="+ self.command_on_logo_clicked.get_text()+"\n"
        
        return config

#This should config the fast option buttons.
class other_option_config(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)
        # Use fast-buttons
        # Use right-click->Menu
        # No other options.
        
        # Fast buttons config
        # Right align
        # Left align
        # 4 corners align
        # Button size.

class menu(gtk.Notebook):
    def __init__(self):
        gtk.Notebook.__init__(self)
        self.menu_behaviour=behavior()
        self.menu_behaviour.set_border_width(5)
        self.menu_elements=config_plugin()
        self.menu_elements.set_border_width(5)
        
        self.append_page(self.menu_behaviour, gtk.Label("Behaviour"))
        self.append_page(self.menu_elements, gtk.Label("Elements"))
    
    def save_string(self):
        return self.menu_behaviour.save_string() + self.menu_elements.save_string()