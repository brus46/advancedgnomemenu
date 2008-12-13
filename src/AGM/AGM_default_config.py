#    Author name:    Marco Mosconi
#    Author email:   brus46@gmail.com
#    Author website: http://www.sciallo.net

#    This file is part of AGM.

#    AGM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, gtk

class conf:
    def __init__(self):
        self.install_picture_dir="./"
        self.install_dir="./"
        self.install_data_dir="./"
        self.plugin_folder="./AGMplugins/"

        FILEPATH = os.path.abspath(__file__)
        pwd, dirname = os.path.split(os.path.dirname(FILEPATH))
        dirname=pwd.split("/")
        dirname.reverse()
        dirname=dirname[0]
        if dirname != "src":
            #print 'Running installed agm, modifying paths.'
            self.install_dir="/usr/bin/"
            self.install_picture_dir="/usr/share/pixmaps/"
            self.install_data_dir="/usr/share/AGM/"
            self.plugin_folder="/usr/local/lib/python/AGMplugins/"
            

        self.theme_path=os.path.expanduser("~")+"/.AGM/themes/"
        
        self.home_logo_path=os.path.expanduser("~")+"/.face"
        if (os.path.exists(self.home_logo_path)==False):
            self.home_logo_path=self.install_picture_dir+"AGM.png"
        self.default_logo_path=self.install_picture_dir+"AGM.png"
        self.config_path=os.path.expanduser("~")+"/.AGM_config"
        self.show_path=os.path.expanduser("~")+"/.AGM_show"
        self.favorites_path=os.path.expanduser("~")+"/.AGM_fav_app"
        self.args=""
        
        
        self.open_folder_command="nautilus %U"
        self.open_file_command="gnome-open %U"
        
        self.opacity=1
        self.welcome="Welcome to Advanced Gnome Menu"
        self.safe_mode=False
        
        #Theme
        self.theme=None
        
        #COLOR_Buttons
        self.bgcolor="#525252"
        self.selectedbgcolor="#373737"
        self.activebgcolor="#969696"
        self.fgcolor="#FFFFFF"
        self.selectedfgcolor="#FFFFFF"
        self.activefgcolor="#FFFFFF"
        self.use_system_color=False
        #COLOR_WINDOW
        self.gradient_color1="#6e6e6eF3"
        self.gradient_color2="#48484884"
        self.gradient_color3="#ffffff"
        self.gradient_enable_3color=False
        
        self.lightingcolor="#fffcfcae"
        self.show_lighting=True
        
        self.iconbordercolor="#fffcfcae"
        self.iconbgcolor="#505050ff"
        
        self.gradient_direction=gradient_direction()
        
        self.startposition=positions()
        self.popupstyle=popup_style()
        self.top_position=top_position()
        
        #Applet
        self.applet_icon=self.home_logo_path
        self.applet_text="Menu"
        self.applet_fg_color="#000000"
        
        #behavior
        self.hide_on_program_launch=False
        
        #Search_box
        self.search_box_top_position=True
        self.search_box_show=True
        
        #Window
        self.window_width=500
        self.window_height=430
        
        #FAV APPS
        self.fav_apps=[
                       {"name":"Firefox", "icon":"firefox", "command":"exec#firefox"},
                       {"name":"Pidgin", "icon":"pidgin", "command":"exec#pidgin"},
                       {"name":"Terminal", "icon":"gnome-terminal", "command":"exec#gnome-terminal"}                       
                       ]
        self.fav_apps_orientation="H" #"V" Horizontal, Vertical
        self.fav_apps_icon_dimension=24
        self.fav_apps_show_text=False
        self.fav_apps_text_bold=False
        self.fav_apps_show=True
        
        #Default menu
        self.menu_order=["GnomeMenu",
            "MorePlaces",
            "LastUsedFiles", 
            "Search",
            "LogOut"]
        self.menu_icon_size=48
        
        self.read_conf()
        pass
    def read_conf(self, config_path=None):
        print_mode=False
        if config_path==None: 
            config_path=self.config_path
        else: print_mode=True
        difference=False
        file=None
        try:
            file=open(config_path, "r")
        except:
            print "Cannot read config: " + config_path + " Using default-one"
        if file==None:
            try:
                file=open(self.install_data_dir+"AGM_default_config", "r")
            except:
                print "Cannot read even default config. This can be a trouble."
        if file!=None:
            for line in file.readlines():
                data=line.split("=")
                if len(data)>=2:
                    data[1] = data[1].replace("\n", "")
                    if print_mode: print data[0] + "=" + data[1] 
                    if data[0]=="opacity":
                        if (self.opacity!=eval(data[1])): difference=True
                        self.opacity=eval(data[1])
                    elif data[0]=="welcome_text":
                        if (self.welcome!=data[1]): difference=True
                        self.welcome=data[1]
                    elif data[0]=="bgcolor":
                        if (self.bgcolor!=data[1]): difference=True
                        self.bgcolor=data[1]
                    elif data[0]=="fgcolor":
                        if (self.fgcolor!=data[1]): difference=True
                        self.fgcolor=data[1]
                    elif data[0]=="selectedbgcolor":
                        if (self.selectedbgcolor!=data[1]): difference=True
                        self.selectedbgcolor=data[1]
                    elif data[0]=="selectedfgcolor":
                        if (self.selectedfgcolor!=data[1]): difference=True
                        self.selectedfgcolor=data[1]
                    elif data[0]=="activebgcolor":
                        if (self.activebgcolor!=data[1]): difference=True
                        self.activebgcolor=data[1]
                    elif data[0]=="activefgcolor":
                        if (self.activefgcolor!=data[1]): difference=True
                        self.activefgcolor=data[1]
                    elif data[0]=="mainbgcolor" or data[0]=="gradient_color1":
                        if (self.gradient_color1!=data[1]): difference=True
                        self.gradient_color1=data[1]
                    elif data[0]=="topbgcolor"  or data[0]=="gradient_color2":
                        if (self.gradient_color2!=data[1]): difference=True
                        self.gradient_color2=data[1]
                    elif data[0]=="gradient_color3":
                        if (self.gradient_color3!=data[1]): difference=True
                        self.gradient_color3=data[1]
                    elif data[0]=="gradient_enable_3color":
                        if (self.gradient_enable_3color!=(data[1]=="True")): difference=True
                        self.gradient_enable_3color=(data[1]=="True")
                    elif data[0]=="lightingbgcolor":
                        if (self.lightingcolor!=data[1]): difference=True
                        self.lightingcolor=data[1]
                    elif data[0]=="show_lighting":
                        if (self.show_lighting!=(data[1]=="True")): difference=True
                        self.show_lighting=(data[1]=="True")
                    elif data[0]=="gradient_direction":
                        if (self.gradient_direction.read_string(data[1])): difference=True
                    elif data[0]=="iconbgcolor":
                        if (self.iconbgcolor!=data[1]): difference=True
                        self.iconbgcolor=data[1]
                    elif data[0]=="iconbordercolor":
                        if (self.iconbordercolor!=data[1]): difference=True
                        self.iconbordercolor=data[1]
                    elif data[0]=="use_system_color":
                        if (self.use_system_color!=(data[1]=="True")): difference=True
                        self.use_system_color=(data[1]=="True")
                    elif data[0]=="menu":
                        if (self.menu_order!=data[1].split("#")): difference=True
                        self.menu_order=data[1].split("#")
                    elif data[0]=="menu_icon_size":
                        if (self.menu_icon_size!=int(data[1])): difference=True
                        self.menu_icon_size=int(data[1])
                    elif data[0]=="position":
                        if self.startposition.read_string(data[1]):
                            difference=True
                    elif data[0]=="top_position":
                        if self.top_position.read_string(data[1]):
                            difference=True
                    elif data[0]=="popup_style":
                        if self.popupstyle.read_string(data[1]):
                            difference=True
                    elif data[0]=="applet_icon":
                        if (self.applet_icon!=data[1]): difference=True
                        self.applet_icon=data[1]
                    elif data[0]=="applet_text":
                        if (self.applet_text!=data[1]): difference=True
                        self.applet_text=data[1]
                    elif data[0]=="applet_fg_color":
                        if (self.applet_fg_color!=data[1]): difference=True
                        self.applet_fg_color=data[1]
                    elif data[0]=="hide_on_program_launch":
                        if (self.hide_on_program_launch!=(data[1]=="True")): difference=True                        
                        self.hide_on_program_launch=(data[1]=="True")
                    elif data[0]=="window_height":
                        if (self.window_height!=int(data[1].replace(".0", ""))): difference=True
                        self.window_height=int(data[1].replace(".0", ""))
                    elif data[0]=="window_width":
                        if (self.window_width!=int(data[1].replace(".0", ""))): difference=True
                        self.window_width=int(data[1].replace(".0", ""))
                    elif data[0]=="fav_apps_icon_dimension":
                        if (self.fav_apps_icon_dimension!=int(data[1].replace(".0", ""))): difference=True                        
                        self.fav_apps_icon_dimension=int(data[1].replace(".0", ""))                        
                    elif data[0]=="fav_apps_show_text":
                        if (self.fav_apps_show_text!=(data[1]=="True")): difference=True                        
                        self.fav_apps_show_text=(data[1]=="True")                        
                    elif data[0]=="fav_apps_text_bold":
                        if (self.fav_apps_text_bold!=(data[1]=="True")): difference=True                        
                        self.fav_apps_text_bold=(data[1]=="True") 
                    elif data[0]=="fav_apps_show":
                        if (self.fav_apps_show!=(data[1]=="True")): difference=True                        
                        self.fav_apps_show=(data[1]=="True") 
                    elif data[0]=="fav_apps_orientation":
                        if (self.fav_apps_orientation!=data[1]): difference=True                        
                        self.fav_apps_orientation=data[1]
                    elif data[0]=="theme":
                        if os.path.isdir(data[1]):
                            self.theme=data[1]
                    elif data[0]=="open_folder_command":
                        self.open_folder_command=data[1]
                    elif data[0]=="open_file_command":
                        self.open_file_command=data[1]
                    elif data[0]=="search_box_show":
                        if (self.search_box_show!=(data[1]=="True")): difference=True                        
                        self.search_box_show=(data[1]=="True") 
                    elif data[0]=="search_box_top_position":
                        if (self.search_box_top_position!=(data[1]=="True")): difference=True                        
                        self.search_box_top_position=(data[1]=="True") 
                    else:
                        print "Unknow config ", data[0]
        fav_changes=self.read_fav_apps()
        return (difference or fav_changes)
    
    def read_fav_apps(self):
        differences=False
        newFavApps=[]
        file=None
        try:
            file=open(self.favorites_path, "r")
        except: print "Cannot read fav apps. Using defaults."
        if file==None:
            try:
                file=open(conf.install_data_dir+"AGM_default_fav_app", "r")
            except: print "Cannot read even default fav apps."        
        
        if file!=None:
            for line in file.readlines():
                data=line.split(";")
                if len(data)>=3:
                    newFavApps.append({"name":data[0], "icon":data[1], "command":data[2]})
            
            if len(newFavApps)==len(self.fav_apps):
                equals=True
                index=0
                for fav in self.fav_apps:
                    newFav=newFavApps[index]
                    if (fav["name"]!=newFav["name"]) or (fav["icon"]!=newFav["icon"]) or (fav["command"]!=newFav["command"]):
                        equals=False
                        break
                    index+=1
                if not equals:
                    differences=True
            else:
                differences=True
            self.fav_apps=newFavApps

        return differences
    
