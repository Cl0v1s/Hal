from ctypes import *
from threading import Thread, Event

instance = None


def get_instance():
    return instance

def thinking(mode):
    if mode:
        instance.setMood(3)
    else:
        instance.setMood(0)


def attention(mode):
    instance.setIdleMode(mode == False, 2, 2);
    if(mode):
        instance.setHeight(42, 32)
        instance.setSpacebetween(20); 
    else:
        instance.setHeight(42, 42)
        instance.setSpacebetween(14); 
    instance.setPosition(0)

def loop(ready, stop):    
    global instance
    ui = CDLL('./lib.so')
    ui.pollEvent.restype = c_bool
    ui.initMillis()
    ui.setColors(0,0,0, 255, 255, 255)
    ui.beginEyes(300, 200, 30)
    ui.beginText(0, 200, 300, 100)
    ui.setAutoblinker(True, 3, 2); 
    ui.setIdleMode(True, 2, 2);
    ui.setWidth(36, 36); 
    ui.setHeight(42, 42); 
    ui.setBorderradius(8, 8); 
    ui.setSpacebetween(14); 

    instance = ui
    ready.set()
    quit = False
    while quit != True:
        quit = ui.pollEvent();
        ui.update()
    stop.set()

if __name__ == "__main__":
    ready = Event()
    stop = Event()
    loop(ready, stop)