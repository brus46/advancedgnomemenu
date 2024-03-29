from AGTM import CairoWin, IndexBar, MenuBar
from AGTM.Config import config

conf=config()
import gtk

class MainWindow():
    def __init__(self):
        self.win=CairoWin.TransparentWindow()
        self.IndexBar=IndexBar.IndexBar(self.big_bar, self.little_bar)
        self.MenuBar=MenuBar.MenuBar(self.little_bar, int(conf.win_width/55))
        
        self.win.set_size_request(conf.win_width_mini, conf.win_height)
        
        self.screen = self.win.get_screen()
        if conf.position=="top":
            self.win.move((self.screen.get_width()-conf.win_width_mini)/2, 0)
        else: self.win.move((self.screen.get_width()-conf.win_width_mini)/2, (self.screen.get_height()-conf.win_height))
        
        self.VBox=gtk.VBox(spacing=5)
        self.win.add(self.VBox)
        
        
        self.VBox.pack_start(self.IndexBar, False)
        self.VBox.pack_start(self.MenuBar, False)        
        
        self.win.show_all()
        self.little_bar()
        self.win.connect("focus-out-event", self.little_bar)
        gtk.main()
    
    def little_bar(self, obj=None, event=None):
        self.MenuBar.clean()
        self.MenuBar.hide()
        self.IndexBar.refresh(close_all=True)
        if self.win.mini==False:
            self.win.mini=True
            self.win.set_size_request(conf.win_width_mini, conf.win_height)
            if conf.position=="top":
                self.win.move((self.screen.get_width()-conf.win_width_mini)/2, 0)
            else: self.win.move((self.screen.get_width()-conf.win_width_mini)/2, (self.screen.get_height()-conf.win_height))
            self.win.do_expose_event()
    
    def big_bar(self, parent):
        if self.win.mini==True:
            self.win.mini=False
            self.win.set_size_request(conf.win_width, conf.win_height)
            if conf.position=="top":
                self.win.move((self.screen.get_width()-conf.win_width)/2, 0)
            else: self.win.move((self.screen.get_width()-conf.win_width)/2, (self.screen.get_height()-conf.win_height))
            self.win.do_expose_event()
        self.MenuBar.show_parent(parent)
        self.MenuBar.show_all()
        self.IndexBar.refresh()