class positions:
    def __init__(self):
        self.CENTER=0
        self.UP_LEFT=1
        self.UP_CENTER=2
        self.UP_RIGHT=3
        self.DW_LEFT=4
        self.DW_CENTER=5
        self.DW_RIGHT=6    
        self.MANUAL=7
        
        self.x=0
        self.y=0
        self.pos=self.CENTER
        
    def read_string(self, str):
        if str!=None:
            pos=0
            x=0
            y=0
            str=str.split("_")
            if str[0]=="CENTER":
                pos=self.CENTER
            elif str[0]=="UP LEFT":
                pos=self.UP_LEFT
            elif str[0]=="UP CENTER":
                pos=self.UP_CENTER
            elif str[0]=="UP RIGHT":
                pos=self.UP_RIGHT
            elif str[0]=="DOWN LEFT":
                pos=self.DW_LEFT
            elif str[0]=="DOWN RIGHT":
                pos=self.DW_RIGHT
            elif str[0]=="DOWN CENTER":
                pos=self.DW_CENTER
            elif str[0]=="MANUAL":
                pos=self.MANUAL
                
            if len(str)>=3:
                x=int(str[1].replace(".0", ""))
                y=int(str[2].replace(".0", ""))
                
            if pos!=self.pos:
                self.x=x
                self.y=y
                self.pos=pos
                return True
            if (self.x!=x or self.y!=y):
                self.x=x
                self.y=y
                return True
            return False
    
    def get_position(self):
        return (self.pos, self.x, self.y)
    def get_pos_name(self):
        return self.get_list()[self.pos]
        
    def set_position(self, pos, x, y):
        self.pos=pos
        self.x=x
        self.y=y
    
    def get_list(self):
        return ["CENTER", "UP LEFT", "UP CENTER", "UP RIGHT", "DOWN LEFT", "DOWN CENTER", "DOWN RIGHT", "MANUAL"]
        pass
    
    def move_window(self, win):
        (width, height)=win.get_size()
        win.set_position(gtk.WIN_POS_NONE)
        if self.pos==self.CENTER:
            win.set_position(gtk.WIN_POS_CENTER_ALWAYS)
            
        elif self.pos==self.UP_LEFT:
            win.set_gravity(gtk.gdk.GRAVITY_NORTH_WEST)
            win.move(0, 0)
        elif self.pos==self.UP_CENTER:
            win.set_gravity(gtk.gdk.GRAVITY_NORTH_WEST)
            win.move((gtk.gdk.screen_width() - width)/2, 0)
        elif self.pos==self.UP_RIGHT:
            win.set_gravity(gtk.gdk.GRAVITY_NORTH_EAST)
            win.move(gtk.gdk.screen_width(), 0)
            
        elif self.pos==self.DW_LEFT:
            win.set_gravity(gtk.gdk.GRAVITY_SOUTH_WEST)
            win.move(0, gtk.gdk.screen_height())
        elif self.pos==self.DW_CENTER:
            win.set_gravity(gtk.gdk.GRAVITY_SOUTH_WEST)
            win.move((gtk.gdk.screen_width() - width)/2, gtk.gdk.screen_height())
        elif self.pos==self.DW_RIGHT:
            win.set_gravity(gtk.gdk.GRAVITY_SOUTH_EAST)
            win.move(gtk.gdk.screen_width(), gtk.gdk.screen_height())
        elif self.pos==self.MANUAL:
            win.set_gravity(gtk.gdk.GRAVITY_NORTH_WEST)
            x=self.x
            y=self.y
            if x<0: x=gtk.gdk.screen_width()-width
            if y<0: y=gtk.gdk.screen_height()-height
            win.move(x, y)
        
    
    def to_string(self):
        return self.get_list()[self.pos] + "_" + str(self.x) + "_" + str(self.y)

