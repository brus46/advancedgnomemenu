from AGM.AGM_Fav_app_model import model
from AGM.AGM_Fav_app import FavApp
import gtk, os
import AGM.AGM_utils as utils

class Model(model):
    def __init__(self):
        model.__init__(self)
        self.model_code_name="Custom"
        self.model_icon="gtk-preferences"
        self.model_name="Custom fav app"
        self.model_description="Use this if you want to create a custom fav app"
    
    def get_fav_app(self):
        command=AskNewCustomCommand().get_command()
        if command!=None:
            (name, icon, tooltip, command)=command
            return FavApp(name, icon, tooltip, command.split(" "))
        return None
                
class AskNewCustomCommand(gtk.Window):
    def __init__(self, text=None, icon=None, tooltip=None, command=None):
        gtk.Window.__init__(self)
        self.text=gtk.Entry()
        self.icon=gtk.Button()
        self.iconname="app"
        self.command=gtk.Entry()
        self.tooltip=gtk.Entry()
        self.cancel=False
        
        okButton=gtk.Button("Ok")
        okButton.connect("clicked", self.ok_pressed)
        cancelButton=gtk.Button("Cancel")
        cancelButton.connect("clicked", self.cancel_pressed)
        HButtonBox=gtk.HButtonBox()
        HButtonBox.add(okButton)
        HButtonBox.add(cancelButton)
        
        
        VBox=gtk.VBox()
        HBox=gtk.HBox()
        HBox.pack_start(gtk.Label("Name"))
        HBox.pack_end(self.text)
        VBox.add(HBox)
        HBox=gtk.HBox()
        HBox.pack_start(gtk.Label("Icon"))
        HBox.pack_end(self.icon)
        self.icon.connect("clicked", self.change_icon)
        VBox.add(HBox)
        HBox=gtk.HBox()
        HBox.pack_start(gtk.Label("Tooltip"))
        HBox.pack_end(self.tooltip)
        VBox.add(HBox)
        HBox=gtk.HBox()
        HBox.pack_start(gtk.Label("Command"))
        HBox.pack_end(self.command)
        self.command.connect("changed", self.text_changed)
        VBox.add(HBox)
        
        VBox.pack_end(HButtonBox, False)
        self.set_icon()
        self.add(VBox)
        
        self.set_title("Add custom command")
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