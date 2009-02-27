from AGM.AGM_Fav_app_model import model
from AGM.AGM_Fav_app import FavApp
import gtk, os
import AGM.localization
_=AGM.localization.Translate

class Model(model):
    def __init__(self):
        model.__init__(self)
        self.model_code_name="Home"
        self.model_icon="user-home"
        self.model_name=_("Home")
        self.model_description=_("Open your home directory")
    
    def get_fav_app(self):
        return FavApp(_("Home"), "user-home", _("Open your home directory"), "nautilus " + os.path.expanduser("~"))
