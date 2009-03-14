import gtk
from AG_commons import GnomeMenuUtils
from AG_commons import utils
import MenuButton

class MenuBar(gtk.HBox):
    def __init__(self, close, max=5):
        gtk.HBox.__init__(self)
        self.set_size_request(-1, 50)
        self.Menu=GnomeMenuUtils.GnomeMenu()
        self.menu=[]
        self.max=max
        self.close=close
        print max
        position=0

    def show_parent(self, parent):
        self.clean()
        self.get_parent(parent)
        i=0
        for el in self.menu:
            if i<self.max:
                newItem=MenuButton.MenuButton(el["icon"], el["tooltip"])
                newItem.connect("clicked", self.execute, el["exec"])
                self.pack_start(newItem, False)
                i+=1
            else: break
    
    def clean(self):
        self.menu=[]
        for child in self.get_children():
            self.remove(child)
    
    def get_parent(self, parent):
        for item in self.Menu.get_items(parent):
            name = item.get_name()
            icon = self.getIcon(item)
            exec_string=item.get_exec()
            self.menu.append({
                      "icon":icon, 
                      "exec":exec_string,
                      "tooltip":name})
        
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
    
    def execute(self, obj, command):
        utils.ExecCommand(command)
        self.close()