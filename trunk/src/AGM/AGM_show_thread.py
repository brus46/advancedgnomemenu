
import threading
import time
import gtk
from AGM.AGM_default_config import conf as config

conf=config()

class ShowThread(threading.Thread):
    def __init__(self, show_function):
        threading.Thread.__init__(self)
        self.show_function=show_function
        self.stop=False
        self.start()
    
    def stopThread(self):
        self.stop=True
    
    def run(self):
        while(1):
           if not self.stop:
               time.sleep(0.01)
               show="0"
               try:
                   file=open(conf.show_path, "r")
                   show=file.read()
                   file.close()
               except: print "cannot read show... assume no-one whats me to show the window right now."
               show=show.replace("\n", "")
               gtk.gdk.threads_enter()
               if (show=="1"): 
                   self.show_function()
                   file=open(conf.show_path, "w")
                   file.write("0")
                   file.close()
               gtk.gdk.threads_leave()
           else:
               break