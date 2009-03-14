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
from Config import config
from AG_commons import utils

conf=config()
hex2float=utils.hex2float

if gtk.pygtk_version < (2, 10, 0):
     print 'This programs needs PyGtk >= 2.10'
     raise SystemExit


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
         self.set_app_paintable(True)
         self.set_decorated(False)
         self.add_events(gtk.gdk.FOCUS_CHANGE_MASK)
         
         self.mini=True
         self.do_screen_changed()

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
         
         position = conf.position         
         x0 = x
         y0 = y
         rect_width = w
         rect_height = h
         radius = o
         
         x1 = x + rect_width
         y1 = y + rect_height         
                      
         if position=="top":
             cr.move_to(x0, y0)
             cr.line_to(x1, y0)
             cr.line_to(x1, y1-radius)
             cr.curve_to(x1, y1 - radius, x1, y1, x1 - radius, y1)
             cr.line_to(x0+radius, y1)
             cr.curve_to(x0 + radius, y1, x0, y1, x0, y1 - radius)
         else:
             cr.move_to(x0, y0 + radius)
             cr.curve_to(x0, y0 + radius, x0, y0, x0 + radius, y0)
             cr.line_to(x1 - radius, y0)
             cr.curve_to(x1 -radius , y0, x1, y0, x1, y0 + radius)
             cr.line_to(x1, y1)
             cr.line_to(x0, y1)
         
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
         
         if self.supports_alpha and conf.safe_mode==False:
              self.draw_window(cr)
         else:
             self.draw_safe_window(cr)
         
         children = self.get_children()
         if event!=None:
             for c in children:
                 self.propagate_expose(c, event)
    
     def draw_window(self, cr):     
         (width, height) = self.get_size()
         x=0
         y=0
         
         cr.move_to(0, 0)
         cr.set_line_width(1.0)

         cr.set_operator(cairo.OPERATOR_OVER)
         radius=20
         if self.mini: 
             height=35
             radius=5
         self.render_rect(cr, x, y, width, height, radius)
         col = utils.hex2float(conf.bgcolor)
         cr.set_source_rgba(col[0], col[1], col[2], col[3])
         cr.fill()

     def draw_safe_window(self, cr):
         (width, height) = self.get_size()
         x=0
         y=0
         cr.move_to(0, 0)
         cr.set_line_width(1.0)

         cr.set_operator(cairo.OPERATOR_OVER)
         if self.mini: height=35
         self.render_safe_rect(cr, x, y, width, height)
         col = utils.hex2float(conf.bgcolor)
         cr.set_source_rgba(col[0], col[1], col[2], col[3])
         cr.fill()
     
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
