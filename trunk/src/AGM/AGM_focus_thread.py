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
from threading import Thread

from time import sleep
class FocusThread(Thread):
    def __init__(self, get_win_focus, get_applet_focus, get_hidden, set_hidden, show_hide):
        Thread.__init__(self)
        self.get_win_focus=get_win_focus
        self.get_applet_focus=get_applet_focus
        
        self.get_hidden=get_hidden
        self.set_hidden=set_hidden
        self.show_hide_function=show_hide
        
        self.running=True
    
    def set_visible(self):
        self.hidden=True
        self.show_hide_function()
    
    def set_not_visible(self):
        self.hidden=False
        self.show_hide_function()
            
    def stop(self):
        self.running=False
    
    def run(self):
        while(self.running):
            sleep(1)
            #print self.get_win_focus(), self.get_applet_focus(), self.get_hidden()
            if (self.get_hidden()==False):
                if (self.get_win_focus()==False and self.get_applet_focus()==False):
                    #print "NOFOCUS"
                    self.show_hide_function()