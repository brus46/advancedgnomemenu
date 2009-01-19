import gtk
from AGM_default_config import conf as config
conf=config()
import AGM_Fav_app_models
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
            print fav_app["model"]
            Model=AGM_Fav_app_models.get_model(fav_app["model"])
            if Model!=None:
                string=fav_app["name"] + "#" + fav_app["icon"] + "#" + fav_app["tooltip"] + "#" + fav_app["command"]
                print string
                newFA=Model.get_from_string(string)
                if newFA!=None:
                    self.content.pack_start(newFA, False)
                    newFA.connect("clicked", self.action)
  
    
    def action(self, obj):
        utils.ExecCommand(obj.command)
        if conf.hide_on_program_launch:
            self.hide_f()
            
    def modify_bg(self, state, color):
        for child in self.content.get_children():
            child.modify_bg(state, color)
    
    def modify_fg(self, state, color):
        for child in self.content.get_children():
            child.modify_fg(state, color)
    