from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from AGM.AGM_Main_Window import AGM as agm
import AGM.AGM_utils as utils
 
class agm4k(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)
 
    def init(self):
        self.setHasConfigurationInterface(False)
        self.resize(125, 125)
        self.setAspectRatioMode(Plasma.Square)
 
    def paintInterface(self, painter, option, rect):
        painter.save()
        painter.setPen(Qt.white)
        painter.drawText(rect, Qt.AlignVCenter | Qt.AlignHCenter, "Menu")
        painter.restore()
 
def CreateApplet(parent):
    return agm4k(parent)
