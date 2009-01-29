import gtk
from AGM_default_config import conf as config
conf=config()
import AGM_Fav_app_models
import AGM_Fav_app
import AGM_utils as utils

class FavAppsBar(gtk.HBox):
    def __init__(self, hide_f):
        gtk.HBox.__init__(self)
        self.hide_f=hide_f
        self.content=gtk.VBox()
        if conf.fav_apps_orientation=="H":
            content=gtk.HBox()
            
        self.add(self.content)
        
        self.read_file()
        
        self.show_all()
    
    def clear(self):
        for child in self.content.get_children():
            self.content.remove(child)
    
    def read_file(self):
        print "Reading fav apps"
        self.clear()
        conf.read_fav_apps()
        fav_apps=conf.fav_apps
        for fav_app in fav_apps:
            newFA=AGM_Fav_app.FavApp(fav_app["name"],fav_app["icon"],fav_app["tooltip"],fav_app["command"])
            if newFA!=None:
                self.content.pack_start(newFA, False)
                newFA.connect("clicked", self.action)
  
    
    def action(self, obj):
        utils.ExecCommand(obj.FA_command.split(" "))
        if conf.hide_on_program_launch:
            self.hide_f()
            
    def modify_bg(self, state, color):
        for child in self.content.get_children():
            child.modify_bg(state, color)
    
    def modify_fg(self, state, color):
        for child in self.content.get_children():
            child.modify_fg(state, color)
    