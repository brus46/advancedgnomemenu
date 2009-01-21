import gtk
import AGM_Fav_app_models
import AGM_utils as utils
import localization
_=localization.Translate

class newFavApp():
    def __init__(self):
        self.fav_app=None
        Model=selectModule().get_model()
        if Model!=None:
            self.fav_app=Model.get_fav_app()
    
    def get_new_fav_app(self):
        return self.fav_app
    
class selectModule(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        VBox=gtk.VBox()
        self.set_title(_("Select Model"))
        self.list=ModelList()
        self.model=None
        okButton=gtk.Button(gtk.STOCK_OK)
        okButton.set_use_stock(True)
        cancelButton=gtk.Button(gtk.STOCK_CANCEL)
        cancelButton.set_use_stock(True)
        ButtonBox=gtk.HButtonBox()
        ButtonBox.set_layout(gtk.BUTTONBOX_END)
        ButtonBox.set_spacing(5)
        ButtonBox.add(okButton)
        okButton.connect("clicked", self.okButton)
        ButtonBox.add(cancelButton)
        cancelButton.connect("clicked", self.cancelButton)
        VBox.pack_end(ButtonBox, False)
        Scroll=gtk.ScrolledWindow()
        Scroll.add_with_viewport(self.list)
        VBox.pack_start(Scroll)
        self.add(VBox)
        
        self.set_size_request(500, 400)
        self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.set_icon_list(utils.getPixbufFromName("gtk-preferences", 16, "app"))
        self.set_resizable(False)
        self.set_modal(True)
        
        self.show_all()
        gtk.main()
    
    def okButton(self, obj):
        print self.list.get_selected()
        self.model=AGM_Fav_app_models.get_model(self.list.get_selected())
        self.cancelButton(obj)
    
    def cancelButton(self, obj):
        self.hide_all()
        gtk.main_quit()
    
    def get_model(self):
        return self.model
    
class ModelList(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)
        
        self.model = gtk.ListStore (gtk.gdk.Pixbuf, str, str, str)
        COL_ICON, COL_NAME, COL_DESCR, COL_CODE = (0, 1, 2, 3)
        
        self.set_model(self.model)
        self.treeselection = self.get_selection()
        self.treeselection.set_mode (gtk.SELECTION_SINGLE)

        cell = gtk.CellRendererPixbuf ()
        column = gtk.TreeViewColumn ('#', cell, pixbuf = COL_ICON)
        self.append_column (column)
    
        cell = gtk.CellRendererText ()
        column = gtk.TreeViewColumn (_('Model'), cell, text = COL_NAME)
        self.append_column (column)
        
        cell = gtk.CellRendererText ()
        column = gtk.TreeViewColumn (_('Description'), cell, text = COL_DESCR)
        self.append_column (column)
        
        self.load()
    
    def load(self):
        list=AGM_Fav_app_models.get_child_models()
        name_list=[]
        for el in list: name_list.append(el)
        name_list.sort()
        for el in name_list:
            model=list[el]
            self.model.append([utils.getPixbufFromName(model.model_icon, 48, "app"), model.model_name, model.model_description, model.model_code_name])
    
    def get_selected(self):
        model, iter = self.treeselection.get_selected()
        if iter:
           return model.get_value (iter, 3)
        return None
        
    def clean_list(self):
        self.model.clear()