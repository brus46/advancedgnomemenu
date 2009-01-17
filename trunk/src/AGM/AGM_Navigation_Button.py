import gtk
import cairo
from AGM.AGM_default_config import conf as config

conf=config()
def hex2float(hex_code):
    hex_code=hex_code.replace("#", "")
    c=["", "", "", ""]
    i=0
    for h in hex_code:
       if (i<=1):
           c[0]+=h
       elif (i<=3):
           c[1]+=h
       elif (i<=5):
           c[2]+=h
       elif (i<=7):
           c[3]+=h
       i+=1 
    ret=[]
    for h in c:
        if h=="": h="00"
        hex=int(h,16)
        
        ic = int(hex)
        ret.append( ic / 255.0 )
    return ret

class NavButton(gtk.DrawingArea):
    def __init__(self):
        super(NavButton, self).__init__()

        #self.set_app_paintable(True)
        self.set_colormap(self.get_screen().get_rgba_colormap())
        #self.modify_bg()
        self.connect("expose_event", self.do_expose_event)
        
        #self.do_expose_event()
    
    def set_image(self, Image):
        
        pass
    
    def set_label(self, label):
        pass
    
    def do_expose_event(self, widget, event):
         print "Redraw"
         cr = widget.window.cairo_create()
         #print event.area
         #cr.rectangle(event.area.x, event.area.y,
         #           event.area.width, event.area.height)
         #cr.clip()

         
         #cr.set_source_rgb(1.0, 1.0, 1.0)

         #cr.set_operator(cairo.OPERATOR_SOURCE)
         #cr.paint()
         #if conf.read_conf():
         #    self.change()
         
         self.draw_button(cr)
         return False
       
    def draw_button(self, cr):
        
        #cr.move_to(0, 0)
        cr.set_line_width(1.0)
        #cr.set_operator(cairo.OPERATOR_OVER)
        col = hex2float(conf.bgcolor)
        print col
        cr.set_source_rgba(col[0], col[1], col[2], col[3])
        
        rect = self.get_allocation()
        
        r=5
        x0=0
        x1=x0+rect.width
        y0=0
        y1=y0+rect.height
        
        cr.move_to(x0, y0+r)
        cr.curve_to(x0, y0+r, x0, y0, x0+r, y0)
        cr.line_to(x1-r, y0)
        cr.curve_to(x1-r, y0, x1, y0, x1, y0+r)
        cr.line_to(x1, y1)
        cr.line_to(x0, y1)        
        cr.close_path()
        
        cr.fill()
        
#        col = hex2float(conf.fgcolor)
#        cr.set_source_rgb(col[0], col[1], col[2])
#        cr.stroke()