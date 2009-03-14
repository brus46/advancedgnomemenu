import gtk
from AG_commons import utils
from Config import config
conf=config()

class IndexButton(gtk.Button):
    def __init__(self, icon, string, parent):
        gtk.Button.__init__(self)
        self.parent_menu=parent
        self.set_label(string)
        self.image=gtk.Image()
        self.image.set_from_pixbuf(utils.getPixbufFromName(icon, 22, "app"))
        self.set_image(self.image)
        self.set_size_request(conf.app_size, -1)
        self.set_relief(gtk.RELIEF_NONE)
        for child in self.get_children():
            for child2 in child.get_children():
                label=child2.get_children()[1]
                label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor))

    def set_active(self, active):
        if active:
            self.set_relief(gtk.RELIEF_NORMAL)
            self.set_image(self.image)
            for child in self.get_children():
                for child2 in child.get_children():
                    label=child2.get_children()[1]
                    label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor_clicked))
            self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.bgcolor_clicked))
        else:
            self.set_relief(gtk.RELIEF_NONE)
            self.set_image(self.image)
            for child in self.get_children():
                for child2 in child.get_children():
                    label=child2.get_children()[1]
                    label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor))
    def get_active(self):
        return self.get_relief()==gtk.RELIEF_NORMAL
        