from AGM.AGM_Fav_app_model import model
from AGM.AGM_Fav_app import FavApp
import gtk

class Model(model):
    def __init__(self):
        model.__init__(self)
        self.model_code_name="Custom"
        self.to_execute=""
    
    def get_fav_app(self):
        command=AskNewCustomCommand().get_command()
        if command!=None:
            (name, icon, tooltip, command)=command
            return FavApps(name, icon, tooltip, command.split(" "))
        return None
        
    def get_from_string(self, string):
        string=string.split("#")
        print string
        if len(string)>=4:
            self.to_execute=string[3]
            return FavApp(string[0], string[1], string[2], string[3].split(" "))
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
        
        VBox=gtk.VBox()
        VBox.add(self.text)
        VBox.add(self.icon)
        VBox.add(self.command)
        VBox.add(self.name)
        
        self.add(VBox)
        self.show_all()
        gtk.main()
    
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