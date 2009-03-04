from AGM.AGM_Fav_app_model import model
from AGM.AGM_Fav_app import FavApp
import gtk, os
import AGM.AGM_utils as utils
from AGM.GnomeMenuUtils import GnomeMenu
import AGM.localization
_=AGM.localization.Translate

class Model(model):
    def __init__(self):
        model.__init__(self)
        self.model_code_name="FromMenu"
        self.model_icon="gtk-preferences"
        self.model_name=_("The GNOME menu")
        self.model_description=_("Pick an application already in the GNOME Menu")
    
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
        
        okButton=gtk.Button(gtk.STOCK_OK)
        okButton.set_use_stock(True)
        cancelButton=gtk.Button(gtk.STOCK_CANCEL)
        cancelButton.set_use_stock(True)
        okButton.connect("clicked", self.ok_pressed)
        cancelButton.connect("clicked", self.cancel_pressed)
        
        HButtonBox=gtk.HButtonBox()
        HButtonBox.set_layout(gtk.BUTTONBOX_END)
        HButtonBox.set_spacing(5)
        HButtonBox.add(okButton)
        HButtonBox.add(cancelButton)
        
        Scroll=gtk.ScrolledWindow()
        self.list=AppList()
        Scroll.add_with_viewport(self.list)
        
        VBox=gtk.VBox(spacing=5)
        VBox.set_border_width(5)
        
        HBox=gtk.HBox(spacing=5)
        HBox.pack_start(gtk.Label(_("Search")+" :"), False)
        self.SearchBox=gtk.Entry()
        self.SearchBox.connect("changed", self.Search)
        
        HBox.add(self.SearchBox)
        
        VBox.pack_start(HBox, False)
        VBox.pack_start(gtk.Label(_("Select program to add")+" :"), False)
        VBox.pack_start(Scroll)
        VBox.pack_end(HButtonBox, False)
        self.add(VBox)
        
        self.set_title(_("Add Fav app from menu."))
        self.set_icon_list(utils.getPixbufFromName("gtk-preferences", 16, "app"))
        self.set_resizable(False)
        self.set_modal(True)
        self.set_size_request(300, 400)
        self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.show_all()
        gtk.main()
    
    def Search(self, obj):
        #print "Search ", self.SearchBox.get_text()
        self.list.search(self.SearchBox.get_text())
        
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
        
        self.Menu=GnomeMenu()
        self.list=self.recursive_search()
        #self.list.sort()
        
        self.model = gtk.ListStore (gtk.gdk.Pixbuf, str)
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
        self.search("")
    
    def get_selected(self):
        model, iter = self.treeselection.get_selected()
        if iter:
            id=model.get_value (iter, 1)
            return (self.list[id]["name"], self.list[id]["icon"], self.list[id]["tooltip"], self.list[id]["command"])
        return None
        
    def clean_list(self):
        self.model.clear()
        pass
    
    def search(self, text=""):
        self.clean_list()
        keys=self.list.keys()
        keys.sort()
        if text=="":
            for nameel in keys:
                el=self.list[nameel]
                self.model.append([utils.getPixbufFromName(el["icon"], 48, "app"), el["name"]])
        else:
            for el in keys:
                el=self.list[el]
                if el["name"].lower().find(text.lower())>=0:
                    self.model.append([utils.getPixbufFromName(el["icon"], 48, "app"), el["name"]])
    
    def recursive_search(self, obj=None):
        found={}
        if obj==None:
            for menu in self.Menu.get_menus():
                newfound=self.recursive_search(menu)
                for newel in newfound:
                    
                    found[newel]=newfound[newel]
        else:
            for menu in self.Menu.get_menus(obj):
                newfound=self.recursive_search(menu)
                for newel in newfound:
                    found[newel]=newfound[newel]
            for item in self.Menu.get_items(obj):
                name = item.get_name()
                icon = self.getIcon(item)
                exec_string=item.get_exec()
                found[name]={"icon":icon, 
                          "name":name,
                          "command":exec_string,
                          "tooltip":name}
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
