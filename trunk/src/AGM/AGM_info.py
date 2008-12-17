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
from AGM.AGM_default_config import conf as config

conf=config()
import os

class Info(gtk.AboutDialog):
    def __init__(self, stand_alone=False):
        gtk.AboutDialog.__init__(self)
        self.stand_alone=True
        gtk.about_dialog_set_url_hook(self.link_open, "website")
        gtk.about_dialog_set_email_hook(self.link_open, "mail")
        
        self.set_title("AGM")
        self.set_name("Advanced Gnome Menu")
        self.set_version("0.8")
        self.set_copyright("(c) 2008 Marco Mosconi")
        self.set_license('''    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
''')
        self.set_website("www.sciallo.net/AGM/")
        self.set_authors(["Marco Mosconi <brus46@gmail.com>", "Fanen Ahua <afanen01@gmail.com>"])
        self.set_artists(["sentinella86 - Ubuntu.it user"])
        self.set_program_name("AGM")
        self.set_comments("Advanced Gnome Menu\nThis program provide an eye-candy gnome menu.\nThis has been developed thinking with inspiration from new netbooks.")
        icon=gtk.gdk.pixbuf_new_from_file(conf.default_logo_path)
        self.set_icon(icon)
        self.set_logo(icon)
        
        self.connect("destroy", self.close)
        self.connect("response", self.close)
        
        self.show_all()
        if self.stand_alone:
            gtk.main()
    
    def link_open(self, d, link, data):
        print link
        if (os.fork()):
            if data=="mail":
                command=conf.open_file_command
                command=command.replace("%U", "mailto:" + link)
                command=command.replace("%u", "mailto:" + link)
                command=command.split(" ")
                os.execvp(command[0], command)
            else:
                command=conf.open_file_command
                command=command.replace("%U", link)
                command=command.replace("%u", link)
                command=command.split(" ")
                os.execvp(command[0], command)
    
    def close(self, obj=None, win=None):
        self.hide_all()
        if self.stand_alone:
            gtk.main_quit()
    
