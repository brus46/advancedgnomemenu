import gtk, os

from AGM_default_config import conf as config
conf=config()

def hex2float(hex_code):
    hex_code=hex_code.replace("#", "")
    c=["", "", "", ""]
    i=0
    if len(hex_code)==12:
        hex_code=hex_code[0]+hex_code[1]+hex_code[4]+hex_code[5]+hex_code[8]+hex_code[9]
    for h in hex_code:
       if (i<=1):
           c[0]+=h
       elif (i<=3):
           c[1]+=h
       elif (i<=5):
           c[2]+=h
       elif (i<=7):
           c[3]+=h
       i+=1 
    ret=[]
    for h in c:
        if h=="": h="00"
        hex=int(h,16)
        
        ic = int(hex)
        ret.append( ic / 255.0 )
    return ret

def searchPictureFromName(iconName):
    icon_theme = gtk.icon_theme_get_default()
    pixbuf = None
    try:
        pixbuf = icon_theme.load_icon(iconName, 32, 0)
    except: pass
    if pixbuf==None:
        if os.path.isfile(iconName):
            return True
        else:
            return False
    else: return True
                
def getPixbufFromName(iconName, size=conf.menu_icon_size, type="folder"):
    #print iconName, size, type
    if isinstance(iconName ,gtk.gdk.Pixbuf)==False:
        icon_theme = gtk.icon_theme_get_default()
        pixbuf = None
        try:
            pixbuf = icon_theme.load_icon(iconName, size, 0)
            path = icon_theme.lookup_icon(iconName, size, 0).get_filename()
        except:
            if iconName and '/' in iconName:
                try:
                    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(iconName, size, size)
                    path = iconName
                except:
                    pass
            if pixbuf == None:
                if type=="folder":
                    iconName = 'gnome-fs-directory'
                elif type=="application" or type=="app":
                    iconName = 'application-default-icon'
                elif type=="theme":
                    from AGM_default_config import conf as config
                    conf=config()
                    iconName= conf.install_data_dir + 'pictures/AGMtheme.png'
                else:
                    iconName = 'text-x-generic'
                try:
                    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(iconName, size, size)
                    path = iconName
                except:
                    try:
                        pixbuf = icon_theme.load_icon(iconName, size, 0)
                        path = icon_theme.lookup_icon(iconName, size, 0).get_filename()
                    except:
                        pixbuf==None
                        pass
    else:
        pixbuf=iconName
    if pixbuf == None:
        print "cannot find icon:" + iconName
        return None
    if pixbuf.get_width() != size or pixbuf.get_height() != size:
        width=pixbuf.get_width()
        height=pixbuf.get_height()
        if width==height:
            width=size
            height=size
        else:    
            if width > size:
                height=height*size/width
                width=size
                if height > size:
                    width=width*size/height
                    height=size
        pixbuf = pixbuf.scale_simple(width, height, gtk.gdk.INTERP_HYPER)
    return pixbuf

def scale_pixbuf(pixbuf, size):
    width=pixbuf.get_width()
    height=pixbuf.get_height()
    if width==height:
        width=size
        height=size
    else:    
        if width > size:
            height=height*size/width
            width=size
            if height > size:
                width=width*size/height
                height=size
    pixbuf = pixbuf.scale_simple(width, height, gtk.gdk.INTERP_HYPER)
    return pixbuf

class OpenFile:
    def __init__(self):
        self.filename=self.browse()
        pass
    def browse(self):
        file_open = gtk.FileChooserDialog(title="Select Theme"
                    , action=gtk.FILE_CHOOSER_ACTION_OPEN
                    , buttons=(gtk.STOCK_CANCEL
                                , gtk.RESPONSE_CANCEL
                                , gtk.STOCK_OPEN
                                , gtk.RESPONSE_OK))   
        file_open.set_current_folder(os.path.expanduser("~")+"/")   
        filter = gtk.FileFilter()
        filter.set_name("AGM Themes")
        filter.add_mime_type("application/x-tar")
        filter.add_pattern("*.tar")
        filter.add_pattern("*.agmtheme")
        file_open.add_filter(filter)
        
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        file_open.add_filter(filter)
        
        """Init the return value"""
        result = None
        if file_open.run() == gtk.RESPONSE_OK:
            result = file_open.get_filename()
        file_open.destroy()
        
        return result
        
    def get_file(self):
        if self.filename!=None and os.path.isfile(self.filename):
            return self.filename
        return None

