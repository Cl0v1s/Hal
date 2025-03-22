#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>

#ifndef DISPLAY_H
#define DISPLAY_H

class Display {
private: 
    SDL_Window* win;
    SDL_Surface* surface;
    SDL_Renderer* renderer;

public:
    Display(int w, int h) {
        SDL_Init(SDL_INIT_EVERYTHING);
        this->win = SDL_CreateWindow("Luxy", 100, 100, w, h, SDL_WINDOW_SHOWN);
        this->surface = SDL_GetWindowSurface(this->win);
        this->renderer = SDL_GetRenderer(this->win);
    }

    ~Display() {
        SDL_DestroyRenderer(this->renderer);
        SDL_DestroyWindow(this->win);
        SDL_Quit();
    }

    void clearDisplay() {
        SDL_RenderClear(this->renderer);
    }

    void display() {
        SDL_RenderPresent(this->renderer);
    }

    unsigned int GetColor(int r, int g, int b, int a) {
        return SDL_MapRGBA(this->surface->format, r, g, b, a);
    }

    void fillRoundRect(int x0, int y0, int w, int h, uint8_t radius, int color) {
        Uint8 r = (color >> 16) & 0xFF;
        Uint8 g = (color >> 8) & 0xFF;
        Uint8 b = color & 0xFF;
        Uint8 a = (color >> 24) & 0xFF;
        SDL_SetRenderDrawColor( this->renderer, r, g, b, a); // Draw in solid blue
        SDL_Rect rect;
        rect.x = x0;
        rect.y = y0;
        rect.w = w;
        rect.h = h;
        SDL_RenderFillRect(this->renderer, &rect);
    }

    void fillTriangle(float x0, float y0, float x1, float y1, float x2, float y2, int color) {
        Uint8 r = (color >> 16) & 0xFF;
        Uint8 g = (color >> 8) & 0xFF;
        Uint8 b = color & 0xFF;
        Uint8 a = (color >> 24) & 0xFF;
        SDL_Vertex triangleVertex[3]=
        {
            {
                { x0,y0}, /* first point location */ 
                { r, g, b, a }, /* first color */ 
                { 0.f, 0.f }
            },
            {
                { x1, y1 }, /* second point location */ 
                { r,g,b, a }, /* second color */
                { 0.f, 0.f }
            },
            {
                { x2, y2 }, /* third point location */ 
                { r,g,b, a }, /* third color */
                { 0.f, 0.f }
            }
        };
        SDL_RenderGeometry(this->renderer, NULL, triangleVertex, 3, NULL, 0);
    }
};

Display display = Display(200, 200);

#endif 