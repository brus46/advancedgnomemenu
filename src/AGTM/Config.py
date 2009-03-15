from AG_commons import GnomeMenuUtils

class config:
    def __init__(self):
        self.position="top" #"bottom"
        self.bgcolor="#000000BB"
        self.fgcolor="#FFFFFF"
        self.bgcolor_clicked="#ffffff"
        self.fgcolor_clicked="#000000"
        self.safe_mode=False
        
        self.Menu=GnomeMenuUtils.GnomeMenu()
        self.apps=self.Menu.get_apps()
        self.app_size=120
        self.app_size_mini=36
        num=0
        for app in self.apps:
            num+=1
        self.win_width=num*(self.app_size)
        self.win_width_mini=num*(self.app_size_mini)
        self.win_height=100
