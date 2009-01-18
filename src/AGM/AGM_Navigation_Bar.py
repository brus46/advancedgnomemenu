import gtk
import AGM_Navigation_Button as Button
import AGM.AGM_utils as utils
from AGM.AGM_default_config import conf as config
conf=config()
class NavBar(gtk.HBox):
    def __init__(self, get_gradient, history=([], [])):
        gtk.HBox.__init__(self, spacing=5)
        self.history, self.history_icon=history
        self.go_home=None
        self.goto=None
        self.get_gradient=get_gradient
        self.update(self.history, self.history_icon)
    
    def set_functions(self, go_home, goto):
        self.go_home=go_home
        self.goto=goto
    
    def update(self, history, history_icon):
        print history
        self.history=history
        self.history_icon=history_icon
        for child in self.get_children():
            self.remove(child)
        i=0
        if len(self.history_icon)>0:
            for step in self.history_icon:
                i+=1
                if i==len(self.history_icon):
                    newButton=Button.NavButton(self.get_gradient, utils.getPixbufFromName(step["icon"], conf.menu_bar_icon_h, "folder"), step["name"], True)    
                    newButton.connect("button-press-event", self.clicked, i)
                else:
                    if step!=None:
                        newButton=Button.NavButton(self.get_gradient, utils.getPixbufFromName(step["icon"], conf.menu_bar_icon_h, "folder"), step["name"])
                        newButton.connect("button-press-event", self.clicked, i)
                    else:
                        newButton=Button.NavButton(self.get_gradient, utils.getPixbufFromName("user-home", conf.menu_bar_icon_h, "folder"), "Menu")
                        newButton.connect("button-press-event", self.clicked, -1)
                    newButton.set_size_request(conf.menu_bar_h, conf.menu_bar_h)
                self.pack_end(newButton, i==len(history_icon))
        else:
            newButton=Button.NavButton(self.get_gradient, utils.getPixbufFromName("user-home", conf.menu_bar_icon_h, "folder"), "Menu", True)
            newButton.connect("button-press-event", self.clicked, -1)
            self.pack_end(newButton)
        self.show_all()
    
    def clicked(self, obj, event, index):
        if event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                if index<0 or index>=len(self.history) or self.history[index]==None:
                    if self.go_home!=None: self.go_home()
                else:
                    if self.goto!=None: self.goto(index)