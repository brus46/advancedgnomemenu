import gtk
import cairo
import AGM_utils as utils
from AGM.AGM_default_config import conf as config

conf=config()

class NavButton(gtk.EventBox):
    #__gsignals__ = { "expose-event": "override" }
    def __init__(self, get_gradient, Image, Text, show_text=False):
        super(NavButton, self).__init__()
        self.set_app_paintable(True)
        self.get_gradient=get_gradient
        #self.set_colormap(self.get_screen().get_rgba_colormap())
        self.image=Image
        self.text=Text
        self.connect("expose_event", self.do_expose_event)
        self.cr=None
        self.widget=None
        self.w=conf.window_width
        self.h=conf.window_height
        
        self.bgcolor=conf.bgcolor
        
        self.label=gtk.Label(self.text)
        self.label.show_all()
        self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(conf.fgcolor))
        self.label.modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse(conf.activefgcolor))
        self.label.modify_fg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse(conf.selectedfgcolor))
        if show_text: self.add(self.label)
        self.set_tooltip_text(self.text)
    
    def set_image(self, Image):
        self.image=Image
        self.do_expose_event(None, None)
    
    def set_label(self, label):
        self.text=label
        self.set_tooltip_text(self.text)
        self.label.set_text(self.text)
    
    def do_expose_event(self, widget, event):
         if widget!=None:
             self.widget=widget
         if self.widget!=None:
             self.cr = self.widget.window.cairo_create()         
         self.draw_button()
         if event!=None:
             children = self.get_children()
             for c in children:
                     self.propagate_expose(c, event)
         return False
       
    def draw_button(self):
        cr=self.cr
        if cr!=None:
            #cr.set_operator(cairo.OPERATOR_OVER)
            #cr.set_source_rgb(0, 0, 0)
            
            rect = self.get_allocation()
            
            r=5
            x0=0
            x1=x0+rect.width
            y0=0
            y1=y0+rect.height
            
            cr.rectangle(x0, y0, x1, y1)
            cr.set_source(self.get_gradient(-rect.x, -rect.y))
            cr.fill()
            
            col = utils.hex2float(self.bgcolor)
            darkness=0.05
            cr.set_source_rgb(col[0]-darkness, col[1]-darkness, col[2]-darkness)
            self.draw_shape(cr, x0, y0, x1, y1, r)
            cr.fill()
                    
            cr.set_source_pixbuf(self.image, conf.menu_bar_icon_x, conf.menu_bar_icon_y)
            cr.paint()
    
    def draw_shape(self, cr, x0, y0, x1, y1, r, no_bottom=False):
        cr.move_to(x0, y0+r)
        cr.curve_to(x0, y0+r, x0, y0, x0+r, y0)
        cr.line_to(x1-r, y0)
        cr.curve_to(x1-r, y0, x1, y0, x1, y0+r)
        cr.line_to(x1, y1)
        if not no_bottom:
            cr.line_to(x0, y1)        
            cr.close_path()
        else:
            cr.move_to(x0, y1)
            cr.line_to(x0, y0+r)
        