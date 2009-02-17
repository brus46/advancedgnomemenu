from AGM.AGM_Fav_app_model import model
from AGM.AGM_Fav_app import FavApp
import gtk
import AGM.AGM_utils as utils
import AGM.localization
_=AGM.localization.Translate

class Model(model):
    def __init__(self):
        model.__init__(self)
        self.model_code_name="Logout"
        self.model_icon="gnome-session-halt"
        self.model_name=_("Logout")
        self.model_description=_("Add a Logout button")
    
    def get_fav_app(self):
        return FavApp(_("Logout"), "gnome-session-halt", _(self.model_description), "gnome-session-save --kill")
