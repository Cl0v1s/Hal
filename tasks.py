from invoke import task

@task
def build(c):
    c.run('g++ -shared -lSDL2  -o lib.so -fPIC c/lib.cpp')
    