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

     def __init__(self, change_func):
		 gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		 self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
		 self.set_skip_taskbar_hint(True)
		 self.set_skip_pager_hint(True)
		 self.set_title("")
		 self.set_keep_above(False)
		 self.stick()
		 self.change=change_func
		 # Indichiamo alle GTK che vogliammo disegnare noi lo sfondo.
		 self.set_app_paintable(True)

		 # non vogliamo le decorazioni del window manager
		 self.set_decorated(False)

		 # usiamo il segnale button-press-event per permettere
		 # il "click e trascina" sulla finestra. Ricordiamo
		 # che non stiamo utilizzando i classici decoratori
		 # del window manager e non gestendo qeusto segnale
		 # non sarebbe possibile spostare la finestra
		 self.add_events(gtk.gdk.FOCUS_CHANGE_MASK)
		 #self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
		 #self.connect('button-press-event', self.on_button_press)

		 # Inizializziamo lo schermo
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
         # Popup su necessita'
         popup_style, width, height = conf.popupstyle.get_style()
         top_popup=False
         if conf.top_position.get_top()==conf.top_position.DW_LEFT or conf.top_position.get_top()==conf.top_position.DW_RIGHT:
             top_popup=True
             
         icon_x, icon_y, icon_dx, icon_dy=self.get_icon_position()
         if top_popup:
             icon_x=icon_x+icon_dx-3
             icon_y=icon_y+icon_dy+10
             icon_dx=99
             icon_dy=87
         else:
             icon_x=icon_x+icon_dx-3
             icon_y=icon_y+icon_dy
             icon_dx=99
             icon_dy=87
         icon_radius=10
         
         x0 = x
         y0 = y
         rect_width = w
         rect_height = h
         radius = 10 + o
         
         x1 = x + rect_width
         y1 = y + rect_height         
         
         if top_popup:           
             if (popup_style!=conf.popupstyle.NONE):
                 y0 = y + height
             
             if (popup_style!=conf.popupstyle.LEFT):
                 cr.move_to(x0, y0 + radius)
                 cr.curve_to(x0, y0 + radius, x0, y0, x0 + radius, y0)
             else:
                 cr.move_to(x0, y)
                 cr.line_to(x0+width, y)
                 cr.curve_to(x0+width, y, x0+width, y0, x0 + width + height, y0)
                 
             if (popup_style==conf.popupstyle.CENTER):
                 xs=((x1-width)/2)
                 cr.line_to(xs-height, y0)
                 cr.curve_to(xs-height, y0, xs, y0, xs, y)
                 xs=xs + width
                 cr.line_to(xs, y)
                 cr.curve_to(xs, y, xs, y0, xs + height, y0)
             if (popup_style!=conf.popupstyle.RIGHT):
                 cr.line_to(x1 - radius, y0)
                 cr.curve_to(x1 -radius , y0, x1, y0, x1, y0 + radius)
             else:
                 xs=x1-width-height
                 cr.line_to(xs, y0)
                 cr.curve_to(xs , y0, xs+height, y0, xs+height, y)
                 cr.line_to(x1, y)
             cr.line_to(x1 , y1 - radius)
             cr.curve_to(x1, y1-radius, x1, y1, x1 - radius, y1)
             if conf.top_icon_show_logo:
                 cr.line_to(icon_x+icon_dx, y1)
                 cr.line_to(icon_x+icon_dx, icon_y+icon_dy-icon_radius)
                 cr.curve_to(icon_x+icon_dx, icon_y+icon_dy-icon_radius, icon_x+icon_dx, icon_y+icon_dy, icon_x+icon_dx-icon_radius, icon_y+icon_dy)
                 cr.line_to(icon_x+icon_radius, icon_y+icon_dy)
                 cr.curve_to(icon_x+icon_radius, icon_y+icon_dy, icon_x, icon_y+icon_dy, icon_x, icon_y+icon_dy-icon_radius)
                 cr.line_to(icon_x, y1)
             cr.line_to(x0+radius, y1)
             cr.curve_to(x0+radius, y1, x0 , y1, x0, y1-radius)
             cr.close_path()
         else:
             if (popup_style!=conf.popupstyle.NONE):
                 y1 = y1 - height
             ydw=y1+height
             
             
             cr.move_to(x0, y0 + radius)
             cr.curve_to(x0, y0 + radius, x0, y0, x0 + radius, y0)                
             if conf.top_icon_show_logo:
                 cr.line_to(icon_x, y0)
                 cr.line_to(icon_x, icon_y+icon_radius)
                 cr.curve_to(icon_x, icon_y+icon_radius, icon_x, icon_y, icon_x+icon_radius, icon_y)
                 cr.line_to(icon_x+icon_dx-icon_radius, icon_y)
                 cr.curve_to(icon_x+icon_dx-icon_radius, icon_y, icon_x+icon_dx, icon_y, icon_x+icon_dx, icon_y+icon_radius)
                 cr.line_to(icon_x+icon_dx, y0)
             
             cr.line_to(x1 - radius, y0)
             cr.curve_to(x1 -radius , y0, x1, y0, x1, y0 + radius)
             if (popup_style!=conf.popupstyle.RIGHT):
                 cr.line_to(x1 , y1 - radius)
                 cr.curve_to(x1, y1-radius, x1, y1, x1 - radius, y1)
             else:
                 cr.line_to(x1 , ydw)
                 cr.line_to(x1-width , ydw)
                 cr.curve_to(x1-width, ydw, x1-width, y1, x1 - width - height, y1)
                 pass
             if (popup_style==conf.popupstyle.CENTER):
                 xds=(x1+width)/2
                 cr.line_to(xds + height, y1)
                 cr.curve_to(xds+height, y1, xds, y1, xds, ydw)
                 cr.line_to(xds-width, ydw)
                 cr.curve_to(xds-width, ydw, xds-width, y1, xds-width-height, y1)
             if (popup_style!=conf.popupstyle.LEFT):
                 cr.line_to(x0+radius, y1)
                 cr.curve_to(x0+radius, y1, x0 , y1, x0, y1-radius)
             else:
                 cr.line_to(x0+width+height, y1)
                 cr.curve_to(x0+width+height, y1, x0+width, y1, x0+width, ydw)
                 cr.line_to(x0, ydw)
             cr.close_path()
             
     def render_light_rect(self, cr, x, y, w, h, o):
         # Crea un rettangolo con i bordi arrotondati
         x0 = x
         y0 = y
         rect_width = w
         rect_height = h
         radius = 10 + o
         
         top=conf.top_position.get_top()
         if top==conf.top_position.DW_LEFT or top==conf.top_position.DW_RIGHT:
             radius_top=5
             radius_dw=radius
         else:
             radius_top=radius
             radius_dw=5
         
         x1 = x0 + rect_width
         y1 = y0 + rect_height
         cr.move_to(x0, y0 + radius_top)
         cr.curve_to(x0, y0 + radius_top, x0, y0, x0 + radius_top, y0)
         cr.line_to(x1 - radius_top, y0)
         cr.curve_to(x1 -radius_top , y0, x1, y0, x1, y0 + radius_top)
         cr.line_to(x1 , y1 - radius_dw)
         cr.curve_to(x1, y1-radius_dw, x1, y1, x1 - radius_dw, y1)
         cr.line_to(x0+radius_dw, y1)
         cr.curve_to(x0+radius_dw, y1, x0 , y1, x0, y1-radius_dw)
         cr.close_path()    
     
     def render_icon_rect(self, cr, x, y, w, h, o):
         x0 = x
         y0 = y
         rect_width = w
         rect_height = h
         radius = 10 + o
         
         x1 = x0 + rect_width
         y1 = y + rect_height         
                  
         cr.move_to(x0, y0 + radius)
         cr.curve_to(x0, y0 + radius, x0, y0, x0 + radius, y0)
         cr.line_to(x1 - radius, y0)
         cr.curve_to(x1 -radius , y0, x1, y0, x1, y0 + radius)
         cr.line_to(x1 , y1 - radius)
         cr.curve_to(x1, y1-radius, x1, y1, x1 - radius, y1)
         cr.line_to(x0+radius, y1)
         cr.curve_to(x0+radius, y1, x0 , y1, x0, y1-radius)
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
         (diff, applet_diff)=conf.read_conf()
         if diff or applet_diff:
             self.change(force=True)
         
         if self.supports_alpha and conf.safe_mode==False:
              self.draw_window(cr)
         else:
             self.draw_safe_window(cr)
         
         if conf.top_icon_show_logo:
             self.draw_icon_place(cr)
         
         if event!=None:
             # chiediamo esplicitamente ai figli di disegnarsi
             # Se non lo facessimo non sarebbero visualizzati
             # i widgets aggiunti alla TransparentWindow
             children = self.get_children()
             for c in children:
                     self.propagate_expose(c, event)
    
     def draw_window(self, cr):     
         top=conf.top_position.get_top()
         down=False
         if top==conf.top_position.DW_LEFT or top==conf.top_position.DW_RIGHT:
             down=True
         (width, height) = self.get_size()
         x=0
         y=0
         if down and conf.top_icon_show_logo: 
             y=0
             height=height-40
         elif  conf.top_icon_show_logo: 
             y=40
             height=height-y
         
         cr.move_to(0, 0)
         cr.set_line_width(1.0)

         cr.set_operator(cairo.OPERATOR_OVER)

         pat=self.get_gradient()
         self.render_rect(cr, x, y, width, height, 10)
         cr.set_source(pat)
         cr.fill()


         #Lightening
         if (conf.show_lighting):
             col = hex2float(conf.lightingcolor)
             pat.add_color_stop_rgba(0.2, col[0], col[1], col[2], col[3])
             if (not down): self.render_light_rect(cr, x, y, width, 20, 10)
             else: self.render_light_rect(cr, x, height-20, width, 20, 10)
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
     
     def get_icon_position(self):
         (width, height) = self.get_size()
         top=conf.top_position.get_top()
         if top==conf.top_position.DW_LEFT:
             (x, y)=(0, height-95)
             (dx, dy) = (31, -5)
         elif top==conf.top_position.DW_RIGHT:
             (x, y)=(width-95, height-95)
             (dx, dy) = (-31, -5)
         elif top==conf.top_position.TOP_RIGHT:
             (x, y)=(width-95, 0)
             (dx, dy) = (-31, 5)
         else:
             (x, y)=(0, 0)
             (dx, dy) = (31, 5)
         
         return (x, y, dx, dy)
     
     def draw_icon_place(self, cr):
         x, y, dx, dy=self.get_icon_position()

         gradient=self.get_gradient()
         
         col = hex2float(conf.iconbgcolor)
         cr.set_source_rgba(col[0], col[1], col[2], col[3])
         self.render_icon_rect(cr, x + dx + 5, y + dy +5, 85, 85, 0)
         
         cr.fill()
         pass
     
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
