from ctypes import *

if __name__ == "__main__":
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
    
    roboEyes.setMood(0)
    
    quit = False
    while quit != True:
        quit = roboEyes.pollEvent();
        roboEyes.update();
    