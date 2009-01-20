from AGM.AGM_Fav_app_model import model
from AGM.AGM_Fav_app import FavApp
import gtk
import AGM.AGM_utils as utils

class Model(model):
    def __init__(self):
        model.__init__(self)
        self.model_code_name="Logout"
        self.model_icon="logout"
        self.model_name="Logout"
        self.model_description="Logout from gnome session"
        self.to_execute=""
    
    def get_fav_app(self):
        return FavApp("Logout", "logout", "Logout from gnome session", ["gnome-session-save", "-kill"])
