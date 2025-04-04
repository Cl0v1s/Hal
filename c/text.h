#ifndef TEXT_H
#define TEXT_H

#include "display.h"

class TextUI {
    private:
        int screenX;
        int screenY;
        int screenWidth;
        int screenHeight;

        float textIndex = 0;
        char* currentText = NULL;

    public:
        TextUI() {

        }

        ~TextUI() {
            if(currentText != NULL) {
                free(currentText);
            }
        }

        void begin(int x, int y, int w, int h) {
            screenX = x;
            screenY = y;
            screenWidth = w;
            screenHeight = h;
        }

        void write(char* text) {
            textIndex = 0;
            if(currentText != NULL) {
                free(currentText);
            }
            currentText = (char*)malloc(strlen(text) + 1);
            strncpy(currentText, text, strlen(text) + 1);
        }

        void update() {
            display.clear(screenX, screenY, screenWidth, screenHeight);
            if(currentText == NULL) return;
            if(textIndex <= strlen(currentText)) {
                textIndex += 0.4;
            }
            int idx = textIndex / 1;
            char text[idx + 2];
            strncpy(text, currentText, idx);
            text[idx] = textIndex <= strlen(currentText) ? '_' : '\0';
            text[idx+1] = '\0';
            display.fillText(screenX + 20, screenY + 20, screenWidth - 40, text);
        }
};

#endif
