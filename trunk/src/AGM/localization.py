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

import locale
from AGM_default_config import conf as config
conf=config()

def ReadDict(language):
    dict={}
    lang_file=conf.install_data_dir + "locale/"+language+".lang"
    try:
        lang=open(lang_file)
        for word in lang.readlines():
            word=word.replace("\n", "")
            word=word.split("=")
            if len(word)==2:
                dict[word[0]]=word[1]
    except:
        print "Your language (" + language + ") is still unavailable"
    
    return dict

def Translate(string):
    if dict.has_key(string):
        return dict[string]
    else:
        #print "Warning: " + string + " translation not avaible!"
        return string

language = locale.getlocale(locale.LC_ALL)[0]
print "Your language is: " + language
dict=ReadDict(language)
