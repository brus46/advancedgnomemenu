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

import gettext, locale
import gtk.glade


def Translate(string):
    locale.setlocale(locale.LC_ALL, '')  
    for module in gtk.glade, gettext:
        #print module
        module.bindtextdomain('advanced-gnome', "./locale/")  
        module.textdomain('advanced-gnome')
    #print string, gettext.gettext(string)
    return unicode( gettext.gettext(string), "utf-8" )

language = locale.getlocale(locale.LC_ALL)[0]
#print "Your language is: " + language
