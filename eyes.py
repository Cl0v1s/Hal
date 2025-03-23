from ctypes import *
from threading import Thread, Event

instance = None


def get_instance():
    return instance



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
    roboEyes = CDLL('./lib.so')
    roboEyes.pollEvent.restype = c_bool
    roboEyes.initMillis()
    roboEyes.setColors(0,0,0, 255, 255, 255)
    roboEyes.begin(200, 200, 30)
    roboEyes.setAutoblinker(True, 3, 2); 
    roboEyes.setIdleMode(True, 2, 2);
    roboEyes.setWidth(36, 36); 
    roboEyes.setHeight(42, 42); 
    roboEyes.setBorderradius(8, 8); 
    roboEyes.setSpacebetween(14); 

    instance = roboEyes
    ready.set()
    quit = False
    while quit != True:
        quit = roboEyes.pollEvent();
        roboEyes.update();
    stop.set()