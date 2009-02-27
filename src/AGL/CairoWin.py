#    Author name:    Marco Mosconi
#    Author email:   brus46@gmail.com
#    Author website: http://www.sciallo.net

#    This file is part of AGM.

#    AGM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
import cairo
from AGM.AGM_default_config import conf as config

conf=config()

if gtk.pygtk_version < (2, 10, 0):
     print 'This programs needs PyGtk >= 2.10'
     raise SystemExit

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
 

class TransparentWindow(gtk.Window):
     __gsignals__ = {
             'expose-event':   'override',
             'screen-changed': 'override',
     }

     def __init__(self):
		 gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		 self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
		 self.set_skip_taskbar_hint(True)
		 self.set_skip_pager_hint(True)
		 self.set_title("")
		 self.set_keep_above(False)
		 self.stick()
		 #self.change=change_func

		 self.set_app_paintable(True)

		 self.set_decorated(False)

		 self.add_events(gtk.gdk.FOCUS_CHANGE_MASK)

		 self.do_screen_changed()

     def on_button_press(self, widget, event):
             self.begin_move_drag(
                 event.button,
                 int(event.x_root),
                 int(event.y_root),
                 event.time)

     def render_safe_rect(self, cr, x, y, w, h):
         x0 = x
         y0 = y
         x1 = x + w
         y1 = y + h
         
         cr.move_to(x0,y0)
         cr.line_to(x1,y0)
         cr.line_to(x1,y1)
         cr.line_to(x0,y1)
         cr.close_path()
         
     def render_rect(self, cr, x, y, w, h, o):
         # Crea un rettangolo con i bordi arrotondati
         
         x0 = x
         y0 = y
         rect_width = w
         rect_height = h
         radius = 10 + o
         
         x1 = x + rect_width
         y1 = y + rect_height         
         
         #ydw=y1+height
         
         cr.move_to(x0, y0 + radius)
         cr.curve_to(x0, y0 + radius, x0, y0, x0 + radius, y0)                
         
         cr.line_to(x1 - radius, y0)
         cr.curve_to(x1 -radius , y0, x1, y0, x1, y0 + radius)

         cr.line_to(x1 , y1-radius)
         cr.curve_to(x1, y1-radius, x1, y1, x1 - radius, y1)
         cr.line_to(x0+radius, y1)
         cr.curve_to(x0+radius, y1, x0, y1, x0, y1-radius)
         
         cr.close_path()
             

     def do_expose_event(self, event=None):
         
         cr = self.window.cairo_create()
         self.do_screen_changed()
         if self.supports_alpha:
                 cr.set_source_rgba(1.0, 1.0, 1.0, 0.0)
         else:
                 cr.set_source_rgb(1.0, 1.0, 1.0)

         cr.set_operator(cairo.OPERATOR_SOURCE)
         cr.paint()
         #(diff, applet_diff)=conf.read_conf()
         #if diff or applet_diff:
         #    self.change(force=True)
         
         if self.supports_alpha and conf.safe_mode==False:
              self.draw_window(cr)
         else:
             self.draw_safe_window(cr)
         
         if event!=None:
             # chiediamo esplicitamente ai figli di disegnarsi
             # Se non lo facessimo non sarebbero visualizzati
             # i widgets aggiunti alla TransparentWindow
             children = self.get_children()
             for c in children:
                     self.propagate_expose(c, event)
    
     def draw_window(self, cr):     
         (width, height) = self.get_size()
         x=0
         y=0
         
         cr.move_to(0, 0)
         cr.set_line_width(1.0)

         cr.set_operator(cairo.OPERATOR_OVER)

         pat=self.get_gradient()
         self.render_rect(cr, x, y, width, height, 10)
         cr.set_source(pat)
         cr.fill()

     def get_point(self, position, h, w, x, y):
          if position==conf.gradient_direction.N:
              return w/2, y
          if position==conf.gradient_direction.NW:
              return x, y
          if position==conf.gradient_direction.NE:
              return w, y
          
          if position==conf.gradient_direction.W:
              return x, (h+y)/2
          if position==conf.gradient_direction.E:
              return w, (h+y)/2
          
          if position==conf.gradient_direction.S:
              return w/2, h + y
          if position==conf.gradient_direction.SW:
              return x, h + y
          if position==conf.gradient_direction.SE:
              return w, h + y
          
          return 0, 0

     def draw_safe_window(self, cr):
         (width, height) = self.get_size()
         x=0
         y=0
         cr.move_to(0, 0)
         cr.set_line_width(1.0)

         cr.set_operator(cairo.OPERATOR_OVER)

         pat=self.get_gradient()
         self.render_safe_rect(cr, x, y, width, height)
         cr.set_source(pat)
         cr.fill()
     
     def get_gradient(self, x=0, y=0):
         (width, height) = self.get_size()
         gradient_coord=[]
         
         startx, starty=self.get_point(conf.gradient_direction.get_start_point(), height, width, x, y)
         endx, endy=self.get_point(conf.gradient_direction.get_end_point(), height, width, x, y)

         pat = cairo.LinearGradient(startx, starty, endx, endy)
         #Color1
         col = hex2float(conf.gradient_color1)
         pat.add_color_stop_rgba(0.0, col[0], col[1], col[2], col[3])

         #Color3 if enabled
         if (conf.gradient_enable_3color):
             col = hex2float(conf.gradient_color3)
             pat.add_color_stop_rgba(0.5, col[0], col[1], col[2], col[3])

         #Color2
         col = hex2float(conf.gradient_color2)
         pat.add_color_stop_rgba(1.0, col[0], col[1], col[2], col[3])
         return pat
     
     def do_screen_changed(self, old_screen=None):
             screen = self.get_screen()
             colormap = screen.get_rgba_colormap()
             self.supports_alpha = True
             if self.is_composited():
                     #print 'Composite manager active!'
                     colormap = screen.get_rgba_colormap()
                     self.supports_alpha = True
             elif self.is_composited()==False:
                     #print "Composite manager isn't active? Will work without cools windows :("
                     colormap = screen.get_rgb_colormap()
                     self.supports_alpha = False
             self.set_colormap(colormap)
