import gtk, cairo
from AG_commons import utils

class MenuButton(gtk.Button):
    def __init__(self, icon, tooltip):
        gtk.Button.__init__(self)
        self.set_relief(gtk.RELIEF_NONE)
        self.icon=icon
        self.tooltip=tooltip
        self.image=gtk.Image()
        self.image.set_from_pixbuf(utils.getPixbufFromName(icon, 35, "app"))
        #self.set_from_pixbuf(utils.getPixbufFromName(icon, 48, "app"))
        self.set_image(self.image)
        #self.connect("expose_event", self.on_expose)
        #self.connect("motion_notify_event", self.on_expose)

        #self.img=utils.getPixbufFromName(icon, 48, "app")
        self.set_tooltip_text(self.tooltip)
        
        self.set_size_request(55, 55)
        pass
    