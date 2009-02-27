import gtk
from AGL.CairoWin import TransparentWindow
from AGM.AGM_Fav_apps_bar import FavAppsBar

class Launcher():
    def __init__(self):
        self.win=TransparentWindow()
        
        self.container=gtk.VBox()
        self.win.add(self.container)
        
        self.fa_bar=FavAppsBar(hide_f=self.hide, force_H=True)
        HBox=gtk.HBox()
        spacing_label1=gtk.Label()
        spacing_label1.set_size_request(15, 15)
        spacing_label2=gtk.Label()
        spacing_label2.set_size_request(15, 15)
        HBox.pack_start(spacing_label1, False)
        HBox.add(self.fa_bar)
        HBox.pack_end(spacing_label2, False)
        
        self.container.add(gtk.Label())
        
        self.container.pack_end(HBox, False, False)
        
        self.win.show_all()
        self.win.set_size_request(350, 250)
        
        gtk.main()
    
    def hide(self):
        self.win.hide()
        gtk.main_quit()