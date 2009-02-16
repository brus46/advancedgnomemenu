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
