extern "C" {
    #include "./compat.h"
    #include "./display.h"
    #include "./eyes.h"
    #include "./text.h"

    SDL_Event e;
    bool pollEvent() {
        bool quit = false;
        SDL_Delay(30);
        while( SDL_PollEvent( &e ) != 0 )
        {
            if( e.type == SDL_QUIT )
            {
                quit = true;
            }
        }
        return quit;
    }

    RoboEyes roboEyes;
    TextUI textUI;

    void setColors(int bgr, int bgg, int bgb, int mainr, int maing, int mainb) {
        roboEyes.BGCOLOR = display.GetColor(bgr, bgg, bgb, 255);
        roboEyes.MAINCOLOR = display.GetColor(mainr, maing, mainb, 255);
    }

    void beginEyes(int w, int h, int rate) {
        roboEyes.begin(w, h, rate);
    }

    void beginText(int x, int y, int w, int h) {
        textUI.begin(x, y, w, h);
    }

    void setAutoblinker(bool active, int interval, int var) {
        roboEyes.setAutoblinker(active, interval, var);
    }

    void setIdleMode(bool active, int interval, int var) {
        roboEyes.setIdleMode(active, interval, var);
    }

    void update() {
        roboEyes.update();
        textUI.update();
    }

    void setWidth(int left, int right) {
        roboEyes.setWidth(left, right);
    }

    void setHeight(int left, int right) {
      roboEyes.setHeight(left, right);
    }

    void setBorderradius(int left, int right) {
        roboEyes.setBorderradius(left, right);
    }

    void setSpacebetween(int space) {
        roboEyes.setSpacebetween(space);
    }

    void setMood(unsigned char mood) {
        roboEyes.setMood(mood);
    }

    void setPosition(unsigned char mood) {
        roboEyes.setPosition(mood);
    }

    void setCuriosity(bool on) {
        roboEyes.setCuriosity(on);
    }

    void setHFlicker(bool on,int v) {
        roboEyes.setHFlicker(on, v);

    }

    void setVFlicker(bool on,int v) {
        roboEyes.setVFlicker(on, v);
    }

    void anim_confused() {
        roboEyes.anim_confused();
    }

    void anim_laugh() {
        roboEyes.anim_laugh();
    }

    void write(char* text) {
        textUI.write(text);
    }
}