from invoke import task
import os
import act

@task
def install(c):
    c.run("pip install -r requirements.txt")
    for dir in os.walk(act.ACTIONS_DIR):
        if(dir[0] == act.ACTIONS_DIR):
            continue
        if "requirements.txt" in dir[2]:
            print("Installing requirements for " + dir[0] + " action:")
            c.run("pip install -r "+ os.path.join(dir[0], "requirements.txt"))



@task
def build(c):
    c.run('g++ -shared -lSDL2 -lSDL2_ttf  -o lib.so -fPIC c/lib.cpp')
    
@task
def actions(c):
    import train
    train.do()