class OpenImage:
    def __init__(self):
        self.filename=self.browse()
        pass
    def browse(self):
        file_open = gtk.FileChooserDialog(title="Select Image"
                    , action=gtk.FILE_CHOOSER_ACTION_OPEN
                    , buttons=(gtk.STOCK_CANCEL
                                , gtk.RESPONSE_CANCEL
                                , gtk.STOCK_OPEN
                                , gtk.RESPONSE_OK))
        file_open.set_current_folder("/usr/share/pixmaps/") 
        filter = gtk.FileFilter()
        filter.set_name("Images")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        filter.add_mime_type("image/svg+xml")
        filter.add_mime_type("image/x-ico")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.jpeg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.svg")
        filter.add_pattern("*.ico")
        file_open.add_filter(filter)
        
        """Init the return value"""
        result = None
        if file_open.run() == gtk.RESPONSE_OK:
            result = file_open.get_filename()
        file_open.destroy()
        
        return result
        
    def get_file(self):
        if self.filename!=None and os.path.isfile(self.filename):
            return self.filename
        return None

class OpenPlugin:
    def __init__(self):
        self.filename=self.browse()
        pass
    def browse(self):
        file_open = gtk.FileChooserDialog(title="Select plugin"
                    , action=gtk.FILE_CHOOSER_ACTION_OPEN
                    , buttons=(gtk.STOCK_CANCEL
                                , gtk.RESPONSE_CANCEL
                                , gtk.STOCK_OPEN
                                , gtk.RESPONSE_OK))   
        file_open.set_current_folder(os.path.expanduser("~")+"/")   
        filter = gtk.FileFilter()
        filter.set_name("AGM Plugins")
        filter.add_mime_type("application/x-tar")
        filter.add_pattern("*.tar")
        filter.add_pattern("*.agmplugin")
        file_open.add_filter(filter)
        
        """Init the return value"""
        result = None
        if file_open.run() == gtk.RESPONSE_OK:
            result = file_open.get_filename()
        file_open.destroy()
        
        return result
        
    def get_file(self):
        if self.filename!=None and os.path.isfile(self.filename):
            return self.filename
        return None

class SaveFile:
    def __init__(self):
        self.filename=self.save()
    def save(self):
        file_open = gtk.FileChooserDialog(title="Save Theme"
                    , action=gtk.FILE_CHOOSER_ACTION_SAVE
                    , buttons=(gtk.STOCK_CANCEL
                                , gtk.RESPONSE_CANCEL
                                , gtk.STOCK_SAVE
                                , gtk.RESPONSE_OK))
        file_open.set_current_folder(os.path.expanduser("~")+"/")   
        filter = gtk.FileFilter()
        filter.set_name("AGM Themes")
        filter.add_mime_type("application/x-tar")
        filter.add_pattern("*.tar")
        file_open.add_filter(filter)
        
        """Init the return value"""
        result = None
        if file_open.run() == gtk.RESPONSE_OK:
            result = file_open.get_filename()
        file_open.destroy()
        
        return result
        
    def get_file(self):
        if self.filename!=None:
            return self.filename
        return None
    
class GetFolder:
    def __init__(self):
        self.filename=self.save()
    def save(self):
        file_open = gtk.FileChooserDialog(title="Choose exporting folder"
                    , action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER
                    , buttons=(gtk.STOCK_CANCEL
                                , gtk.RESPONSE_CANCEL
                                , gtk.STOCK_OPEN
                                , gtk.RESPONSE_OK))
        file_open.set_current_folder(os.path.expanduser("~")+"/")           
        """Init the return value"""
        result = None
        if file_open.run() == gtk.RESPONSE_OK:
            result = file_open.get_filename()
        file_open.destroy()
        
        return result
        
    def get_folder(self):
        if self.filename!=None:
            return self.filename
        return None
    
def ExecCommand(command):
        tr=newThread(command)
        tr.start()
            
from threading import Thread
class newThread(Thread):
    def __init__(self, command):
        Thread.__init__(self)
        print command
        self.command=command
        if len(command)>0:
            for par in self.command:
                    if par=="":
                        self.command.pop(par)
    
    def run(self):
        os.chdir(os.path.expanduser("~"))
        if os.path.isfile(self.command[0]):
            os.spawnv(False, self.command[0], self.command)
        else: os.spawnvp(False, self.command[0], self.command)
        #print self.command[0], "finisched"