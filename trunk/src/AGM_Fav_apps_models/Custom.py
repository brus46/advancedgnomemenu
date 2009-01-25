from AGM.AGM_Fav_app_model import model
from AGM.AGM_Fav_app import FavApp
import gtk, os
import AGM.AGM_utils as utils
import AGM.localization
_=AGM.localization.Translate

class Model(model):
    def __init__(self):
        model.__init__(self)
        self.model_code_name="Custom"
        self.model_icon="gtk-preferences"
        self.model_name=_("Pick a custom application")
        self.model_description=_("Link to a custom application")
    
    def get_fav_app(self):
        command=AskNewCustomCommand().get_command()
        if command!=None:
            (name, icon, tooltip, command)=command
            return FavApp(name, icon, tooltip, command)
        return None

def get_label(text):
    label=gtk.Label(text+":")
    label.set_size_request(80, -1)
    return label
           
class AskNewCustomCommand(gtk.Window):
    def __init__(self, text=None, icon=None, tooltip=None, command=None):
        gtk.Window.__init__(self)
        self.text=gtk.Entry()
        self.icon=gtk.Button()
        self.iconname="app"
        self.command=gtk.Entry()
        self.tooltip=gtk.Entry()
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
        
        VBox=gtk.VBox(spacing=5)
        HBox=gtk.HBox()
        HBox.pack_start(get_label(_("Name")), False)
        HBox.pack_end(self.text)
        VBox.pack_start(HBox, False)
        HBox=gtk.HBox()
        HBox.pack_start(get_label(_("Icon")), False)
        HBox.pack_start(self.icon, False)
        self.icon.connect("clicked", self.change_icon)
        self.icon.set_size_request(60, 60)
        VBox.pack_start(HBox, False)
        HBox=gtk.HBox()
        HBox.pack_start(get_label(_("Tooltip")), False)
        HBox.pack_end(self.tooltip)
        VBox.pack_start(HBox, False)
        HBox=gtk.HBox()
        HBox.pack_start(get_label(_("Command")), False)
        HBox.pack_end(self.command)
        self.command.connect("changed", self.text_changed)
        VBox.pack_start(HBox, False)
        
        VBox.pack_end(HButtonBox, False)
        self.set_icon()
        self.add(VBox)
        
        self.set_title(_("Add custom command"))
        self.set_icon_list(utils.getPixbufFromName("gtk-preferences", 16, "app"))
        self.set_resizable(False)
        self.set_modal(True)
        self.set_size_request(300, 200)
        self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        
        self.show_all()
        gtk.main()
    
    def text_changed(self, obj):
        if utils.searchPictureFromName(self.command.get_text())==True:
            self.iconname=self.command.get_text()
            self.set_icon()
        
    def change_icon(self, obj):
        icon=utils.OpenImage().get_file()
        if os.path.isfile(icon)==True:
            self.iconname=icon
            self.set_icon()
    
    def set_icon(self):
        image=gtk.Image()
        pixbuf=utils.getPixbufFromName(self.iconname, 48, "app")
        image.set_from_pixbuf(pixbuf)
        self.icon.set_image(image)
    
    def get_command(self):
        if self.cancel:
            return None
        return (self.text.get_text(), self.iconname, self.tooltip.get_text(), self.command.get_text())
    
    def ok_pressed(self, obj):
        self.hide()
        gtk.main_quit()
    
    def cancel_pressed(self, obj):
        self.cancel=True
        self.hide()
        gtk.main_quit()
