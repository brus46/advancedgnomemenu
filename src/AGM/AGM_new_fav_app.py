import gtk
import AGM_Fav_app_models
import AGM_utils as utils

class newFavApp():
    def __init__(self):
        print "newFavApp"
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
        self.set_title("Select Model")
        self.list=ModelList()
        self.model=None
        okButton=gtk.Button("ok")
        cancelButton=gtk.Button("cancel")
        ButtonBox=gtk.HButtonBox()
        ButtonBox.add(okButton)
        okButton.connect("clicked", self.okButton)
        ButtonBox.add(cancelButton)
        cancelButton.connect("clicked", self.cancelButton)
        VBox.pack_end(ButtonBox, False)
        VBox.pack_start(self.list)
        self.add(VBox)
        
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
        column = gtk.TreeViewColumn ('Model', cell, text = COL_NAME)
        self.append_column (column)
        
        cell = gtk.CellRendererText ()
        column = gtk.TreeViewColumn ('Description', cell, text = COL_DESCR)
        self.append_column (column)
        
        self.load()
    
    def load(self):
        list=AGM_Fav_app_models.get_child_models()
        for el in list:
            model=list[el]
            self.model.append([utils.getPixbufFromName(model.model_icon, 48, "app"), model.model_name, model.model_description, model.model_code_name])
    
    def get_selected(self):
        model, iter = self.treeselection.get_selected()
        if iter:
           return model.get_value (iter, 3)
        return None
        
    def clean_list(self):
        self.model.clear()
        pass