from invoke import task
import train

@task
def build(c):
    c.run('g++ -shared -lSDL2 -lSDL2_ttf  -o lib.so -fPIC c/lib.cpp')
    
@task
def actions(c):
    train.do()