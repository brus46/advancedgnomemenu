from AGM.AGM_Fav_app_model import model
from AGM.AGM_Fav_app import FavApp
import gtk, os
import AGM.localization
_=AGM.localization.Translate

class Model(model):
    def __init__(self):
        model.__init__(self)
        self.model_code_name="Computer"
        self.model_icon="computer"
        self.model_name=_("Computer")
        self.model_description=_("Select a program from all sources visible to this computer")
    
    def get_fav_app(self):
        return FavApp(_("Computer"), "computer", _(self.model_description), "nautilus computer:///")
