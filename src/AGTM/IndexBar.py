import gtk
from AG_commons import GnomeMenuUtils
from IndexButton import IndexButton

class IndexBar(gtk.HBox):
    def __init__(self, show_big, show_little):
        gtk.HBox.__init__(self)
        self.show_big=show_big
        self.show_little=show_little
        self.Menu=GnomeMenuUtils.GnomeMenu()
        self.apps=self.Menu.get_apps()
        self.buttons=[]
        for app in self.apps:
            newButton=IndexButton(self.Menu.getIcon(app), app.get_name(), app)
            newButton.connect("clicked", self.toggled)
            self.buttons.append(newButton)
            self.pack_start(newButton, False)
    
    def toggled(self, obj):
        if obj.get_active():
            obj.set_active(False)
            self.show_little()
        else:
            for child in self.buttons:
                if obj!=child:
                    child.set_active(False)
            obj.set_active(True)
            self.show_big(obj.parent_menu)
    
    def refresh(self, close_all=False):
        for child in self.buttons:
            if close_all:
                child.set_active(False)
            else:
                child.set_active(child.get_active())
