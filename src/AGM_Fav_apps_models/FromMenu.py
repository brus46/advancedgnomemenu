from AGM.AGM_Fav_app_model import model
from AGM.AGM_Fav_app import FavApp
import gtk, os
import AGM.AGM_utils as utils
from Alacarte.MenuEditor import MenuEditor
from Alacarte import util
import gmenu, cgi, sys

class Model(model):
    def __init__(self):
        model.__init__(self)
        self.model_code_name="FromMenu"
        self.model_icon="gtk-preferences"
        self.model_name="Get fav app from the menu."
        self.model_description="Use this if you want to create a fav app from an existing app in the menu."
    
    def get_fav_app(self):
        command=AskNewCustomCommand().get_command()
        if command!=None:
            (name, icon, tooltip, command)=command
            return FavApp(name, icon, tooltip, command)
        return None
                
class AskNewCustomCommand(gtk.Window):
    def __init__(self, text=None, icon=None, tooltip=None, command=None):
        gtk.Window.__init__(self)
        self.text=""
        self.iconname="app"
        self.command=""
        self.tooltip=""
        self.cancel=False
        
        okButton=gtk.Button("Ok")
        okButton.connect("clicked", self.ok_pressed)
        cancelButton=gtk.Button("Cancel")
        cancelButton.connect("clicked", self.cancel_pressed)
        HButtonBox=gtk.HButtonBox()
        HButtonBox.add(okButton)
        HButtonBox.add(cancelButton)
        
        Scroll=gtk.ScrolledWindow()
        self.list=AppList()
        Scroll.add_with_viewport(self.list)
        
        VBox=gtk.VBox()
        
        VBox.pack_start(Scroll)
        VBox.pack_end(HButtonBox, False)
        self.add(VBox)
        
        self.set_title("Add Fav app from menu.")
        self.set_size_request(500, 400)
        self.show_all()
        gtk.main()
    def get_command(self):
        if self.cancel:
            return None
        if None!=self.list.get_selected():
            return self.list.get_selected()
    
    def ok_pressed(self, obj):
        self.hide()
        gtk.main_quit()
    
    def cancel_pressed(self, obj):
        self.cancel=True
        self.hide()
        gtk.main_quit()

class AppList(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)
        
        self.editor=MenuEditor()
        self.list=self.recursive_search()
        self.list.sort()
        
        self.model = gtk.ListStore (gtk.gdk.Pixbuf, str, int)
        COL_ICON, COL_NAME, COL_INDEX = (0, 1, 2)
        
        self.set_model(self.model)
        self.treeselection = self.get_selection()
        self.treeselection.set_mode (gtk.SELECTION_SINGLE)

        cell = gtk.CellRendererPixbuf ()
        column = gtk.TreeViewColumn ('#', cell, pixbuf = COL_ICON)
        self.append_column (column)
    
        cell = gtk.CellRendererText ()
        column = gtk.TreeViewColumn ('Model', cell, text = COL_NAME)
        self.append_column (column)
        
        self.load()
    
    def load(self):
        
        index=0
        for el in self.list:
            self.model.append([utils.getPixbufFromName(el["icon"], 48, "app"), el["name"], index])
            index+=1
    
    def get_selected(self):
        model, iter = self.treeselection.get_selected()
        if iter:
            id=model.get_value (iter, 2)
            return (self.list[id]["name"], self.list[id]["icon"], self.list[id]["tooltip"], self.list[id]["command"])
        return None
        
    def clean_list(self):
        self.model.clear()
        pass

    def recursive_search(self, obj=None):
        found=[]
        if obj==None:
            for menu in self.editor.getMenus():
                newfound=self.recursive_search(menu)
                for newel in newfound:
                    found.append(newel)
        else:
            for menu, show in self.editor.getMenus(obj):
                if show:
                    newfound=self.recursive_search(menu)
                    for newel in newfound:
                        found.append(newel)
            for item, show in self.editor.getItems(obj):
                if show and item.get_type() == gmenu.TYPE_ENTRY:
                    name = item.get_name()
                    icon = self.getIcon(item)
                    exec_string=item.get_exec()
                    #print exec_string
                    found.append({
                              "icon":icon, 
                              "name":name,
                              "command":exec_string,
                              "tooltip":name})
        return found    

    def getIcon(self, item):
        pixbuf = None
        if item == None:
            return None
        if isinstance(item, str):
            iconName = item
        else:
            iconName = item.get_icon()
        if iconName and not '/' in iconName and iconName[-3:] in ('png', 'svg', 'xpm'):
            iconName = iconName[:-4]
        icon_theme = gtk.icon_theme_get_default()
        return iconName