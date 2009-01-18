import gtk, cairo
import AGM_utils as utils
from AGM.AGM_default_config import conf as config

conf=config()

class Entry(gtk.Entry):
    __gsignals__ = {
             'expose-event':   'override'}
    def __init__(self, get_gradient):
        gtk.Entry.__init__(self)
        self.get_gradient=get_gradient
        for (state, color) in [(gtk.STATE_NORMAL,conf.fgcolor), (gtk.STATE_ACTIVE,conf.activefgcolor), (gtk.STATE_PRELIGHT,conf.selectedfgcolor)]:
             self.modify_text(state, gtk.gdk.color_parse(color))
        for (state, color) in [(gtk.STATE_NORMAL,conf.bgcolor), (gtk.STATE_ACTIVE,conf.activebgcolor), (gtk.STATE_PRELIGHT,conf.selectedbgcolor)]:
             self.modify_bg(state, gtk.gdk.color_parse(color))
             self.modify_base(state, gtk.gdk.color_parse(color))
        #self.connect("expose_event", self.do_expose_event)

    def do_expose_event(self, event=None):
         gtk.Entry.do_expose_event(self, event)
         self.cr = self.window.cairo_create()
         self.draw_button()
         return False
       
    def draw_button(self):
        cr=self.cr
        if cr!=None:
            
            rect = self.get_allocation()
            
            r=5
            x0=0
            x1=x0+rect.width
            y0=0
            y1=y0+rect.height
            
            cr.rectangle(x0, y0, x1, y1)
            cr.set_source(self.get_gradient(-rect.x, -rect.y))
            cr.fill()
            col=utils.hex2float(conf.fgcolor)
            cr.set_source_rgb(col[0], col[1], col[2])
            cr.stroke()