class popup_style:
    def __init__(self):
        self.NONE=0
        self.LEFT=1
        self.CENTER=2
        self.RIGHT=3
        
        self.style=self.NONE
        self.width=48
        self.height=32
        pass
    
    def get_list(self):
        return ["NONE", "LEFT", "CENTER", "RIGHT"]
    def read_string(self, str):
        pos=self.NONE
        width=48
        height=32
        
        str=str.split("_")
        if str[0]=="NONE":
            pos=0
        elif str[0]=="LEFT":
            pos=1
        elif str[0]=="CENTER":
            pos=2
        elif str[0]=="RIGHT":
            pos=3
        if len(str)>=2:
            width=int(str[1].replace(".0", ""))
        if len(str)>=3:
            height=int(str[2].replace(".0", ""))            
        if pos!=self.style or width!=self.width or height!=self.height:
            self.height=height
            self.width=width
            self.style=pos
            return True
        return False
    
    def get_str(self):
        return self.get_list()[self.style]
    
    def get_style(self):
        return self.style, self.width, self.height

class top_position:
    def __init__(self):
        self.TOP_LEFT=0
        self.TOP_RIGHT=1
        self.DW_LEFT=2
        self.DW_RIGHT=3
        
        self.top=0
        pass
    def get_list(self):
        return ["NORTH WEST", "NORTH EAST", "SOUTH WEST", "SOUTH EAST"]
    def read_string(self, str):
        pos=0
        if str=="NORTH WEST":
            pos=0
        elif str=="NORTH EAST":
            pos=1
        elif str=="SOUTH WEST":
            pos=2
        elif str=="SOUTH EAST":
            pos=3
        if pos!=self.top:
            self.top=pos
            return True
        return False
    
    def get_str(self):
        return self.get_list()[self.top]
    
    def get_top(self):
        return self.top

