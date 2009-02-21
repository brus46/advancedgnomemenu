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

import gtk, os, sys
from AGM_search_bar import search_box

if gtk.pygtk_version < (2, 10, 0):
     print 'This programs needs PyGtk >= 2.10'
     raise SystemExit

import AGM.AGM_CairoWin as CairoWin
from AGM import AGM_trayicon
from AGM.AGM_menu import Menu
from AGM.AGM_default_config import conf as config
import AGM_default_config
from AGM.AGM_info import Info
from AGM.AGM_config import Config
#from AGM.AGM_show_thread import ShowThread
import AGM.AGM_info_menu as info_menu
import AGM.AGM_utils as utils
from AGM.AGM_execute_box import ExecuteBar

from AGM_Navigation_Bar import NavBar

conf=config()

class AGM:
    ''' AGM stands for Advanced Gnome Menu '''
    def __init__(self, show_trayicon=True, show=True, top_buttons=True, applet=False, applet_unpressed=None):
        self.hidden=False
        self.applet=applet
        self.applet_unpressed=applet_unpressed
        self.show_trayicon=show_trayicon
        self.show_topbuttons=top_buttons
        
        self.X, self.Y=-1, -1
        self.top_icon=None
        self.popup=None
        
        self.obj=[]
        
        self.nameLabel = gtk.Label()
        self.EBox=gtk.EventBox()
        self.EBox.add(gtk.Image())
        self.EBox.set_size_request(80, 80)        
        
        self.infobutton=gtk.Button()
        imageinfo=gtk.Image()
        imageinfo.set_from_stock(gtk.STOCK_INFO, gtk.ICON_SIZE_SMALL_TOOLBAR)
        self.infobutton.set_image(imageinfo)
        self.infobutton.set_relief(gtk.RELIEF_NONE)
        self.infobutton.connect("clicked", self.showInfo);
        self.infomenu=info_menu.InfoMenu()
        
        self.configbutton=gtk.Button()
        imageconfig=gtk.Image()
        imageconfig.set_from_stock(gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_SMALL_TOOLBAR)
        self.configbutton.set_image(imageconfig)
        self.configbutton.set_relief(gtk.RELIEF_NONE)
        self.configbutton.connect("clicked", self.showConfig);
        
        self.exitbutton=gtk.Button()
        imageexit=gtk.Image()
        imageexit.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_SMALL_TOOLBAR)
        self.exitbutton.set_image(imageexit)
        self.exitbutton.set_relief(gtk.RELIEF_NONE)
        self.exitbutton.connect("clicked", self.exit);
        self.win=CairoWin.TransparentWindow(self.reboot)
        self.win.set_skip_taskbar_hint(True)
        self.win.set_title("AdvancedGnomeMenu") 
        self.win.connect("focus-out-event", self.hide)
        
        self.NavBar=NavBar(self.win.get_gradient)
        
        self.execution_box=""
        self.search_box=""
        self.fav_apps_buttons=[]
        self.fav_apps_bar_H=gtk.HBox()
        self.fav_apps_bar_V=gtk.VBox()
        self.eb = gtk.EventBox()
        
        gtk.gdk.threads_init()
        self.win.set_opacity(conf.opacity)
        
        self.win.resize(conf.window_width, conf.window_height)
        
        conf.startposition.move_window(self.win)
        self.layout = gtk.VBox(spacing=5)
        self.eb.add(self.layout)
        self.eb.set_visible_window(False)
        self.eb.set_border_width(12)
        self.setObjects();
        self.win.add(self.eb)
        self.win.stick()
        
        self.setcolors()
        
        if show:
            self.win.show_all()
        if self.show_trayicon: 
            self.tray=AGM_trayicon.TrayIcon(self)
            
        
        self.showPrecParentButton([[],[]])
        
        
        
        self.win.hide()
        self.hidden=True
        
        #if not self.applet:
        #    self.showThread=ShowThread(self.setOnFocus)
        if show: 
            gtk.main()
            self.exit(None)
    
    def get_win(self):
        return self.win
    
    def setcolors(self):
        if not conf.use_system_color:
            self.nameLabel.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.welcome_color))
            self.menu.get_child().modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.bgcolor))
            self.menu.get_child().modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse(conf.bgcolor))
            self.menu.get_child().modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse(conf.bgcolor))
            
            self.color(self.infobutton)
            self.color(self.configbutton)
            for button in self.fav_apps_buttons:
                self.color(button)
            self.color(self.exitbutton)
            
            self.color(self.search_box)
            self.color(self.execution_box)
            
        pass
    
    def color(self, obj):
        try:
            obj.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.bgcolor))
            obj.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse(conf.activebgcolor))
            obj.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse(conf.selectedbgcolor))
        except: pass
        try:
            obj.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor))
            obj.get_child().modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse(conf.activefgcolor))
            obj.get_child().modify_fg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse(conf.selectedfgcolor))
        except: pass
        try:
            obj.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor))
            obj.modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse(conf.activefgcolor))
            obj.modify_fg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse(conf.selectedfgcolor))
        except: pass
            
    
    def showInfo(self, obj):
        self.infomenu.show(obj)
    
    def showConfig(self, obj):
        Config(win=self)
    
    def setObjects(self):
        self.favApps() 
        MainBox=gtk.HBox()
        self.menu=Menu(self.showPrecParentButton, self.hide, self.change_icon)
        self.NavBar.set_functions(self.menu.goHome, self.menu.goTo)
        
        top_style=conf.top_position.get_top()
        
        for child in self.EBox.get_children():
            self.EBox.remove(child)
        
        self.EBox.add(gtk.Image())
        self.EBox.set_visible_window(False)
        self.set_default_logo()
                
        ToolButtons=gtk.HBox(spacing = 5)
        if (not self.show_trayicon): 
            ToolButtons.pack_end(self.exitbutton, False, False)
        ToolButtons.pack_end(self.infobutton, False, False)
        ToolButtons.pack_end(self.configbutton, False, False)
        
        self.nameLabel=gtk.Label()
        self.nameLabel.set_label('<big><b>%s</b></big>' % conf.welcome)
        self.nameLabel.set_justify(gtk.JUSTIFY_RIGHT)
        self.nameLabel.set_use_markup(True)

        TopPanel=gtk.HBox()
        TopPanelUsable=gtk.VBox()
        TopPanel.pack_end(TopPanelUsable)
        requestH=0
        requestW=32
        if (conf.fav_apps_orientation=="H"):
            TopPanelUsable.pack_start(self.fav_apps_bar_H)
            requestW=conf.fav_apps_icon_dimension + 10
            requestH=conf.fav_apps_icon_dimension + 10
        if conf.search_box_top_position and conf.search_box_show:
            requestH+=32
        if conf.execution_box_top_position and conf.execution_box_show:
            requestH+=32
        if requestH<32: requestH=32
        TopPanel.set_size_request(requestW, requestH)

        MenuBar=self.NavBar
        MenuBar.set_size_request(-1, conf.menu_bar_h)
        
        BottomPanel=gtk.VBox()
        requestH=0
        requestW=32   
        if (conf.fav_apps_orientation=="HB"):
            print "Bottom favapps"
            BottomPanel.pack_start(self.fav_apps_bar_H)
            requestW=conf.fav_apps_icon_dimension + 10
            requestH=conf.fav_apps_icon_dimension + 10
            if conf.search_box_top_position==False and conf.search_box_show:
                BottomPanel.set_size_request(conf.fav_apps_icon_dimension + 10, conf.fav_apps_icon_dimension + 10 + 48)
            else: BottomPanel.set_size_request(conf.fav_apps_icon_dimension + 10, conf.fav_apps_icon_dimension + 10)
        BottomPanel.set_size_request(requestW, requestH)
        
        popup_style, w,h=conf.popupstyle.get_style()
        space_label=gtk.Label()
        space_label.set_size_request(100, h)
        
        MenuBox=gtk.HBox(spacing=5)
        
        MainMenu=gtk.VBox()
        MainMenu.pack_start(MenuBar, False)
        MainMenu.pack_end(self.menu)
        
        FavBarV=gtk.VBox()
        top=conf.top_position.get_top()
        
        if top==conf.top_position.TOP_RIGHT or top==conf.top_position.TOP_LEFT:
            FavBarV.pack_start(gtk.Label())
            FavBarV.pack_end(self.fav_apps_bar_V)
        else:
            FavBarV.pack_start(self.fav_apps_bar_V)
        if conf.fav_apps_orientation=="V":
            MenuBox.pack_end(FavBarV, False)
        elif conf.fav_apps_orientation=="VL": MenuBox.pack_start(FavBarV, False)
        MenuBox.pack_start(MainMenu)
        
        if (top_style==conf.top_position.TOP_RIGHT):
            IconBox=gtk.VBox()
            IconBox.pack_start(self.EBox, False, False)
            IconBox.add(gtk.Label())
            
            SpacingLabel=gtk.Label()
            SpacingLabel.set_size_request(28, -1)
            MainBox.pack_end(SpacingLabel, False, False)
            
            MainBox.pack_end(IconBox, False, False)
            
            InfoBox=gtk.HBox(spacing=5)
            Labels=gtk.VBox(spacing=5)
            Labels.pack_start(self.nameLabel)
            InfoBox.pack_start(Labels)

            LeftBox=gtk.VBox()
            SpacingLabel2=gtk.Label()
            SpacingLabel2.set_size_request(40, 35)
            LeftBox.pack_start(SpacingLabel2, False, False)
            LeftBox.pack_end(InfoBox, False, False)
            if self.show_topbuttons: LeftBox.pack_start(ToolButtons, False, False)
            
            MainBox.pack_start(LeftBox, False, False)
            self.layout.pack_start(MainBox, False, False)
            self.layout.pack_start(TopPanel, False, False)
            if (popup_style!=conf.popupstyle.NONE):
                self.layout.pack_end(space_label, False, False)
            #self.layout.pack_end(BottomPanel, False, False)
            #self.layout.pack_end(MenuBox, True, True)

        elif (top_style==conf.top_position.DW_LEFT):
            IconBox=gtk.VBox()
            IconBox.pack_end(self.EBox, False, False)
            IconBox.add(gtk.Label())
            
            SpacingLabel=gtk.Label()
            SpacingLabel.set_size_request(28, -1)
            MainBox.pack_start(SpacingLabel, False, False)
            
            MainBox.pack_start(IconBox, False, False)
            
            InfoBox=gtk.HBox(spacing=5)
            Labels=gtk.VBox(spacing=5)
            Labels.pack_start(self.nameLabel)
            InfoBox.pack_start(Labels)

            RightBox=gtk.VBox()
            SpacingLabel2=gtk.Label()
            SpacingLabel2.set_size_request(40, 35)
            RightBox.pack_end(SpacingLabel2, False, False)
            
            if self.show_topbuttons: RightBox.pack_start(ToolButtons, False, False)
            RightBox.pack_start(InfoBox, False, False)
            
            MainBox.pack_end(RightBox, False, False)
            if (popup_style!=conf.popupstyle.NONE):
                self.layout.pack_start(space_label, False, False)
            self.layout.pack_start(TopPanel, False, False)
            self.layout.pack_start(MenuBox, True, True)
            #self.layout.pack_end(MainBox, False, False)
        elif (top_style==conf.top_position.DW_RIGHT):
            #print "config down right"
            IconBox=gtk.VBox()
            IconBox.pack_end(self.EBox, False, False)
            IconBox.add(gtk.Label())
            
            SpacingLabel=gtk.Label()
            SpacingLabel.set_size_request(28, -1)
            MainBox.pack_end(SpacingLabel, False, False)
            
            MainBox.pack_end(IconBox, False, False)
            
            InfoBox=gtk.HBox(spacing=5)
            Labels=gtk.VBox(spacing=5)
            Labels.pack_start(self.nameLabel)
            InfoBox.pack_start(Labels)

            LeftBox=gtk.VBox()
            SpacingLabel2=gtk.Label()
            SpacingLabel2.set_size_request(40, 35)
            LeftBox.pack_end(SpacingLabel2, False, False)
            
            if self.show_topbuttons: LeftBox.pack_start(ToolButtons, False, False)
            LeftBox.pack_start(InfoBox, False, False)
            
            MainBox.pack_start(LeftBox, False, False)
            if (popup_style!=conf.popupstyle.NONE):
                self.layout.pack_start(space_label, False, False)
            self.layout.pack_start(TopPanel, False, False)
            self.layout.pack_start(MenuBox, True, True)
            #self.layout.pack_end(MainBox, False, False)

        else: 
            IconBox=gtk.VBox()
            IconBox.pack_start(self.EBox, False, False)
            IconBox.add(gtk.Label())
            
            SpacingLabel=gtk.Label()
            SpacingLabel.set_size_request(28, -1)
            MainBox.pack_start(SpacingLabel, False, False)
            
            MainBox.pack_start(IconBox, False, False)
            
            InfoBox=gtk.HBox(spacing=5)
            Labels=gtk.VBox(spacing=5)
            Labels.pack_start(self.nameLabel)
            InfoBox.pack_start(Labels)

            RightBox=gtk.VBox()
            SpacingLabel2=gtk.Label()
            SpacingLabel2.set_size_request(40, 35)
            RightBox.pack_start(SpacingLabel2, False, False)
            RightBox.pack_end(InfoBox, False, False)
            if self.show_topbuttons: RightBox.pack_end(ToolButtons, False, False)
            
            MainBox.pack_end(RightBox, False, False)
            self.layout.pack_start(MainBox, False, False)
            self.layout.pack_start(TopPanel, False, False)

            if (popup_style!=conf.popupstyle.NONE):
                self.layout.pack_end(space_label, False, False)
            #self.layout.pack_end(MenuBox, True, True)
        
        self.layout.pack_end(BottomPanel, False, False)
        self.layout.pack_end(MenuBox, True, True)
        self.execution_box=ExecuteBar(self.win.get_gradient)
        self.search_box=search_box(self.menu.search, self.win.get_gradient)
        
        #
        if conf.execution_box_show and conf.execution_box_top_position:
            TopPanelUsable.pack_start(self.execution_box, False)
        elif conf.execution_box_show:
            BottomPanel.pack_start(self.execution_box, False)
        
        if conf.search_box_show and conf.search_box_top_position:
            TopPanelUsable.pack_start(self.search_box, False)
        elif conf.search_box_show:
            BottomPanel.pack_start(self.search_box, False)
        
        
        self.obj.append(MainBox)
        self.obj.append(TopPanel)
        self.obj.append(BottomPanel)
        self.obj.append(MenuBox)
        self.obj.append(space_label)
        
    def set_default_logo(self):
        if conf.top_icon_show_logo:
            IconLabel=(gtk.gdk.pixbuf_new_from_file(conf.default_logo_path).scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))
            if conf.top_icon_mode==conf.USE_USER_LOGO:
                if (os.path.exists(conf.home_logo_path)==True):
                    IconLabel=utils.scale_pixbuf(gtk.gdk.pixbuf_new_from_file(conf.home_logo_path), 80)
                else:
                    IconLabel=(utils.getPixbufFromName("distributor-logo", 80, "app"))
            elif conf.top_icon_mode==conf.USE_OTHER_LOGO:
                if (os.path.exists(conf.top_icon_other_logo)==True):
                    IconLabel=utils.scale_pixbuf(gtk.gdk.pixbuf_new_from_file(conf.top_icon_other_logo), 80)
            self.EBox.get_child().set_from_pixbuf(IconLabel)
        
    def change_icon(self, image, text):
        if image!=None:
            if (conf.top_icon_enable_smart_mode):
                myimage=utils.getPixbufFromName(image, 80, "folder")
                self.EBox.get_child().set_from_pixbuf(myimage)
        else:
            self.set_default_logo()
    
    def favApps(self):
        for child in self.fav_apps_bar_H.get_children():
            self.fav_apps_bar_H.remove(child)
        
        for child in self.fav_apps_bar_V.get_children():
            self.fav_apps_bar_V.remove(child)
        
        if (conf.fav_apps_orientation=="H" or conf.fav_apps_orientation=="HB") and (conf.fav_apps_show):
            fav_apps_bar=self.fav_apps_bar_H
        elif (conf.fav_apps_show):
            fav_apps_bar=self.fav_apps_bar_V
        import AGM_Fav_apps_bar
        bar=AGM_Fav_apps_bar.FavAppsBar(self.hide)
        bar.show_all()
        fav_apps_bar.pack_start(bar, False)
        self.color(bar)
           
    def showPrecParentButton(self, history):
        self.win.show_all()
        self.NavBar.update(history[0], history[1])
        
    def goback(self, obj=None, event=None):
        if event==None or event.button==1:
            self.menu.goToParent()
            self.search_box.set_text("")
        
    def gohome(self, obj=None, event=None):
        if event==None or event.button==1:
            self.menu.goHome()
            self.search_box.set_text("")
    
    def get_hidden(self):
        return self.hidden
    def set_hidden(self, hidden):
        self.hidden=hidden
    
    def setOnFocus(self):
        if self.hidden==True:
            self.show()
        else:
            self.hide()
    
    def show(self, x=-1, y=-1, popup=AGM_default_config.popup_style(), top_icon=AGM_default_config.top_position(), gravity=gtk.gdk.GRAVITY_NORTH_WEST):
        self.hidden=False
        #conf.startposition.x=x
        #conf.startposition.y=y
        #conf.startposition.pos=conf.startposition.MANUAL
        #conf.startposition.move_window(self.win, gravity)
        self.menu.goHome()
        self.search_box.set_text("")
        self.execution_box.set_text("")
        conf.read_conf()
        
        need_reboot=False
        if isinstance(popup, AGM_default_config.popup_style):
            if popup!=conf.popupstyle:
                conf.popupstyle=popup
                need_reboot=True
        if isinstance(top_icon, AGM_default_config.top_position):
            if top_icon!=conf.top_position:
                conf.top_position=top_icon
        if need_reboot:
            conf.rewrite()
            self.reboot()
    
        #print conf.top_position.get_str()
        
        self.X, self.Y=x, y
        position=AGM_default_config.positions()
        if self.X==-1 or self.Y==-1:
            position.set_position(position.CENTER, self.X, self.Y)
        else:
            position.set_position(position.MANUAL, self.X, self.Y)
        
        position.move_window(self.win, gravity)
        
        self.win.show()
        
    def hide(self, widget=None, event=None):
    	if widget!=None:
    		if event.in_==False:
    			self.win.hide()
        		self.hidden=True
                if self.applet_unpressed!=None: self.applet_unpressed()
        else:
            self.win.hide()
            self.hidden=True
            self.applet_unpressed()
    
    def exit(self, obj, kill=True):
        if obj!=None: gtk.main_quit()
        if kill: sys.exit(0)
    
    def reboot(self, force=False):
        diff, applet_diff=conf.read_conf()
        #if self.applet and (applet_diff or force ) and self.applet_refresh!=None:
        #    self.applet_refresh()

        if diff or force:
            if not force: print "Configuration changed"
            print "Reloading menu"
            
            for obj in self.obj:
                self.layout.remove(obj)
            self.obj=[]
            self.setObjects()
            self.nameLabel.set_label('<big><b>%s</b></big>' % conf.welcome)
            self.favApps()
            self.menu.reload()
            self.setcolors()
            self.win.set_opacity(conf.opacity)
            self.win.resize(conf.window_width, conf.window_height)
            conf.startposition.move_window(self.win)
        else:
            #print "No config changes"
            pass
