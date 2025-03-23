import os 
import json

ACTIONS_DIR = "actions"

def action_is_well_defined(dir):
    files = dir[2]
    if(('data.json' in files and '__init__.py' in files) == False):
        return False
    return True

def load_action(dir, with_data = False):
    action = __import__(dir[0].replace("/", "."), fromlist = ["*"])
    data = []
    if(with_data == True):
        with open(dir[0] + os.sep + "data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    return [action.INTENTS, action.main, data]

def load_actions(with_data = False):
    actions = []
    for dir in os.walk(ACTIONS_DIR):
        if(dir[0] == ACTIONS_DIR):
            continue
        if action_is_well_defined(dir):
            actions.append(load_action(dir, with_data))
    return actions