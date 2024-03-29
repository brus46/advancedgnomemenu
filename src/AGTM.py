#!/usr/bin/python

#    Program name: AGTM - Advanced Gnome Tab Menu
#    Project version: 0.0.1
#    Project licence: GPL v3
# 
#    Author name:    Marco Mosconi
#    Author email:   brus46@gmail.com
#    Author website: http://www.sciallo.net

#    This program is free software: you can redistribute it and/or modify
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


import os, sys

FILEPATH = os.path.abspath(__file__)
pwd, dirname = os.path.split(os.path.dirname(FILEPATH))
if dirname != "src":
    print 'Running installed agtm, modifying PYTHONPATH.'
    sys.path.insert(0, "/usr/local/lib/python/")


from AGTM.MainWindow import MainWindow

MainWindow()