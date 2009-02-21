
import gtk
import AGM.AGM_utils as utils
import AGM.AGM_default_config
import AGM.localization

conf=AGM.AGM_default_config.conf()
_=AGM.localization.Translate



class Configure(gtk.Window):
    def __init__(self):     
        gtk.Window.__init__(self)
        
        self.set_title(_("Configure file browsing"))
        self.set_icon_from_file(conf.default_logo_path)
        self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.set_modal(True)
        
        self.set_border_width(5)
        self.connect("destroy-event", self.close)
        
        VBox=gtk.VBox(spacing=5)
        buttons=gtk.HButtonBox()
        
        okbutton=gtk.Button(gtk.STOCK_OK)
        okbutton.set_use_stock(True)
        okbutton.connect("clicked", self.ok)
        
        cancelbutton=gtk.Button(gtk.STOCK_CANCEL)
        cancelbutton.set_use_stock(True)
        cancelbutton.connect("clicked", self.close)
        
        buttons.add(okbutton)
        buttons.add(cancelbutton)
        
        self.show_open_as_root=gtk.CheckButton(_("Show 'open as root' option."))
        self.show_open_a_terminal_here=gtk.CheckButton(_("Show 'open a terminal here' option."))
        (show_root, show_term)=read_config()
        
        self.show_open_as_root.set_active(show_root)
        self.show_open_a_terminal_here.set_active(show_term)
        
        
        VBox.pack_start(self.show_open_as_root, False)
        VBox.pack_start(self.show_open_a_terminal_here, False)
        VBox.pack_end(buttons, False)
        
        
        self.add(VBox)
        self.show_all()
        gtk.main()
    
    def ok(self, obj=None):
        try:
            file=open(conf.config_dir+"BrowsingPlugins.conf", "w")
            if self.show_open_as_root.get_active():
                file.write("show_open_as_root=True\n")
            else: file.write("show_open_as_root=False\n")
            if self.show_open_a_terminal_here.get_active():
                file.write("show_open_a_terminal_here=True\n")
            else: file.write("show_open_a_terminal_here=False\n")
            
        except: print ("Error writing browsing config: " + str(sys.exc_info()) )
        self.close()
        
    def close(self, obj=None, event=None):
        self.hide()
        gtk.main_quit()


def read_config():
    show_open_as_root=False
    show_open_a_terminal_here=False
    try:
        file=open(conf.config_dir+"BrowsingPlugins.conf", "r")
        for line in file.readlines():
            line=line.replace("\n", "")
            line=line.split("=")
            if len(line)>=2:
                if line[0]=="show_open_as_root":
                    if line[1]=="True":
                        show_open_as_root=True
                elif line[0]=="show_open_a_terminal_here":
                    if line[1]=="True":
                        show_open_a_terminal_here=True
    except:
        print ("Error reading browsing config: " + str(sys.exc_info()) )
    return (show_open_as_root, show_open_a_terminal_here)