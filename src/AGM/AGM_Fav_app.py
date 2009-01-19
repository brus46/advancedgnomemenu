import gtk
import AGM_utils as utils
from AGM_default_config import conf as config
conf=config()

class FavApp(gtk.Button):
    def __init__(self, text, icon, tooltip, command):
        gtk.Button.__init__(self)
        self.command=command
        show_text=conf.fav_apps_show_text
        image=gtk.Image()
        image.set_from_pixbuf(utils.getPixbufFromName(icon, conf.fav_apps_icon_dimension, "app"))
        content=gtk.HBox()
        content.pack_start(image, False)
        if (conf.fav_apps_show_text): 
            if conf.fav_apps_text_bold:
                self.label=gtk.Label("<b>" + text + "</b>")
            else: self.label=gtk.Label(text)
            self.label.set_justify(gtk.JUSTIFY_LEFT)
            self.label.set_use_markup(True)
            self.label.set_size_request(100, conf.fav_apps_icon_dimension)
            content.pack_start(self.label, True)
        content.pack_start(gtk.Label())
        self.add(content)
        self.set_tooltip_text(tooltip)
        self.set_relief(gtk.RELIEF_NONE)
        self.show()
        
    def modify_fg(self, state, color):
        self.label.modify_fg(state, color)