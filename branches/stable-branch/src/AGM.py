#!/usr/bin/python

#    Program name: AGM - Advanced Gnome Menu
#    Project version: 0.8.2
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
    print 'Running installed agm, modifying PYTHONPATH.'
    sys.path.insert(0, "/usr/local/lib/python/")


from AGM.AGM_Main_Window import AGM
from AGM.AGM_config import Config
from AGM.AGM_info import Info
from AGM.AGM_default_config import conf as config

conf=config()

no_trayicon=False
#no_trayicon=True
check=True
do_not_start=False
args=sys.argv
i=0
for arg in args:
    if i>0:
        conf.args+= arg + " "
    i+=1
    if arg=="--no-trayicon":
        no_trayicon=True
    elif arg=="--trayicon":
        no_trayicon=False
    elif arg=="--no-check-already-running":
        check=False
    elif arg=="--config":
        do_not_start=True
        Config(True)
    elif arg=="--info":
        do_not_start=True
        Info(True)
    elif arg=="--help":
        print "Help: "
        print "--no-trayicon:               don't show the trayicon"
        print "--no-check-already-running:  don't control if AGM is already running"
        print "--config:                    launch configurator"
        print "--help:                      show this help"
        do_not_start=True
        
if do_not_start==False:
    if check:
        cmd = os.popen('ps -ewwo pid,args')
        x = cmd.readlines()
        num_found=0
        for y in x:
           p = y.find('AGM.py')
           if p >= 0: 
               if y.find("<defunt>")>=0:
                   line=y.split(" ")
                   stop="kill -9 "+line[1]
                   os.system(stop)
                   num_found==0
               else:
                   num_found+=1
        
        if (num_found<=1): 
            if (no_trayicon):
                AGM(show_trayicon=False)
            else:
                AGM(top_buttons=False)
        else:
            print "AGM already running, sending onFocus command."
            file=open(conf.show_path, "w")
            file.write("1")
            file.close()
    else:
        if (no_trayicon):
            AGM(show_trayicon=False)
        else:
            AGM(top_buttons=False)            
