import gtk
from AG_commons import utils
from Tooltips import Tooltip
from Config import config
conf=config()

class IndexButton(gtk.Button):
    def __init__(self, icon, string, parent):
        gtk.Button.__init__(self)
        self.parent_menu=parent
        self.text=string
        self.set_label("")
        self.image=gtk.Image()
        self.image.set_from_pixbuf(utils.getPixbufFromName(icon, 22, "app"))
        self.set_image(self.image)
        #self.set_size_request(conf.app_size, -1)
        self.tooltip=Tooltip(string)
        self.connect("enter_notify_event", self.show_tooltip)
        self.connect("leave-notify-event", self.hide_tooltip)
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
                    label.set_text(self.text)
                    label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor_clicked))
            self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.bgcolor_clicked))
        else:
            self.set_relief(gtk.RELIEF_NONE)
            self.set_image(self.image)
            for child in self.get_children():
                for child2 in child.get_children():
                    label=child2.get_children()[1]
                    label.set_text("")
                    label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor))
    def get_active(self):
        return self.get_relief()==gtk.RELIEF_NORMAL
    
    def show_tooltip(self, obj, event):
        if self.get_active()==False:
            h=(conf.app_size_mini)
            screen=self.get_screen()
            x=self.allocation.x
            x+=(screen.get_width()-conf.win_width_mini)/2
            if conf.position=='top':
                self.tooltip.set_gravity(gtk.gdk.GRAVITY_NORTH_WEST)
                self.tooltip.move(x, h)
            else:
                self.tooltip.set_gravity(gtk.gdk.GRAVITY_SOUTH_WEST)
                self.tooltip.move(x, h)
            self.tooltip.show_all()
    
    def hide_tooltip(self, obj, event):
        self.tooltip.hide()