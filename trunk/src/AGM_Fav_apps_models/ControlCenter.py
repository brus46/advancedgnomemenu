from AGM.AGM_Fav_app_model import model
from AGM.AGM_Fav_app import FavApp
import gtk
import AGM.AGM_utils as utils
import AGM.localization
_=AGM.localization.Translate


class Model(model):
    def __init__(self):
        model.__init__(self)
        self.model_code_name="ControlCenter"
        self.model_icon="gnome-control-center"
        self.model_name=_("Control Center")
        self.model_description=_("Launch the GNOME Control Center")
    
    def get_fav_app(self):
        return FavApp(_("Control Center"), "gnome-control-center", self.model_description, "gnome-control-center")
