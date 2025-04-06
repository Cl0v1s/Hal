from invoke import task
import os
import act

@task
def installActions(c):
    for dir in os.walk(act.ACTIONS_DIR):
        if(dir[0] == act.ACTIONS_DIR):
            continue
        if "requirements.txt" in dir[2]:
            print("Installing requirements for " + dir[0] + " action:")
            c.run("pip install -r "+ os.path.join(dir[0], "requirements.txt"))

@task
def install(c):
    c.run("pip install -r requirements.txt")
    installActions(c)

@task
def build(c):
    c.run('g++ -shared -lSDL2 -lSDL2_ttf  -o lib.so -fPIC c/lib.cpp')
    
@task(iterable=['name'])
def learnName(c, name):
    c.run("python -m eff_word_net.generate_reference --input-dir name/records --output-dir name --model-type resnet_50_arc --wakeword " + name[0])

@task
def learnActions(c):
    import train
    train.do()