class gradient_direction:
    def __init__(self):
        self.NE=0
        self.N=1
        self.NW=2
        self.W=3
        self.SW=4
        self.S=5
        self.SE=6
        self.E=7
        
        
        self.gradient=[self.N,self.S]
        pass
    
    def read_string(self, string):
        dir=string.split(";")
        if len(dir)>=2:
            start=self.N
            end=self.S
            list=self.get_list()
            for el in list:
                if list[el]==dir[0]:
                    start=el
                if list[el]==dir[1]:
                    end=el
            if self.gradient[0]!=start or self.gradient[1]!=end:
                self.gradient=[start, end]
                return True
            else: return False
        else:
            if self.gradient[0]!=self.N or self.gradient[1]!=self.S:
                self.gradient=[self.N, self.S]
                return True
            else: return False
    
    def get_list(self):
        return {self.N:"N",
                self.NE:"NE",
                self.NW:"NW",
                self.W:"W",
                self.E:"E",
                self.S:"S",
                self.SE:"SE",
                self.SW:"SW" }
    
    def to_string(self):
        return ""+ self.get_list()[self.gradient[0]] + ";"+ self.get_list()[self.gradient[1]]+";"
    
    def get_start_point(self):
        return self.gradient[0]
    
    def get_end_point(self):
        return self.gradient[1]