import random
import bips
import json
import pathlib
import psutil
import os 

INTENTS = [
    "HI",
    "CHANGELOG",
    "DIAGNOSTIC",
]

def hi():
    with open(pathlib.Path(__file__).parent.resolve().joinpath('hi.json')) as f:
        data = json.load(f)
        index = random.randrange(0, len(data))
        bips.say(data[index]["text"])

def changelog():
    with open(pathlib.Path(os.getcwd()).resolve().joinpath('changelog.json')) as f:
        data = json.load(f)
        tag = list(data.items())[-1]
        bips.say(tag[0])
        for entry in tag[1]:
            bips.say(entry["message"])
    pass

def diagnostic():
    bips.say("CPU: <prosody pitch='120'>{0}</prosody>%;".format(psutil.cpu_percent()))
    bips.say("Memory: <prosody pitch='120'>{0}</prosody>%;".format(round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)))
    pass


def main(intent, request):
    match intent:
        case "HI":
            return hi()
        case "CHANGELOG":
            return changelog()
        case "DIAGNOSTIC":
            return diagnostic()
        case _:
            return 0
        
if __name__ == "__main__":
    changelog()


