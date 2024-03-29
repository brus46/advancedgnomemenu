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

import gtk, os, sys
import AGM.AGM_utils as utils
from AGM.AGM_default_config import conf as config
conf=config()
import localization
_=localization.Translate
import AGM_Entry

class ExecuteBar(gtk.HBox):
    def __init__(self, get_gradient):
        gtk.HBox.__init__(self)
        conf.read_conf()
        self.command=AGM_Entry.Entry(get_gradient)
        #self.command.do_expose_event()
        self.run_in_terminal=gtk.Button()
        terminal_icon=gtk.Image()
        icon=utils.getPixbufFromName("terminal", 22, "app")
        terminal_icon.set_from_pixbuf(icon)
        self.run_in_terminal.set_image(terminal_icon)
        
        self.label=gtk.Label(_("Execute")+ ":")
        self.label.set_size_request(50, -1)
        
        self.run_in_terminal.set_relief(gtk.RELIEF_NONE)
        self.pack_end(self.run_in_terminal, False)
        self.pack_end(self.command)
        
        self.command.set_tooltip_text(_("Execute"))
        self.command.connect("activate", self.execute_command)
        self.run_in_terminal.connect("clicked", self.terminal_execution)
        self.pack_start(self.label, False)
        
    def execute_command(self, obj):
        command=self.command.get_text()
        if (command!=""):
            if (os.fork()==0):
                command=command.split(" ")
                try:
                   os.chdir(os.path.expanduser("~"))
                   os.execvp(command[0], command)
                except: print "Command fail: " + str(command)
                sys.exit(-1)
    
    def terminal_execution(self, obj):
        command=self.command.get_text()
        if command!="":
            if (os.fork()==0):
                execute_command=conf.execution_box_terminal_command.split(" ")
                new_command=[]
                for part in execute_command:
                    if part.find("%U")>=0 or part.find("%u")>=0:
                        part=part.replace("%u", command)
                        part=part.replace("%U", command)
                    new_command.append(part)
                #print new_command
                os.execvp(new_command[0], new_command)
                sys.exit(-1)

    def modify_bg(self, state, color):
        if conf.use_custom_color:
            self.run_in_terminal.modify_bg(state, color)
    def modify_fg(self, state, color):
        if conf.use_custom_color:
            self.label.modify_fg(state, color)
    def set_text(self, string):
        self.command.set_text(str(string))