from threading import Thread
import time
from AGM.AGM_default_config import conf as config
conf=config()

class Show_menu(Thread):
    def __init__(self, menu_show):
        Thread.__init__(self)
        self.show_menu=menu_show
        self.end=False
    
    def exit_loop(self):    
        self.end=True
    
    def run(self):
        while self.end==False:
            time.sleep(1)
            content="0"
            try:
                file=open(conf.show_path, "r")
                content=file.read()
                file.close()
            except: print "cannot read show file"
            if content.replace("\n", "") == "1":
                
                file=open(conf.show_path, "w")
                file.write("0")
                file.close()
                self.show_menu()

def ask_show_menu():
    file=open(conf.show_path, "w")
    file.write("1")
    file.close()