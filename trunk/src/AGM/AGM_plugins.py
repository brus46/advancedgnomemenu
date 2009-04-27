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

import AGM_plugin
import sys, os
from AGM_default_config import conf as config
conf=config()

FILEPATH = os.path.abspath(__file__)
pwd, dirname = os.path.split(os.path.dirname(FILEPATH))
if dirname != "src":
    print 'Running installed agm, modifying PYTHONPATH.'
    sys.path.insert(0, "/usr/local/lib/python/AGMplugins/")
else:
    sys.path.insert(0, "./AGMplugins/")

def get_child_plugins():
    myplugins={}
    folder=conf.plugin_folder
    listafile=os.listdir(folder)
    listafile.sort()
    
    for file in listafile:
        if os.path.isfile(folder+file) and file.find(".py")>0 and file.find(".pyc")<0 and file.find("__")<0:
            try:
                file=file.replace(".py", "")
                #currentPlugin=__import__('AGMplugins/' + file)
                currentPlugin=__import__(file)
                myplugins[file] = currentPlugin.Plugin()
            except AttributeError:
                print "Attribute Error ", file ,sys.exc_info()[1]
            except:
                print "Error loading " + file + " plugin", sys.exc_info()[1]

    #If a plugin isn't an instance of AGM_plugin this isn't a plugin.
    for plugin in myplugins:
        if not (isinstance(myplugins[plugin], AGM_plugin.AGM_plugin)):
            print plugin + " isn't an instance of AGM_plugin!"
            myplugins.remove(plugin)
             
    return myplugins