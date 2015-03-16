# How to create a plugin for AGM #

  * Plugins must be written in Python
  * Plugins must have a class "Plugin" extending AGM.AGM\_plugin.AGM\_plugin


---

# Basic structure example #

```
from AGM.AGM_plugin import AGM_plugin as plugin
from AGM import AGM_plugin
# This is a AGM plugin
class Plugin(plugin):
    def __init__(self):
        plugin.__init__(self)
        #Author and plugin info
        self.author="Marco Mosconi <brus46@gmail.com>"
        self.author_site="http://www.sciallo.net"
        self.name="Test plugin"
        self.description="This plugin doesn't do nothing."
        self.license="GPL"
        self.type=AGM_plugin.TYPE_MIX # can be TYPE_MENU, TYPE_SEARCH or TYPE MIX, default TYPE_MIX
        self.is_configurable=False #If false the program assume that you cannot configure this plugin.
        pass
    
    def configure(self):
        # If the plugin is configurable this function will be called when the user press "Configure"
        pass
    
    # if type = TYPE_MENU or TYPE_MIX this function will be called in order to obtain the items of a menu (after i'll explain better how to write this.)
    def get_menu(self, parent=None):
        menu=[]        
        return menu
    
    #if type=TYPE_SEARCH or TYPE_MIX this function will be called in order to obtain a list of elements which matches with the search-key (after i'll explain better how to write this.)
    def search(self, key):
        return []
```