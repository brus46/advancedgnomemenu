from threading import Thread
import Launcher
class Show_launcher(Thread):
    def __init__(self):
        Thread.__init__(self)

def ask_show_launcher():
    Launcher.Launcher()
    pass