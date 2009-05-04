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

import AGM_Fav_app_model
import sys, os
from AGM_default_config import conf as config
conf=config()

FILEPATH = os.path.abspath(__file__)
pwd, dirname = os.path.split(os.path.dirname(FILEPATH))
if dirname != "src":
    print 'Running installed agm, modifying PYTHONPATH.'
    sys.path.insert(0, "/usr/local/lib/python/AGM_Fav_apps_models/")
else:
    sys.path.insert(0, "./AGM_Fav_apps_models/")

def get_child_models():
    mymodels={}
    folder=conf.model_folder
    listafile=os.listdir(folder)
    listafile.sort()
    
    for file in listafile:
        if os.path.isfile(folder+file) and file.find(".py")>0 and file.find(".pyc")<0 and file.find("__")<0:
            try:
                file=file.replace(".py", "")
                currentmodel=__import__(file)
                mymodels[file] = currentmodel.Model()
            except:
                print "Error loading " + file + " model", sys.exc_info()[1]

    #If a model isn't an instance of AGM_Fav_app_model this isn't a model.
    for model in mymodels:
        if not (isinstance(mymodels[model], AGM_Fav_app_model.model)):
            print model + " isn't an instance of AGM_model!"
            mymodels.remove(model)
             
    return mymodels

def get_model(modelname):
    models=get_child_models()
    for model_name in models:
        model=models[model_name]
        if model.model_code_name==modelname:
            return model
    return None
    